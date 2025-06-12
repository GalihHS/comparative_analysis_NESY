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
import json

# Check if filename is passed
if len(sys.argv) < 3:
    print("Usage: python py_file.py <input_dir> <input_method>")
    sys.exit(1)

filename = sys.argv[2] + "/" + sys.argv[1] + "/"

for j in range(5):

    filename_res = filename + "results_" + str(j+1) + ".json"

    with open(filename_res, "r") as file_res:
        data = json.load(file_res)
    
    realistic = data["metrics"]["both"]["realistic"]
    times = data["times"]

    # Extract the desired values
    hits_1.append(realistic["hits_at_1"])
    hits_3.append(realistic["hits_at_3"])
    hits_10.append(realistic["hits_at_10"])
    MRR.append(realistic["inverse_harmonic_mean_rank"])
    testing_time.append(times["evaluation"])
    training_time.append(times["training"])




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

