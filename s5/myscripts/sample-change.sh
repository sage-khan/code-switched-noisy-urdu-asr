#!/bin/bash

# Will find all wav files in $source directory
# Process them and mirror the tree architecture in $output
source="N64"
output="N64-out"
mkdir -p $output

find $source -type f -name "*.wav" -print | while IFS= read -r file;
do
    out=${file/$source/$output}
    mkdir -p "$(dirname "${out}")"

    sox -S "$file" -r 44100 -c 1 "$out"
done
