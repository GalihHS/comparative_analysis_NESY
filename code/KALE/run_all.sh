
#!/bin/bash

# Create results directory if it doesn't exist
mkdir -p results

# Number of repetitions
repetitions=5


for ((run=1; run<=repetitions; run++))
do
    echo "=== Run $run/$repetitions ==="

    echo "--- family_small with normal ontology ---"
    timestamp_file="results/timestamps_small_normal.txt"
    output_file="results/output_small_normal.txt"
    echo "=== Run $run/$repetitions ===" >> "$output_file"

    # Learn phase
    echo "Starting learn (Run $run)..."
    start_time=$(date +%s)
    java -jar KALE.jar -train datasets/family_small/train.txt -valid datasets/family_small/valid.txt -test datasets/family_small/test.txt -rule datasets/family_small/groundings.txt -m 12 -n 2411 -w 0.1 -k 80 -d 0.3 -ge 0.1 -gr 0.1 -# 1500 -skip 50 >> "$output_file" 2>&1
    end_time=$(date +%s)
    duration=$((end_time - start_time))
    echo "LEARN Run${run}: ${duration} seconds" >> "$timestamp_file"
    echo "Learn phase took ${duration} seconds." >> "$output_file"

    # Inference phase
    echo "Starting Inference (Run $run)..."
    start_time=$(date +%s)
    java -cp src test.Eval_LinkPrediction 2411 12 80 MatrixE-k80-d0.3-ge0.1-gr0.1-w0.1.best MatrixR-k80-d0.3-ge0.1-gr0.1-w0.1.best datasets/family_small/train.txt datasets/family_small/valid.txt datasets/family_small/test.txt none >> "$output_file" 2>&1
    end_time=$(date +%s)
    duration=$((end_time - start_time))
    echo "INFERENCE Run${run}: ${duration} seconds" >> "$timestamp_file"
    echo "Inference phase took ${duration} seconds." >> "$output_file"

    rm MatrixE-k80-d0.3-ge0.1-gr0.1-w0.1.best
    rm MatrixR-k80-d0.3-ge0.1-gr0.1-w0.1.best

done





for ((run=1; run<=repetitions; run++))
do
    echo "=== Run $run/$repetitions ==="

    echo "--- family_medium ---"
    timestamp_file="results/timestamps_medium.txt"
    output_file="results/output_medium.txt"
    echo "=== Run $run/$repetitions ===" >> "$output_file"

    # Learn phase
    echo "Starting learn (Run $run)..."
    start_time=$(date +%s)
    java -jar KALE.jar -train datasets/family_medium/train.txt -valid datasets/family_medium/valid.txt -test datasets/family_medium/test.txt -rule datasets/family_medium/groundings.txt -m 12 -n 2968 -w 0.1 -k 80 -d 0.3 -ge 0.1 -gr 0.1 -# 1500 -skip 50 >> "$output_file" 2>&1
    end_time=$(date +%s)
    duration=$((end_time - start_time))
    echo "LEARN Run${run}: ${duration} seconds" >> "$timestamp_file"
    echo "Learn phase took ${duration} seconds." >> "$output_file"

    # Inference phase
    echo "Starting Inference (Run $run)..."
    start_time=$(date +%s)
    java -cp src test.Eval_LinkPrediction 2968 12 80 MatrixE-k80-d0.3-ge0.1-gr0.1-w0.1.best MatrixR-k80-d0.3-ge0.1-gr0.1-w0.1.best datasets/family_medium/train.txt datasets/family_medium/valid.txt datasets/family_medium/test.txt none >> "$output_file" 2>&1
    end_time=$(date +%s)
    duration=$((end_time - start_time))
    echo "INFERENCE Run${run}: ${duration} seconds" >> "$timestamp_file"
    echo "Inference phase took ${duration} seconds." >> "$output_file"
done








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

        # Learn phase
        echo "Starting learning (Run $run)..."
        start_time=$(date +%s)
        java -jar KALE.jar -train datasets/family_small/train.txt -valid datasets/family_small/valid.txt -test datasets/family_small/test.txt -rule datasets/family_small/groundings_${perc}%.txt -m 12 -n 2411 -w 0.1 -k 80 -d 0.3 -ge 0.1 -gr 0.1 -# 1500 -skip 50 >> "$output_file" 2>&1
        end_time=$(date +%s)
        duration=$((end_time - start_time))
        echo "BUILD Run${run}: ${duration} seconds" >> "$timestamp_file"
        echo "Build phase took ${duration} seconds." >> "$output_file"

        # Inference phase
        echo "Starting inference (Run $run)..."
        start_time=$(date +%s)
        java -cp src test.Eval_LinkPrediction 2411 12 80 MatrixE-k80-d0.3-ge0.1-gr0.1-w0.1.best MatrixR-k80-d0.3-ge0.1-gr0.1-w0.1.best datasets/family_small/train.txt datasets/family_small/valid.txt datasets/family_small/test.txt none >> "$output_file" 2>&1
        end_time=$(date +%s)
        duration=$((end_time - start_time))
        echo "INFERENCE Run${run}: ${duration} seconds" >> "$timestamp_file"
        echo "Inference phase took ${duration} seconds." >> "$output_file"

        rm MatrixE-k80-d0.3-ge0.1-gr0.1-w0.1.best
        rm MatrixR-k80-d0.3-ge0.1-gr0.1-w0.1.best

    done
done






for perc in "${percentages[@]}"
do

    # Repeat the whole process
    for ((run=1; run<=repetitions; run++))
    do
        echo "=== Run $run/$repetitions for ${perc}% wrong rules ==="

        echo "--- family_small with ${perc}% wrong rules ---"

        # Define output and timestamp files for this dataset
        timestamp_file="results/timestamps_small_${perc}%_wrong.txt"
        output_file="results/output_small_${perc}%_wrong.txt"

        echo "=== Run $run/$repetitions ===" >> "$output_file"

        # Learn phase
        echo "Starting learning (Run $run)..."  
        start_time=$(date +%s)
        java -jar KALE.jar -train datasets/family_small/train.txt -valid datasets/family_small/valid.txt -test datasets/family_small/test.txt -rule datasets/family_small/groundings_${perc}%_wrong.txt -m 12 -n 2411 -w 0.1 -k 80 -d 0.3 -ge 0.1 -gr 0.1 -# 1500 -skip 50 >> "$output_file" 2>&1
        end_time=$(date +%s)
        duration=$((end_time - start_time))
        echo "BUILD Run${run}: ${duration} seconds" >> "$timestamp_file"
        echo "Build phase took ${duration} seconds." >> "$output_file"

        # Inference phase
        echo "Starting inference (Run $run)..."
        start_time=$(date +%s)
        java -cp src test.Eval_LinkPrediction 2411 12 80 MatrixE-k80-d0.3-ge0.1-gr0.1-w0.1.best MatrixR-k80-d0.3-ge0.1-gr0.1-w0.1.best datasets/family_small/train.txt datasets/family_small/valid.txt datasets/family_small/test.txt none >> "$output_file" 2>&1
        end_time=$(date +%s)
        duration=$((end_time - start_time))
        echo "INFERENCE Run${run}: ${duration} seconds" >> "$timestamp_file"
        echo "Inference phase took ${duration} seconds." >> "$output_file"

        rm MatrixE-k80-d0.3-ge0.1-gr0.1-w0.1.best
        rm MatrixR-k80-d0.3-ge0.1-gr0.1-w0.1.best

    done
done





for ((run=1; run<=repetitions; run++))
do
    echo "=== Run $run/$repetitions ==="

    echo "--- wn18 ---"
    timestamp_file="results/timestamps_wn18.txt"
    output_file="results/output_wn18.txt"
    echo "=== Run $run/$repetitions ===" >> "$output_file"

    # Learn phase
    echo "Starting learn (Run $run)..."
    start_time=$(date +%s)
    java -jar KALE.jar -train datasets/wn18/train.txt -valid datasets/wn18/valid.txt -test datasets/wn18/test.txt -rule datasets/wn18/groundings.txt -m 18 -n 40559 -w 0.1 -k 50 -d 0.2 -ge 0.1 -gr 0.1 -# 1000 -skip 50 >> "$output_file" 2>&1
    end_time=$(date +%s)
    duration=$((end_time - start_time))
    echo "LEARN Run${run}: ${duration} seconds" >> "$timestamp_file"
    echo "Learn phase took ${duration} seconds." >> "$output_file"

    # Inference phase
    echo "Starting Inference (Run $run)..."
    start_time=$(date +%s)
    java -cp src test.Eval_LinkPrediction 40559 18 50 MatrixE-k50-d0.2-ge0.1-gr0.1-w0.1.best MatrixR-k50-d0.2-ge0.1-gr0.1-w0.1.best datasets/wn18/train.txt datasets/wn18/valid.txt datasets/wn18/test.txt none >> "$output_file" 2>&1
    end_time=$(date +%s)
    duration=$((end_time - start_time))
    echo "INFERENCE Run${run}: ${duration} seconds" >> "$timestamp_file"
    echo "Inference phase took ${duration} seconds." >> "$output_file"

    rm MatrixE-k80-d0.3-ge0.1-gr0.1-w0.1.best
    rm MatrixR-k80-d0.3-ge0.1-gr0.1-w0.1.best

done



echo "All experiments completed. See 'results/' directory for timestamps and outputs."

