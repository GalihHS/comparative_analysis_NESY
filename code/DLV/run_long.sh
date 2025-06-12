#!/bin/bash

# Create results directory if it doesn't exist
mkdir -p results


echo "--- family_small with 80% wrong rules ---"

# Define output and timestamp files for this dataset
timestamp_file="results/timestamps_small_80%_wrong.txt"
output_file="results/output_small_80%_wrong.txt"

echo "=== Run 1/1 ===" >> "$output_file"
echo "Starting building (Run 1)..."	
# Build phase
start_time=$(date +%s)
timeout 24h ./run.sh family_small/train.txt family_small/rules_80%_wrong.txt family_small/train_sat_wrong_80%.txt >> "$output_file" 2>&1
end_time=$(date +%s)
duration=$((end_time - start_time))
echo "BUILD Run1: ${duration} seconds" >> "$timestamp_file"
echo "Build phase took ${duration} seconds." >> "$output_file"



echo "=== Run fb ==="

# Define output and timestamp files for this dataset
timestamp_file="results/timestamps_fb15k-237.txt"
output_file="results/output_fb15k-237.txt"

echo "--- Dataset: fb15k-237 ---" >> "$output_file"

# Build phase
start_time=$(date +%s)
timeout 24h ./run.sh fb15k-237/train.txt fb15k-237/rules.txt fb15k-237/train_sat.txt >> "$output_file" 2>&1
end_time=$(date +%s)
duration=$((end_time - start_time))
echo "BUILD : ${duration} seconds" >> "$timestamp_file"
echo "Build phase took ${duration} seconds." >> "$output_file"



echo "finished"
