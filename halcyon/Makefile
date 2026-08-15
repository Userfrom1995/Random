GHC      ?= ghc
GHC_FLAGS := -O2 -Wall -isrc
BIN      := halcyon
SRC      := $(shell find src -name '*.hs')

all: build

build: $(BIN)

$(BIN): $(SRC)
	$(GHC) $(GHC_FLAGS) --make src/Main.hs -o $(BIN)

test: build
	./$(BIN) selftest
	node js/node.js selftest
	node js/test.js

diff: build
	node js/test.js diff

clean:
	rm -f $(BIN)
	rm -f src/*.o src/*.hi
	rm -rf src/Halcyon/*.o src/Halcyon/*.hi
	rm -rf js/*.o js/*.hi

.PHONY: all build test diff clean