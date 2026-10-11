#!/usr/bin/env bash
# Rebuild the demo from a LitViz checkout: the real frontend, in fixture mode, served under /litviz-demo/.
#   scripts/build.sh <path to LitViz checkout>
# The only change to the app: the Idea Landscape is not disabled in fixture mode (the shim serves it).
set -euo pipefail
SRC=$(cd "$1" && pwd)
OUT=$(cd "$(dirname "$0")/.." && pwd)
WORK=$(mktemp -d)
trap 'rm -rf "$WORK"' EXIT
cp -R "$SRC/frontend" "$WORK/frontend"
cd "$WORK/frontend"
sed -i.bak 's|<LandscapeView graph={graph} papers={papers} visible={visible} theme={theme} offline={fixture}|<LandscapeView graph={graph} papers={papers} visible={visible} theme={theme} offline={false}|' src/App.tsx
grep -q 'theme={theme} offline={false}' src/App.tsx || { echo "LandscapeView patch did not apply" >&2; exit 1; }
[ -d node_modules ] || npm ci --no-audit --no-fund
VITE_USE_FIXTURE=1 npx vite build --base=/litviz-demo/ --outDir "$WORK/dist"
rm -rf "$OUT/assets" "$OUT/demo"
mkdir -p "$OUT/demo"
cp -R "$WORK/dist/assets" "$OUT/assets"
python3 "$OUT/scripts/make_landscape.py" "$SRC/frontend/fixtures/mock_graph.json" "$OUT/demo/landscape.json"
cp "$OUT/shim/demo-shim.js" "$OUT/demo/demo-shim.js"
# the shim must run before the app's module script
sed 's|<head>|<head>\n    <script src="/litviz-demo/demo/demo-shim.js"></script>|' "$WORK/dist/index.html" > "$OUT/index.html"
echo "built into $OUT"
