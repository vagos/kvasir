#!/bin/bash

set -euo pipefail

top=$(git rev-parse --show-toplevel)

input="$top/eval"
output="$top/results"
mkdir -p "$output"

# Evaluate each task
kvasir -vvv -i "$input"/math.js -q "$input"/query/to_haskell.pl -o "$output"/math.hs
