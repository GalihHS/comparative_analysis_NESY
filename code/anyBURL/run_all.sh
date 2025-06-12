#!/bin/bash

# Create results directory if it doesn't exist
mkdir -p results

# Number of repetitions
repetitions=5

# List of datasets
datasets=("family_small" "family_medium" "wn18" "fb15k-237")

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
        java -Xmx12G -cp AnyBURL-23-1.jar de.unima.ki.anyburl.Learn "config-learn_${dataset}.properties" >> "$output_file" 2>&1
        end_time=$(date +%s)
        duration=$((end_time - start_time))
        echo "LEARN Run${run}: ${duration} seconds" >> "$timestamp_file"
        echo "Learn phase took ${duration} seconds." >> "$output_file"

        # Apply phase
        echo "Starting apply for $dataset (Run $run)..."
        start_time=$(date +%s)
        java -Xmx12G -cp AnyBURL-23-1.jar de.unima.ki.anyburl.Apply "config-apply_${dataset}.properties" >> "$output_file" 2>&1
        end_time=$(date +%s)
        duration=$((end_time - start_time))
        echo "APPLY Run${run}: ${duration} seconds" >> "$timestamp_file"
        echo "Apply phase took ${duration} seconds." >> "$output_file"

        # Eval phase
        echo "Starting eval for $dataset (Run $run)..."
        java -Xmx12G -cp AnyBURL-23-1.jar de.unima.ki.anyburl.Eval "config-eval_${dataset}.properties" >> "$output_file" 2>&1

    done
done

echo "All experiments completed. See 'results/' directory for timestamps and outputs."
