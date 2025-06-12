positive = []
negative = []
hits_1 = []
hits_3 = []
hits_10 = []
MRR = []
training_time = []
testing_time = []

import sys
import statistics

# Check if filename is passed
if len(sys.argv) < 3:
    print("Usage: python py_file.py <input_file> <timestamp_file>")
    sys.exit(1)

filename = sys.argv[1]

with open(filename, "r") as file:
    lines = file.readlines()

i = 0
while i < len(lines):
    line = lines[i].strip()
    parts = line.split()

    if len(parts) <= 1:
        i += 1
        continue

    # Case 2: Line starts with "* loading"
    elif parts[0] == "Filt" and parts[1] == "setting:":
        
        if i + 10 < len(lines):
            new_line = (lines[i + 2].strip()).split()
            if new_line[0] == "MRR:":
                MRR.append(float(new_line[1]))
            new_line = (lines[i + 4].strip()).split()
            if new_line[0] == "Hit@1:":
                hits_1.append(float(new_line[1]))
            new_line = (lines[i + 5].strip()).split()
            if new_line[0] == "Hit@3:":
                hits_3.append(float(new_line[1]))
            new_line = (lines[i + 7].strip()).split()
            if new_line[0] == "Hit@10:":
                hits_10.append(float(new_line[1]))
        i += 10
            
    i += 1

filename_time = sys.argv[2]

with open(filename_time, "r") as f:
    lines_time = f.readlines()

i = 0
while i < len(lines_time):
    line = lines_time[i].strip()
    parts = line.split()
    
    if len(parts) <= 1:
        i += 1
        continue

    if parts[0] == "LEARN" or parts[0] =="BUILD" :
        training_time.append(float(parts[2]))
    elif parts[0] == "INFERENCE":
        testing_time.append(float(parts[2]))
   
    i += 1


contradicts_1 = [positive[i]/(positive[i]+negative[i]) for i in range(len(positive))]

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
print("testing time:", safe_mean(testing_time[:5]), ecart_type(testing_time[:5]))

