
#!/bin/bash

# Create results directory if it doesn't exist
mkdir -p results

echo "--- fb15k-237 ---"
timestamp_file="results/timestamps_fb15k-237.txt"
output_file="results/output_fb15k-237.txt"
echo "=== Run1/1 ===" >> "$output_file"

# Learn phase
echo "Starting learn (Run 1)..."
start_time=$(date +%s)
timeout 40h java -jar KALE.jar -train datasets/fb15k/train.txt -valid datasets/fb15k/valid.txt -test datasets/fb15k/test.txt -rule datasets/fb15k/groundings.txt -m 237 -n 14505 -w 0.1 -k 120 -d 0.3 -ge 0.1 -gr 0.1 -# 1000 -skip 50 >> "$output_file" 2>&1
end_time=$(date +%s)
duration=$((end_time - start_time))
echo "LEARN Run 1: ${duration} seconds" >> "$timestamp_file"
echo "Learn phase took ${duration} seconds." >> "$output_file"

# Inference phase
echo "Starting Inference (Run 1)..."
start_time=$(date +%s)
java -cp src test.Eval_LinkPrediction 14505 237 120 MatrixE-k120-d0,3-ge0,1-gr0,1-w0,1.best MatrixR-k120-d0,3-ge0,1-gr0,1-w0,1.best datasets/fb15k/train.txt datasets/fb15k/valid.txt datasets/fb15k/test.txt none >> "$output_file" 2>&1
end_time=$(date +%s)
duration=$((end_time - start_time))
echo "INFERENCE Run 1: ${duration} seconds" >> "$timestamp_file"
echo "Inference phase took ${duration} seconds." >> "$output_file"


echo "All experiments completed. See 'results/' directory for timestamps and outputs."

