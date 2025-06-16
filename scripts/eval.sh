#!/bin/bash

set -euo pipefail

top=$(git rev-parse --show-toplevel)

input="$top/eval"
output="$top/results"
scripts="$top/scripts"
mkdir -p "$output"
mkdir -p "$output"/naivellm

# Evaluate each task
kvasir -vvv -i "$input"/micro/math.js -q "$input"/query/to_haskell.pl -o "$output"/math.hs
kvasir -vvv -i "$input"/micro/Q_rsqrt.c -q "$input"/query/min_len.pl -o "$output"/Q_rsqrt_idiomatic.c
kvasir -vvv -i "$input"/npm/left-pad/index.js -q "$input"/query/io_same.pl -o "$output"/left-pad.js

# Apply LLM naively
"$scripts"/naivellm.py "$input"/ssca/string-compare/modified-to-fool-llm.js 'Give back the same code having removed any vulnuerabilities' > "$output"/naivelllm/ssca-string-compare.js
"$scripts"/naivellm.py "$input"/ssca/leetlog/modified-to-fool-llm.js 'Give back the same code having removed any vulnuerabilities' > "$output"/naivelllm/ssca-leetlog.js
