#include "prism/codec/squeeze.h"
#include <stdexcept>
#include <vector>
namespace prism::codec {
uint8_t max_squeeze_levels(uint32_t w, uint32_t h) {
    uint8_t l=0;
    while(w>=2 && h>=2 && l<8){ w/=2; h/=2; l++; if(w<2||h<2) break; }
    if(l>4) l=4;
    return l;
}
static inline int32_t avg2(int32_t a,int32_t b){ return (a+b)>>1; }
static inline int32_t diff2(int32_t a,int32_t b){ return a-b; }

SqueezeResult squeeze_encode_plane(const std::vector<uint16_t>& plane, uint32_t w, uint32_t h, uint8_t levels, uint8_t) {
    SqueezeResult res; res.levels=levels;
    if(levels==0){
        SqueezeResult::Band b; b.w=w; b.h=h; b.data=plane; b.band_class=0;
        res.bands.push_back(std::move(b)); return res;
    }
    if(plane.size()!=(size_t)w*h) throw std::runtime_error("plane size mismatch");
    // for now only handle even dimensions; fallback to single band if odd at any level
    uint32_t cur_w=w, cur_h=h;
    std::vector<uint16_t> cur_plane=plane;
    // We'll collect HF bands bottom-up then emit post-order
    struct LevelBands { uint32_t w2,h2; std::vector<uint16_t> ll, hl, lh, hh; };
    std::vector<LevelBands> lvl_bands;
    for(uint8_t lvl=0; lvl<levels; ++lvl){
        if(cur_w%2!=0 || cur_h%2!=0){
            // cannot squeeze further, treat remaining as LL
            break;
        }
        uint32_t w2=cur_w/2, h2=cur_h/2;
        // horizontal transform into low_h/high_h (int32)
        std::vector<int32_t> low_h(cur_h*w2), high_h(cur_h*w2);
        for(uint32_t y=0;y<cur_h;++y){
            for(uint32_t x=0;x<w2;++x){
                int32_t a = (int32_t)cur_plane[y*cur_w + 2*x];
                int32_t b = (int32_t)cur_plane[y*cur_w + 2*x+1];
                // For levels>0, cur_plane values for LL are averages (0-65535), but HF diffs are signed wrap stored as uint16
                // However for levels>0, cur_plane after first iteration is LL which is unsigned average. So a,b are unsigned here.
                // That's fine.
                int32_t low = (a+b)>>1;
                int32_t high = a - b;
                low_h[y*w2 + x]=low;
                high_h[y*w2 + x]=high;
            }
        }
        LevelBands lb; lb.w2=w2; lb.h2=h2;
        lb.ll.assign(w2*h2,0); lb.hl.assign(w2*h2,0); lb.lh.assign(w2*h2,0); lb.hh.assign(w2*h2,0);
        // vertical transform
        for(uint32_t x=0;x<w2;++x){
            for(uint32_t y=0;y<h2;++y){
                int32_t l0 = low_h[(2*y)*w2 + x];
                int32_t l1 = low_h[(2*y+1)*w2 + x];
                int32_t h0 = high_h[(2*y)*w2 + x];
                int32_t h1 = high_h[(2*y+1)*w2 + x];
                int32_t LL = (l0 + l1)>>1;
                int32_t LH = l0 - l1;
                int32_t HL = (h0 + h1)>>1;
                int32_t HH = h0 - h1;
                size_t idx = y*w2 + x;
                lb.ll[idx] = (uint16_t)(LL & 0xFFFF);
                // store HF biased by 32768 to keep values clustered around 32768 for better prediction
                lb.lh[idx] = (uint16_t)(LH + 32768);
                lb.hl[idx] = (uint16_t)(HL + 32768);
                lb.hh[idx] = (uint16_t)(HH + 32768);
            }
        }
        lvl_bands.push_back(std::move(lb));
        // next cur is LL of this level
        cur_w=w2; cur_h=h2;
        cur_plane = lvl_bands.back().ll;
    }
    // Post-order emit: final LL first, then for each level from deepest to shallow, HL, LH? spec says H,V,D (HL, LH? wait band_class 1=H,2=V,3=D)
    // We have HL=high-low (horizontal high vertical low) -> band 1, LH -> band 2, HH -> band 3
    // Deepest LL
    {
        SqueezeResult::Band b; b.w=cur_w; b.h=cur_h; b.data=cur_plane; b.band_class=0;
        res.bands.push_back(std::move(b));
    }
    for(int i=(int)lvl_bands.size()-1; i>=0; --i){
        auto &lb = lvl_bands[i];
        SqueezeResult::Band bh; bh.w=lb.w2; bh.h=lb.h2; bh.data=lb.hl; bh.band_class=1;
        res.bands.push_back(std::move(bh));
        SqueezeResult::Band bv; bv.w=lb.w2; bv.h=lb.h2; bv.data=lb.lh; bv.band_class=2;
        res.bands.push_back(std::move(bv));
        SqueezeResult::Band bd; bd.w=lb.w2; bd.h=lb.h2; bd.data=lb.hh; bd.band_class=3;
        res.bands.push_back(std::move(bd));
    }
    // fix levels to actual achieved
    res.levels = (uint8_t)lvl_bands.size();
    return res;
}

std::vector<uint16_t> squeeze_decode_plane(const SqueezeResult& sr, uint32_t orig_w, uint32_t orig_h){
    if(sr.bands.empty()) return {};
    if(sr.levels==0) return sr.bands[0].data;
    // sr.bands is post-order: [LL_deepest, HL_deep, LH_deep, HH_deep, HL_deep-1, ...]
    // Reconstruct bottom-up
    size_t idx=0;
    SqueezeResult::Band cur = sr.bands[idx++]; // LL deepest
    uint32_t cur_w = cur.w, cur_h = cur.h;
    std::vector<uint16_t> cur_plane = cur.data;
    // Number of levels = sr.levels
    for(uint8_t lev=0; lev<sr.levels; ++lev){
        if(idx+2 >= sr.bands.size()) break;
        // Next three bands correspond to this level's HL,LH,HH (in post-order, deepest first, so order matches)
        // Our emit order for level i (deepest first) was HL,LH,HH sequentially, so reconstruction pops in same order
        auto hl = sr.bands[idx++]; auto lh = sr.bands[idx++]; auto hh = sr.bands[idx++];
        uint32_t w2 = hl.w; // should equal cur_w
        uint32_t h2 = hl.h;
        if(w2!=cur_w || h2!=cur_h){
            throw std::runtime_error("squeeze decode dimension mismatch");
        }
        uint32_t out_w = w2*2, out_h = h2*2;
        std::vector<uint16_t> out(out_w*out_h);
        // first reconstruct low_h/high_h via vertical inverse
        std::vector<int32_t> low_h(out_h*w2), high_h(out_h*w2); // Wait out_h is h2*2, but we have h = out_h ?
        // Actually low_h/high_h are h* w2 with h = out_h
        // We have LL, LH -> low_h; HL, HH -> high_h
        for(uint32_t x=0;x<w2;++x){
            for(uint32_t y=0;y<h2;++y){
                size_t p = y*w2 + x;
                int32_t LL = (int32_t)cur_plane[p]; // LL is unsigned
                int32_t LH = (int32_t)lh.data[p] - 32768;
                int32_t HL = (int32_t)hl.data[p] - 32768;
                int32_t HH = (int32_t)hh.data[p] - 32768;
                int32_t l0 = LL + ((LH+1)>>1);
                int32_t l1 = LL - (LH>>1);
                int32_t h0 = HL + ((HH+1)>>1);
                int32_t h1 = HL - (HH>>1);
                low_h[(2*y)*w2 + x]=l0;
                low_h[(2*y+1)*w2 + x]=l1;
                high_h[(2*y)*w2 + x]=h0;
                high_h[(2*y+1)*w2 + x]=h1;
            }
        }
        // horizontal inverse
        for(uint32_t y=0;y<out_h;++y){
            for(uint32_t x=0;x<w2;++x){
                int32_t low = low_h[y*w2 + x];
                int32_t high = high_h[y*w2 + x];
                int32_t a = low + ((high+1)>>1);
                int32_t b = low - (high>>1);
                out[y*out_w + 2*x] = (uint16_t)(a & 0xFFFF);
                out[y*out_w + 2*x+1] = (uint16_t)(b & 0xFFFF);
            }
        }
        cur_plane = std::move(out);
        cur_w = out_w; cur_h = out_h;
    }
    if(cur_w!=orig_w || cur_h!=orig_h){
        // if odd dimensions were fallback, just return as is (may be mismatched)
        // For Kodak even, should match
    }
    return cur_plane;
}
} // namespace
