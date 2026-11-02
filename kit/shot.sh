#!/bin/bash
# usage: shot.sh <html-file> <scene> <beat> <out.png> [width height]
# Call with explicit args. In zsh, never loop with `set -- $var` (no word splitting).
W=${5:-1100}; H=${6:-1000}
rm -f "$4"
CH="/Applications/Google Chrome.app/Contents/MacOS/Google Chrome"
"$CH" --headless=new --disable-gpu --hide-scrollbars --user-data-dir=/tmp/chrome-ex-$$ --window-size=$W,$H --virtual-time-budget=3000 --screenshot="$4" "file://$1#s$2b$3" >/dev/null 2>&1 &
P=$!
for i in $(seq 1 40); do sleep 0.5; [ -s "$4" ] && sleep 1 && break; done
kill $P 2>/dev/null; pkill -f "user-data-dir=/tmp/chrome-ex-$$ " 2>/dev/null
ls -la "$4" | awk '{print $5, $9}'
