hits_1 = []
hits_3 = []
hits_10 = []
MRR = []
testing_time = []
training_time = []

import sys
import statistics

# Check if filename is passed
if len(sys.argv) < 2:
    print("Usage: python py_file.py <input_file_result>")
    sys.exit(1)

filename_res = sys.argv[1]

with open(filename_res, "r") as file:
    lines = file.readlines()

i = 0
while i < len(lines):
    line = lines[i].strip()
    parts = line.split()

    if len(parts) <= 1:
        i += 1
        continue

    # Case 2: Line starts with "* loading"
    elif parts[0] == "Build":
        training_time.append(float(parts[3]))
    elif parts[0] == "HITS@1:":
        hits_1.append(float(parts[1]))
    elif parts[0] == "HITS@3:":
        hits_3.append(float(parts[1]))
    elif parts[0] == "HITS@10:":
        hits_10.append(float(parts[1]))
    elif parts[0] == "MRR:":
        MRR.append(float(parts[1]))
    elif parts[0] == "Total":
        testing_time.append(float(parts[3]))
    i += 1



def sum_every_n_elements(lst, n):
    return [sum(lst[i:i+n]) for i in range(0, len(lst), n)]

def safe_mean(lst):
    return statistics.mean(lst) if lst else float('nan')

def ecart_type(lst):
    return statistics.stdev(lst) if len(lst) > 1 else float('nan')

# Print result lengths to check
print("Hits@1:", safe_mean(hits_1[:5]), ecart_type(hits_1[:5]))
print("Hits@3:", safe_mean(hits_3[:5]), ecart_type(hits_3[:5]))
print("Hits@10:", safe_mean(hits_10[:5]), ecart_type(hits_10[:5]))
print("MRR:", safe_mean(MRR[:5]), ecart_type(MRR[:5]))
print("training time:", safe_mean(training_time[:5]), ecart_type(training_time[:5]))
print("testing time", safe_mean(testing_time[:5]), ecart_type(testing_time[:5]))

