#!/bin/bash

# Create results directory if it doesn't exist
mkdir -p results

# Number of repetitions
repetitions=5

# List of datasets
datasets=("family_small" "family_medium" "fb15k-237" "wn18")

# Repeat the whole process
for ((run=1; run<=repetitions; run++))
do
    echo "=== Run $run/$repetitions ==="
    
    for dataset in "${datasets[@]}"
    do
        echo "--- Dataset: $dataset ---"

        # Define output and timestamp files for this dataset
        timestamp_file="results/timestamps_${dataset}.txt"
        output_file="results/output_${dataset}.txt"

        echo "=== Run $run/$repetitions ===" >> "$output_file"
        echo "--- Dataset: $dataset ---" >> "$output_file"

        # Learn phase
        echo "Starting learn for $dataset (Run $run)..."
        start_time=$(date +%s)
        python3 KGE_Family.py conf_kge.json $dataset >> "$output_file" 2>&1
        end_time=$(date +%s)
        duration=$((end_time - start_time))
        echo "LEARN Run${run}: ${duration} seconds" >> "$timestamp_file"
        echo "Learn phase took ${duration} seconds." >> "$output_file"
	
	mkdir -p results/BoxE/$dataset/
	mkdir -p results/RotatE/$dataset/
	mkdir -p results/TransE/$dataset/
	mv KGE_results/$dataset/BoxE/results.json results/BoxE/$dataset/results_$run.json
        mv KGE_results/$dataset/RotatE/results.json results/RotatE/$dataset/results_$run.json
        mv KGE_results/$dataset/TransE/results.json results/TransE/$dataset/results_$run.json
        
    done
done

echo "All experiments completed. See 'results/' directory for timestamps and outputs."
