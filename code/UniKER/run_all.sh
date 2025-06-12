
#!/bin/bash

# Create results directory if it doesn't exist
mkdir -p results

# Number of repetitions
repetitions=5



for ((run=1; run<=repetitions; run++))
do
    rm -rf record
    cp data/family_small/normal_rules.txt data/family_small/MLN_rule.txt
    echo "=== Run $run/$repetitions ==="

    echo "--- family_small ---"
    timestamp_file="results/timestamps_small.txt"
    output_file="results/output_small.txt"
    echo "=== Run $run/$repetitions ===" >> "$output_file"

    start_time=$(date +%s)
    python3 run.py family_small -1 family_small_model TransE 8 0.0 0.2 >> "$output_file" 2>&1
    end_time=$(date +%s)
    duration=$((end_time - start_time))
    echo "LEARN Run${run}: ${duration} seconds" >> "$timestamp_file"
    echo "Learn phase took ${duration} seconds." >> "$output_file"
done



for ((run=1; run<=repetitions; run++))
do
    rm -rf record	
    echo "=== Run $run/$repetitions ==="

    echo "--- family_medium ---"
    timestamp_file="results/timestamps_medium.txt"
    output_file="results/output_medium.txt"
    echo "=== Run $run/$repetitions ===" >> "$output_file"

    start_time=$(date +%s)
    python3 run.py family_medium -1 family_medium_model TransE 8 0.0 0.2 >> "$output_file" 2>&1
    end_time=$(date +%s)
    duration=$((end_time - start_time))
    echo "LEARN Run${run}: ${duration} seconds" >> "$timestamp_file"
    echo "Learn phase took ${duration} seconds." >> "$output_file"
done




for ((run=1; run<=repetitions; run++))
do
    rm -rf record
    echo "=== Run $run/$repetitions ==="

    echo "--- wn18 ---"
    timestamp_file="results/timestamps_wn18.txt"
    output_file="results/output_wn18.txt"
    echo "=== Run $run/$repetitions ===" >> "$output_file"

    start_time=$(date +%s)
    python3 run.py wn18 -1 family_wn18_model TransE 8 0.0 0.2 >> "$output_file" 2>&1
    end_time=$(date +%s)
    duration=$((end_time - start_time))
    echo "LEARN Run${run}: ${duration} seconds" >> "$timestamp_file"
    echo "Learn phase took ${duration} seconds." >> "$output_file"
done




# List of percentages
percentages=("20" "40" "60" "80")

for perc in "${percentages[@]}"
do

        cp data/family_small/MLN_rule_${perc}%.txt data/family_small/MLN_rule.txt
        for ((run=1; run<=repetitions; run++))
        do
		rm -rf record
                echo "=== Run $run/$repetitions for ${perc}% rules ==="

                echo "--- family_small with ${perc}% rules ---"
                timestamp_file="results/timestamps_small_${perc}%.txt"
                output_file="results/output_small_${perc}%.txt"
                echo "=== Run $run/$repetitions ===" >> "$output_file"

                start_time=$(date +%s)
                python3 run.py family_small -1 family_small_model TransE 8 0.0 0.2 >> "$output_file" 2>&1
                end_time=$(date +%s)
                duration=$((end_time - start_time))
                echo "LEARN Run${run}: ${duration} seconds" >> "$timestamp_file"
                echo "Learn phase took ${duration} seconds." >> "$output_file"
        done
done

percentages=("20" "40" "60" "80")

for perc in "${percentages[@]}"
do
        cp data/family_small/MLN_rule_${perc}%_wrong.txt data/family_small/MLN_rule.txt
        for ((run=1; run<=repetitions; run++))
        do
		rm -rf record
                echo "=== Run $run/$repetitions for ${perc}% wrong rules ==="

                echo "--- family_small with ${perc}% wrong rules ---"
                timestamp_file="results/timestamps_small_${perc}%_wrong.txt"
                output_file="results/output_small_${perc}%_wrong.txt"
                echo "=== Run $run/$repetitions ===" >> "$output_file"

                start_time=$(date +%s)
                python3 run.py family_small -1 family_small_model TransE 8 0.0 0.2 >> "$output_file" 2>&1
                end_time=$(date +%s)
                duration=$((end_time - start_time))
                echo "LEARN Run${run}: ${duration} seconds" >> "$timestamp_file"
                echo "Learn phase took ${duration} seconds." >> "$output_file"
        done
done



echo "All experiments completed. See 'results/' directory for timestamps and outputs."

