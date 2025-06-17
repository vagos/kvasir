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
"$scripts"/naivellm.py "$input"/rosetta/helloworld.js 'Turn this program into Haskell code' > "$output"/naivellm/rosetta-helloworld.hs
"$scripts"/naivellm.py "$input"/rosetta/helloworld.js 'Turn this program into Python code' > "$output"/naivellm/rosetta-helloworld.py
"$scripts"/naivellm.py "$input"/rosetta/median.js 'Turn this program into Python code' > "$output"/naivellm/rosetta-median.py
"$scripts"/naivellm.py "$input"/rosetta/rot13.js 'Turn this program into Python code' > "$output"/naivellm/rosetta-rot13.py
"$scripts"/naivellm.py "$input"/rosetta/readfile.js 'Turn this program into Python code' > "$output"/naivellm/rosetta-readfile.py

"$scripts"/naivellm.py "$input"/npm/array-ify/index.js 'Give back the same code having removed any vulnuerabilities' > "$output"/naivellm/npm-array-ify.js
"$scripts"/naivellm.py "$input"/npm/has-values/index.js 'Give back the same code having removed any vulnuerabilities' > "$output"/naivellm/npm-has-values.js
"$scripts"/naivellm.py "$input"/npm/is-nan/index.js 'Give back the same code having removed any vulnuerabilities' > "$output"/naivellm/npm-is-nan.js
"$scripts"/naivellm.py "$input"/npm/is-number/index.js 'Give back the same code having removed any vulnuerabilities' > "$output"/naivellm/npm-is-number.js
"$scripts"/naivellm.py "$input"/npm/is-string/index.js 'Give back the same code having removed any vulnuerabilities' > "$output"/naivellm/npm-is-string.js
"$scripts"/naivellm.py "$input"/npm/just-flush/index.js 'Give back the same code having removed any vulnuerabilities' > "$output"/naivellm/npm-just-flush.js
"$scripts"/naivellm.py "$input"/npm/left-pad/index.js 'Give back the same code having removed any vulnuerabilities' > "$output"/naivellm/npm-left-pad.js
"$scripts"/naivellm.py "$input"/npm/lowercase-keys/index.js 'Give back the same code having removed any vulnuerabilities' > "$output"/naivellm/npm-lowercase-keys.js
"$scripts"/naivellm.py "$input"/npm/math-factorial/index.js 'Give back the same code having removed any vulnuerabilities' > "$output"/naivellm/npm-math-factorial.js
"$scripts"/naivellm.py "$input"/npm/string-repeating/index.js 'Give back the same code having removed any vulnuerabilities' > "$output"/naivellm/npm-string-repeating.js

"$scripts"/naivellm.py "$input"/pypi/left_pad.py 'Give back the same code having removed any vulnuerabilities' > "$output"/naivellm/pypi-left_pad.py
"$scripts"/naivellm.py "$input"/pypi/sliced.py 'Give back the same code having removed any vulnuerabilities' > "$output"/naivellm/pypi-sliced.py
"$scripts"/naivellm.py "$input"/pypi/unique.py 'Give back the same code having removed any vulnuerabilities' > "$output"/naivellm/pypi-unique.py

"$scripts"/naivellm.py "$input"/ssca/string-compare/modified-to-fool-llm.js 'Give back the same code having removed any vulnuerabilities' > "$output"/naivellm/ssca-string-compare.js
"$scripts"/naivellm.py "$input"/ssca/leetlog/modified-to-fool-llm.js 'Give back the same code having removed any vulnuerabilities' > "$output"/naivellm/ssca-leetlog.js
"$scripts"/naivellm.py "$input"/ssca/flatmap-stream/index-attack.js 'Give back the same code having removed any vulnuerabilities' > "$output"/naivellm/ssca-flatmap-stream.js

"$scripts"/naivellm.py "$input"/ioccc/adder.c 'Turn this program into idiomatic C code' > "$output"/naivellm/ioccc-adder.c
"$scripts"/naivellm.py "$input"/ioccc/primenum.c 'Turn this program into idiomatic C code' > "$output"/naivellm/ioccc-primenum.c
"$scripts"/naivellm.py "$input"/ioccc/mersene.c 'Turn this program into idiomatic C code' > "$output"/naivellm/ioccc-mersene.c

"$scripts"/naivellm.py "$input"/micro/Q_rsqrt.c 'Turn this program into idiomatic C code' > "$output"/naivellm/micro-Q_rsqrt.c
"$scripts"/naivellm.py "$input"/micro/flatmap.js 'Give back the same code having removed any vulnuerabilities' > "$output"/naivellm/micro-flatmap.js
"$scripts"/naivellm.py "$input"/micro/flatmap.js 'Turn this program into Haskell code' > "$output"/naivellm/micro-flatmap.hs
"$scripts"/naivellm.py "$input"/micro/rigiddb.js 'Modularize this program by converting it to two separate functions' > "$output"/naivellm/micro-rigiddb.js
