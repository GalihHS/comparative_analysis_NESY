
#!/bin/bash

# Create results directory if it doesn't exist
mkdir -p results
rm -rf record

echo "=== Run $run/$repetitions ==="

echo "--- fb15k-237 ---"
timestamp_file="results/timestamps_fb15k-237.txt"
output_file="results/output_fb15k-237.txt"
echo "=== Run $run/$repetitions ===" >> "$output_file"

start_time=$(date +%s)
python3 run.py fb15k 0 family_fb15k_model TransE 8 0.0 0.2 >> "$output_file" 2>&1
end_time=$(date +%s)
duration=$((end_time - start_time))
echo "LEARN Run${run}: ${duration} seconds" >> "$timestamp_file"
echo "Learn phase took ${duration} seconds." >> "$output_file"



echo "All experiments completed. See 'results/' directory for timestamps and outputs."

