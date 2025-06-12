#!/bin/bash

# Create results directory if it doesn't exist
mkdir -p results

# Number of repetitions
repetitions=5

# Repeat the whole process
for ((run=1; run<=repetitions; run++))
do
        rm wn18/train_sat.txt
        echo "=== Run $run/$repetitions ==="

        echo "--- wn18 ---"

        # Define output and timestamp files for this dataset
        timestamp_file="results/timestamps_wn18.txt"
        output_file="results/output_wn18.txt"

        echo "=== Run $run/$repetitions ===" >> "$output_file"
        echo "Starting building (Run $run)..."  
        # Build phase
        start_time=$(date +%s)
        ./run.sh wn18/train.txt wn18/rules.txt wn18/train_sat.txt >> "$output_file" 2>&1
        end_time=$(date +%s)
        duration=$((end_time - start_time))
        echo "BUILD Run${run}: ${duration} seconds" >> "$timestamp_file"
        echo "Build phase took ${duration} seconds." >> "$output_file"

done

# Inference phase
echo "Starting inference (Run $run)..."
start_time=$(date +%s)
python3 compute_metrics.py wn18/test.txt wn18/train_sat.txt wn18/train.txt >> "$output_file" 2>&1
end_time=$(date +%s)
duration=$((end_time - start_time))
echo "INFERENCE Run${run}: ${duration} seconds" >> "$timestamp_file"
echo "Inference phase took ${duration} seconds." >> "$output_file"



