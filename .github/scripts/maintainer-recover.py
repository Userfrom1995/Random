import json, os, subprocess, sys

repo = os.environ["GITHUB_REPOSITORY"]
pat = os.environ["GH_TOKEN"]
bot_token = os.environ.get("BOT_TOKEN", pat)
push_url = f"https://x-access-token:{pat}@github.com/{repo}.git"

# Ensure all commits are authored as Mae (Maintainer) bot, never owner
for k, v in [
    ("user.name", "Mae (Maintainer)"),
    ("user.email", "github-actions[bot]@users.noreply.github.com"),
]:
    subprocess.run(["git", "config", k, v], capture_output=True)

decisions = []
if os.path.exists(".maintainer/decision.json"):
    try:
        decisions = json.load(open(".maintainer/decision.json"))
    except Exception as e:
        print(f"decision.json unparseable: {e}")

recovers = [d for d in decisions if d.get("action") in ("recover", "merge")]
# Fallback autonomous scan: if Mae did not emit recover, auto-detect closed bot PRs with head not in main
if not recovers:
    print("No recover decisions from Mae; running fallback auto-scan for closed orphan PRs...")
    try:
        out = subprocess.run(["gh", "pr", "list", "--state", "closed", "--limit", "50",
                              "--json", "number,state,isMerged,author,headRefOid"],
                             capture_output=True, text=True, check=False).stdout
        prs = json.loads(out) if out.strip() else []
        for p in prs:
            author = (p.get("author") or {}).get("login", "")
            if author not in ("github-actions[bot]", "app/github-actions"):
                continue
            if p.get("isMerged"):
                continue
            n = p.get("number")
            head = p.get("headRefOid")
            if not head:
                continue
            # head not in main?
            if subprocess.run(["git", "merge-base", "--is-ancestor", head, "origin/main"],
                              capture_output=True).returncode != 0:
                print(f"fallback: detected closed unlanded PR #{n} (head {head[:7]} not in main)")
                recovers.append({"pr": n})
                if len(recovers) >= 3:
                    break
    except Exception as e:
        print(f"fallback scan failed: {e}")
    if not recovers:
        print("No recover actions; nothing to land.")
        sys.exit(0)

# Remove checkout credential injection so the PAT URL authenticates.
subprocess.run(["git", "config", "--local", "--unset-all",
                "http.https://github.com/.extraheader"], capture_output=True)
for cfg in subprocess.run(["git", "config", "--local", "--name-only",
                           "--get-regexp", r"^includeIf\.gitdir:.*\.path$"],
                          capture_output=True, text=True).stdout.split():
    subprocess.run(["git", "config", "--local", "--unset-all", cfg], capture_output=True)

def gh_comment(pr, body):
    env = os.environ.copy()
    env["GH_TOKEN"] = bot_token
    subprocess.run(["gh", "issue", "comment", str(pr), "--repo", repo, "-b", body],
                   check=False, env=env)

def merge_open_pr(pr):
    """Mae-directed merge of an OPEN approved PR via rebase (branch preserved)."""
    print(f"Mae directed merge of open approved PR #{pr} via rebase.")
    env = os.environ.copy()
    env["GH_TOKEN"] = pat
    rc = subprocess.run(["gh", "pr", "merge", str(pr), "--rebase", "--repo", repo],
                        capture_output=True, text=True, env=env)
    if rc.returncode == 0:
        print(f"Merged open PR #{pr} into main (rebase; branch preserved).")
        gh_comment(pr, "Merged into `main` by the Maintainer (rebase merge, PR branch preserved). Linked issues are auto-closed by GitHub on merge. -  Mae, the Maintainer")
        # Close any issues the PR body links with Closes/Fixes/Resolves #N (rule: Maintainer closes them).
        body = subprocess.run(["gh", "pr", "view", str(pr), "--repo", repo, "--json", "body", "--jq", ".body"],
                              capture_output=True, text=True, env={**os.environ, "GH_TOKEN": bot_token}).stdout or ""
        import re
        for m in re.findall(r"(?:Closes|Fixes|Resolves)\s+#(\d+)", body, re.IGNORECASE):
            subprocess.run(["gh", "issue", "close", m, "--repo", repo],
                          capture_output=True, text=True, env={**os.environ, "GH_TOKEN": bot_token})
            print(f"Closed linked issue #{m}.")
        subprocess.run(["git", "fetch", "origin", "main", "--quiet"], check=False)
        return True
    print(f"::error::gh pr merge #{pr} failed: {rc.stderr[:400]}")
    return False

for d in recovers:
    pr = d.get("pr") or d.get("target")
    if not pr:
        continue
    pr = int(pr)
    info = subprocess.run(["gh", "pr", "view", str(pr), "--repo", repo,
                           "--json", "state,title,headRefOid,headRefName,isMerged"],
                          capture_output=True, text=True, check=False).stdout
    try:
        meta = json.loads(info)
    except Exception:
        print(f"skip recover #{pr}: cannot read PR"); continue
    if meta.get("isMerged"):
        print(f"PR #{pr} already merged; nothing to land"); continue
    if meta.get("state") == "OPEN":
        # Mae directed a `recover`/`merge` on an open PR -> perform a normal rebase merge.
        merge_open_pr(pr)
        continue
    subprocess.run(["git", "fetch", push_url, f"pull/{pr}/head:refs/pull/{pr}/head"], check=False)
    head = f"refs/pull/{pr}/head"
    if subprocess.run(["git", "merge-base", "--is-ancestor", head, "origin/main"],
                      capture_output=True).returncode == 0:
        print(f"PR #{pr} head already in main; nothing to land")
        continue
    title = meta.get("title", f"PR #{pr}")
    ref = f"recover-{pr}"
    subprocess.run(["git", "fetch", "origin", "main", "--quiet"], check=False)
    subprocess.run(["git", "checkout", "-B", ref, "origin/main"], check=False)
    # Try merge with auto-resolve favoring PR (theirs) when possible
    rc = subprocess.run(["git", "merge", "--no-ff", "--allow-unrelated-histories", "-X", "theirs",
                         head, "-m", f"maintainer: land closed PR #{pr}: {title}"],
                        capture_output=True, text=True)
    if rc.returncode != 0:
        # If still conflicted, attempt manual resolve by taking PR version for conflicted files
        conflicted = subprocess.run(["git", "diff", "--name-only", "--diff-filter=U"],
                                    capture_output=True, text=True).stdout.splitlines()
        if conflicted:
            print(f"merge conflict on {len(conflicted)} files, auto-resolving with --theirs")
            for f in conflicted:
                subprocess.run(["git", "checkout", "--theirs", "--", f], check=False)
            subprocess.run(["git", "add", "-A"], check=False)
            rc2 = subprocess.run(["git", "-c", "user.name=Mae (Maintainer)",
                                  "-c", "user.email=github-actions[bot]@users.noreply.github.com",
                                  "commit", "-m", f"maintainer: land closed PR #{pr}: {title} (auto-resolved conflicts)"],
                                 capture_output=True, text=True)
            if rc2.returncode != 0:
                subprocess.run(["git", "merge", "--abort"], check=False)
                msg = (f"ALERT: could not auto-land closed PR #{pr} (merge conflict). "
                       f"Manual or follow-up resolution required.")
                gh_comment(pr, msg)
                print(msg); continue
        else:
            subprocess.run(["git", "merge", "--abort"], check=False)
            msg = (f"ALERT: could not auto-land closed PR #{pr} (merge conflict). "
                   f"Manual or follow-up resolution required.")
            gh_comment(pr, msg)
            print(msg); continue
    # Verify new tip descends from current main tip (orphan-main guard)
    current_main = subprocess.run(["git", "rev-parse", "origin/main"],
                                  capture_output=True, text=True).stdout.strip()
    if subprocess.run(["git", "merge-base", "--is-ancestor", current_main, "HEAD"],
                      capture_output=True).returncode != 0:
        print(f"ABORT: landing commit does not descend from current main {current_main[:7]}")
        subprocess.run(["git", "checkout", "-B", "main", "origin/main", "--quiet"], check=False)
        continue
    prc = subprocess.run(["git", "push", push_url, f"HEAD:main"], capture_output=True, text=True)
    if prc.returncode != 0:
        subprocess.run(["git", "fetch", "origin", "main", "--quiet"], check=False)
        subprocess.run(["git", "rebase", "origin/main", "--quiet"], check=False)
        # Re-check ancestry after rebase before second push
        current_main = subprocess.run(["git", "rev-parse", "origin/main"],
                                      capture_output=True, text=True).stdout.strip()
        if subprocess.run(["git", "merge-base", "--is-ancestor", current_main, "HEAD"],
                          capture_output=True).returncode != 0:
            print(f"ABORT: rebased landing does not descend from current main {current_main[:7]}")
            continue
        prc = subprocess.run(["git", "push", push_url, f"HEAD:main"], capture_output=True, text=True)
    if prc.returncode == 0:
        print(f"Landed closed PR #{pr} into main.")
        gh_comment(pr, "Recovered and landed into `main` by the Maintainer. -  Mae, the Maintainer")
        subprocess.run(["git", "fetch", "origin", "main", "--quiet"], check=False)
        subprocess.run(["git", "checkout", "-B", "main", "origin/main", "--quiet"], check=False)
    else:
        print(f"::error::Failed to push landing for PR #{pr}")
