#!/bin/bash

mkdir -p performance_logs
mkdir -p output

# Process PGMs
for img in ./test_pgm/*.pgm; do
    [ -f "$img" ] || continue
    img_name=$(basename "$img" .pgm)

    out_file="./output/${img_name}-pure.pgm"
    log_file="./performance_logs/statsfor${img_name}-pure.txt"

    perf stat -o "$log_file" python3 sobel_pure.py "$img" "$out_file"
    echo "Processed $img → $out_file, stats → $log_file"
done
