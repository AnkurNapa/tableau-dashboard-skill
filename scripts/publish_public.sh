#!/bin/bash
# Copy the skill into the public repo without private files, scan it, commit it and push it.
# Usage: publish_public.sh "commit message"
# Prints the list of changed files, which feeds the email digest.
set -euo pipefail
SKILL="$HOME/.claude/skills/tableau-dashboard"
REPO="$HOME/Documents/tableau-dashboard-skill"
MSG="${1:-docs: update Tableau skill lessons}"

# cookbook.md summarises a copyrighted book, so it never leaves this Mac.
rsync -a --delete --exclude 'cookbook.md' --exclude '.DS_Store' \
  "$SKILL/references/" "$REPO/references/"
rsync -a "$SKILL/scripts/" "$REPO/scripts/"
rsync -a --delete "$SKILL/palettes/" "$REPO/palettes/"
# Public SKILL.md drops the private cookbook row.
grep -v 'references/cookbook.md' "$SKILL/SKILL.md" > "$REPO/SKILL.md"

# Strip the home folder from any absolute path.
find "$REPO" -type f \( -name '*.md' -o -name '*.sh' \) -not -path '*/.git/*' \
  -exec sed -i '' "s#/Users/$(whoami)/#~/#g" {} +

# Scans run alone; nothing is committed unless every one is clean.
cd "$REPO"
fail=0
if grep -rn ', and' --include='*.md' . | grep -v 'no ", and"'; then fail=1; fi
if grep -rnP '[\x{2013}\x{2014}\x{201C}\x{201D}\x{2018}\x{2019}]' --include='*.md' .; then fail=1; fi
if grep -rn "/Users/$(whoami)" . --exclude-dir=.git --exclude-dir=.gstack; then fail=1; fi
if grep -rniE 'napaankur|api[_-]?key *[:=]|token *[:=] *[A-Za-z0-9]{20,}' . --exclude-dir=.git --exclude-dir=.gstack --exclude=publish_public.sh; then fail=1; fi
if [ -e references/cookbook.md ]; then echo "cookbook.md leaked"; fail=1; fi
if [ "$fail" = 1 ]; then echo "SCAN FAILED: nothing committed"; exit 1; fi

git add .gitignore SKILL.md README.md references scripts palettes assets .github
if git diff --cached --quiet; then echo "NO CHANGES"; exit 0; fi
echo "CHANGED:"; git diff --cached --name-only
git commit -q -m "$MSG"
git push -q origin main
echo "PUSHED $(git rev-parse --short HEAD)"
