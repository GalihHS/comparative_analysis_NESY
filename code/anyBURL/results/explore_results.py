positive = []
negative = []
hits_1 = []
hits_3 = []
hits_10 = []
MRR = []
testing_time = []
training_time = []

import sys
import statistics

# Check if filename is passed
if len(sys.argv) < 3:
    print("Usage: python py_file.py <input_file_result> <input_file_time>")
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

    # Case 1: Line starts with "positive"
    if parts[0] == "positive":
        if len(parts) >= 7:
            try:
                pos_val = float(parts[2])
                neg_val = float(parts[6])
                positive.append(pos_val)
                negative.append(neg_val)
            except ValueError:
                print("error for : ", i)
                pass  # skip if not numbers

    # Case 2: Line starts with "* loading"
    elif parts[0] == "*" and parts[1] == "loading":
        if i + 1 < len(lines):
            next_line = lines[i + 1].strip()
            values = next_line.split()
            if len(values) >= 4:
                try:
                    hits_1.append(float(values[0]))
                    hits_3.append(float(values[1]))
                    hits_10.append(float(values[2]))
                    MRR.append(float(values[3]))
                except ValueError:
                    pass
            i += 1  # Skip the line that was just read

    i += 1


filename_time = sys.argv[2]

with open(filename_time, "r") as f:
    for line in f:
        line = line.strip()
        if line.startswith("APPLY"):
            parts = line.split()
            testing_time.append(int(parts[-2]))  # Extract number before "seconds"
        elif line.startswith("LEARN"):
            parts = line.split()
            training_time.append(int(parts[-2]))


def sum_every_n_elements(lst, n):
    return [sum(lst[i:i+n]) for i in range(0, len(lst), n)]


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
print("testing time", safe_mean(testing_time), ecart_type(testing_time))

