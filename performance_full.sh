#!/bin/bash

mkdir -p performance_logs
mkdir -p output

# Process JPEGs
for img in ./test_jpeg/*.{jpg,jpeg}; do
    [ -f "$img" ] || continue
    img_name=$(basename "$img")
    base_name="${img_name%.*}"
    out_file="./output/$img_name"
    log_file="./performance_logs/statsfor${base_name}.txt"

    perf stat -o "$log_file" python3 sobel.py "$img" "$out_file" -t 0
    echo "Processed $img → $out_file, stats → $log_file"
done

# Process PGMs
for img in ./test_pgm/*.pgm; do
    [ -f "$img" ] || continue
    img_name=$(basename "$img")
    base_name="${img_name%.*}"
    out_file="./output/$img_name"
    log_file="./performance_logs/statsfor${base_name}.txt"

    perf stat -o "$log_file" python3 sobel.py "$img" "$out_file" -t 0
    echo "Processed $img → $out_file, stats → $log_file"
done