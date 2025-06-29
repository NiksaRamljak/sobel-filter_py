#!/bin/bash

mkdir -p performance_logs
mkdir -p output

# Process JPEGs
for img in ./test_jpeg/*.{jpg,jpeg}; do
    img_name=$(basename "$img" .${img##*.})
    log_file="./performance_logs/statsfor${img_name}-one.txt"
    perf stat -r 5 -o "$log_file" python3 sobel.py "$img" "./output/${img_name}-one.jpg" -t 1
    echo "Processed $img, stats saved to $log_file"
done

for img in ./test_jpeg/*.{jpg,jpeg}; do
    img_name=$(basename "$img" .${img##*.})
    log_file="./performance_logs/statsfor${img_name}.txt"
    perf stat -r 5 -o "$log_file" python3 sobel.py "$img" "./output/${img_name}.jpg"
    echo "Processed $img, stats saved to $log_file"
done

# Process PGMs
for img in ./test_pgm/*.pgm; do
    img_name=$(basename "$img" .pgm)
    log_file="./performance_logs/statsfor${img_name}-one.txt"
    perf stat -r 5 -o "$log_file" python3 sobel.py "$img" "./output/${img_name}-one.pgm" -t 1
    echo "Processed $img, stats saved to $log_file"
done
for img in ./test_pgm/*.pgm; do
    img_name=$(basename "$img" .pgm)
    log_file="./performance_logs/statsfor${img_name}.txt"
    perf stat -r 5 -o "$log_file" python3 sobel.py "$img" "./output/${img_name}.pgm"
    echo "Processed $img, stats saved to $log_file"
done
