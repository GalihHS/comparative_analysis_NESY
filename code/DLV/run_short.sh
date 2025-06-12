#!/bin/bash

# Create results directory if it doesn't exist
mkdir -p results

# Number of repetitions
repetitions=5


# List of percentages
percentages=("20" "40" "60" "80")

for perc in "${percentages[@]}"
do

        # Repeat the whole process
        for ((run=1; run<=repetitions; run++))
        do
                echo "=== Run $run/$repetitions for ${perc}% rules ==="

                echo "--- family_small with ${perc}% rules ---"

                # Define output and timestamp files for this dataset
                timestamp_file="results/timestamps_small_${perc}%.txt"
                output_file="results/output_small_${perc}%.txt"

                echo "=== Run $run/$repetitions ===" >> "$output_file"
                echo "Starting building (Run $run)..."  
                # Build phase
                start_time=$(date +%s)
                ./run.sh family_small/train.txt family_small/rules_${perc}%.txt family_small/train_sat_less_${perc}%.txt >> "$output_file" 2>&1
                end_time=$(date +%s)
                duration=$((end_time - start_time))
                echo "BUILD Run${run}: ${duration} seconds" >> "$timestamp_file"
                echo "Build phase took ${duration} seconds." >> "$output_file"

                # Inference phase
                echo "Starting inference (Run $run)..."
                start_time=$(date +%s)
                python3 compute_metrics.py family_small/test.txt family_small/train_sat_less_${perc}%.txt family_small/train.txt >> "$output_file" 2>&1
                end_time=$(date +%s)
                duration=$((end_time - start_time))
                echo "INFERENCE Run${run}: ${duration} seconds" >> "$timestamp_file"
                echo "Inference phase took ${duration} seconds." >> "$output_file"

                rm family_small/train_sat_less_${perc}%.txt

        done
done







# List of datasets
datasets=("family_small" "family_medium")

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


        # Build phase
        echo "Starting building for $dataset (Run $run)..."
        start_time=$(date +%s)
        ./run.sh ${dataset}/train.txt ${dataset}/rules.txt ${dataset}/train_sat.txt >> "$output_file" 2>&1
        end_time=$(date +%s)
        duration=$((end_time - start_time))
        echo "BUILD Run${run}: ${duration} seconds" >> "$timestamp_file"
        echo "Build phase took ${duration} seconds." >> "$output_file"

        # Inference phase
        echo "Starting inference for $dataset (Run $run)..."
        start_time=$(date +%s)
        python3 compute_metrics.py ${dataset}/test.txt ${dataset}/train_sat.txt ${dataset}/train.txt >> "$output_file" 2>&1
        end_time=$(date +%s)
        duration=$((end_time - start_time))
        echo "INFERENCE Run${run}: ${duration} seconds" >> "$timestamp_file"
        echo "Inference phase took ${duration} seconds." >> "$output_file"

        rm ${dataset}/train_sat.txt 

    done
done


echo "finished"
