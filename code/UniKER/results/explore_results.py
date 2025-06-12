
hits_1 = []
hits_3 = []
hits_10 = []
MRR = []
testing_time = []
training_time = []

import sys
import statistics
from datetime import datetime

def time_difference_in_seconds(start_time: str, end_time: str) -> float:
    start_dt = datetime.strptime(start_time.strip(), '%Y-%m-%d %H:%M:%S,%f')
    end_dt = datetime.strptime(end_time.strip(), '%Y-%m-%d %H:%M:%S,%f')
    delta = end_dt - start_dt
    return delta.total_seconds()


# Check if filename is passed
if len(sys.argv) < 2:
    print("Usage: python py_file.py <input_dir>")
    sys.exit(1)

filename = sys.argv[1]

with open(filename, "r") as file:
    lines = file.readlines()


found_metrics = False
found_time = False
found_test_time = False
start_time = ""
end_time = ""
end_test_time = ""
i = len(lines) - 1
while i >= 0:
    
    line = lines[i].strip()
    parts = line.split()

    if len(parts) < 2:
        i -= 1
        continue

    if parts[1] == "Run":
        training_time.append(time_difference_in_seconds(start_time, end_time))
        found_metrics = False
        found_time = False
        found_test_time = False
        start_time = ""
        end_time = ""

    if len(parts) < 3:
        i -= 1
        continue

    if parts[2] == "INFO":
        start_time = parts[0] + " " + parts[1]
        if not found_time:
            end_time = parts[0] + " " + parts[1]
            found_time = True

    if len(parts) < 4:
        i -= 1
        continue

    if parts[3] == "Test" and len(parts) >= 5 and not found_metrics:
        if parts[4] == "HITS@10":
            hits_10.append(float(parts[8]))
        if parts[4] == "HITS@3":
            hits_3.append(float(parts[8]))
        if parts[4] == "HITS@1":
            hits_1.append(float(parts[8]))
        if parts[4] == "MRR":
            MRR.append(float(parts[8]))
            found_metrics = True
            end_test_time = parts[0] + " " + parts[1]
        
    if parts[3] == "Evaluating" and len(parts) >= 6:
        if parts[5] == "Test":
            if not found_test_time:
                testing_time.append(time_difference_in_seconds(parts[0] + " " + parts[1], end_test_time))
                found_test_time = True

    i -= 1



def safe_mean(lst):
    return statistics.mean(lst) if lst else float('nan')

def ecart_type(lst):
    return statistics.stdev(lst) if len(lst) > 1 else float('nan')

# Print result lengths to check
print("Hits@1:", safe_mean(hits_1), ecart_type(hits_1))
print("Hits@3:", safe_mean(hits_3), ecart_type(hits_3))
print("Hits@10:", safe_mean(hits_10), ecart_type(hits_10))
print("MRR:", safe_mean(MRR), ecart_type(MRR))
print("training time:", safe_mean(training_time), ecart_type(training_time))
print("testing time:", safe_mean(testing_time), ecart_type(testing_time))

