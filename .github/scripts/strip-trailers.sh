#!/usr/bin/env bash
# Remove leaked owner attribution trailers from an agent PR branch.
# Called by the research workflow after the agent has pushed its work.

set -euo pipefail

issue_number="$(jq -r '.issue.number // empty' "${GITHUB_EVENT_PATH:?GITHUB_EVENT_PATH is required}" 2>/dev/null)"
if [ -z "$issue_number" ]; then
  echo "No issue number in the workflow event; refusing to rewrite history."
  exit 1
fi

if [ "$(jq -r '.issue.pull_request.html_url // empty' "$GITHUB_EVENT_PATH" 2>/dev/null)" = "" ]; then
  pr_number="$(gh pr list --repo "$GITHUB_REPOSITORY" --state open --json number,headRefName,createdAt \
    --jq '[.[] | select(.headRefName | startswith("opencode/issue'"$issue_number"'-"))] | sort_by(.createdAt) | last | .number // empty')"
else
  pr_number="$issue_number"
fi

if [ -z "$pr_number" ]; then
  echo "No open PR is associated with issue #$issue_number; nothing to sanitize."
  exit 0
fi

branch="$(gh pr view "$pr_number" --repo "$GITHUB_REPOSITORY" --json headRefName --jq '.headRefName')"
case "$branch" in
  opencode/issue"$issue_number"-*) ;;
  *)
    echo "Refusing to rewrite unexpected branch '$branch'."
    exit 1
    ;;
esac

git fetch origin "refs/heads/$branch:refs/remotes/origin/prbranch" --quiet
bad="$(git log --format=%B refs/remotes/origin/main..refs/remotes/origin/prbranch | grep -c '^Co-authored-by: Userfrom1995' || true)"
if [ "$bad" -eq 0 ]; then
  echo "No leaked owner trailers on $branch."
  exit 0
fi

echo "Stripping $bad leaked owner trailer(s) from $branch."
git checkout --detach refs/remotes/origin/prbranch --quiet
git filter-branch -f --msg-filter 'sed "/^Co-authored-by: Userfrom1995.*/d"' refs/remotes/origin/main..HEAD >/dev/null
git push --force origin "HEAD:refs/heads/$branch" --quiet
echo "Trailers stripped and branch updated: $branch"
