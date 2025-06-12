# UniKER
## Introduction
The official Pytorch implementation of the paper [UniKER: A Unified Framework for Combining Embedding and Definite Horn Rule Reasoning for Knowledge Graph Inference](https://aclanthology.org/2021.emnlp-main.769.pdf)

## Supported Models:
* RotatE, pRotatE, TransE, ComplEx, DistMult
 
## Evaluation Metrics:
* MRR, MR, HITS@1, HITS@3, HITS@10 (filtered)

## KG Data:
* entities.dict: a dictionary map entities to unique ids
* relations.dict: a dictionary map relations to unique ids
* train.txt: the KGE model is trained to fit this data set
* valid.txt: create a blank file if no validation data is available
* test.txt: the KGE model is evaluated on this data set
* MLN_rule.txt: the logical rules with the format "weight \t head_rel \t body1_rel \t body2_rel"

## Usage
For example, this command train a UniKER on family dataset with the scoring function defined following TransE with GPU 0.
```
  python run.py family 0 family_model TransE 8 0.0 0.2
```
Each parameter means:
```
  python run.py DATASET CUDA SAVE_MODEL_NAME BASIC_KGE_MODEL INTER NOISE_THRESHOLD TOP_K_THRESHOLD IS_INIT
```

----------

To test it on family_small with normal ontology:
```
python3 run.py family_small -1 family_small_model TransE 8 0.0 0.2
```

To test it on family_small with less rules:
- rename data/family_small/MLN_rule.txt to data/family_small/normal_rules.txt (or less_rules.txt) - and - rename data/family_small/less_rules.txt to data/family_small/MLN_rule.txt
- rename data/family_small/train_sat.txt to data/family_small/train_sat_normal.txt - and - rename data/family_small/train_sat_less.txt to data/family_small/train_sat.txt
```
python3 run.py family_small -1 family_small_model TransE 8 0.0 0.2
```

To test it on family_small with wrong rules:
- rename data/family_small/MLN_rule.txt to data/family_small/normal_rules.txt (or less_rules.txt) - and - rename data/family_small/wrong_rules.txt to data/family_small/MLN_rule.txt
- rename data/family_small/train_sat.txt to data/family_small/train_sat_less.txt - and - rename data/family_small/train_sat_normal.txt to data/family_small/train_sat.txt
```
python3 run.py family_small -1 family_small_model TransE 8 0.0 0.2
```

To test it on family_medium:
```
python3 run.py family_medium -1 family_medium_model TransE 8 0.0 0.2
```

To test it on FB15k-237:
```
python3 run.py fb15k -1 family_fb15k_model TransE 8 0.0 0.2
```


