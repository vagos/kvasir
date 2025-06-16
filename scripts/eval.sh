#!/bin/bash

set -euo pipefail

top=$(git rev-parse --show-toplevel)

input="$top/eval"
output="$top/results"
mkdir -p "$output"

# Evaluate each task
kvasir -vvv -i "$input"/micro/math.js -q "$input"/query/to_haskell.pl -o "$output"/math.hs
kvasir -vvv -i "$input"/micro/Q_rsqrt.c -q "$input"/query/min_len.pl -o "$output"/Q_rsqrt_idiomatic.c
kvasir -vvv -i "$input"/npm/left-pad/index.js -q "$input"/query/io_same.pl -o "$output"/left-pad.js
