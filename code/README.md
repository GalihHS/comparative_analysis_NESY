# comparative_analysis_NESY

all tests :

nohup ./run_all.sh > logs_for_all_tests.txt 2>&1 &


## To test Uniker:
from: https://github.com/vivian1993/UniKER

Go inside Uniker repository

On family_small with normal ontology:
```
python3 run.py family_small -1 family_small_model TransE 8 0.0 0.2
```

On family_small with less rules:
- rename data/family_small/MLN_rule.txt to data/family_small/normal_rules.txt (or less_rules.txt) - and - rename data/family_small/less_rules.txt to data/family_small/MLN_rule.txt
- rename data/family_small/train_sat.txt to data/family_small/train_sat_normal.txt - and - rename data/family_small/train_sat_less.txt to data/family_small/train_sat.txt
```
python3 run.py family_small -1 family_small_model TransE 8 0.0 0.2
```

On family_small with wrong rules:
- rename data/family_small/MLN_rule.txt to data/family_small/normal_rules.txt (or less_rules.txt) - and - rename data/family_small/wrong_rules.txt to data/family_small/MLN_rule.txt
- rename data/family_small/train_sat.txt to data/family_small/train_sat_less.txt - and - rename data/family_small/train_sat_normal.txt to data/family_small/train_sat.txt
```
python3 run.py family_small -1 family_small_model TransE 8 0.0 0.2
```

On family_medium:
```
python3 run.py family_medium -1 family_medium_model TransE 8 0.0 0.2
```

On FB15k-237:
```
python3 run.py fb15k -1 family_fb15k_model TransE 8 0.0 0.2
```



### To test KALE:
from: https://github.com/iieir-km/KALE

Go inside KALE repository

  - On family_small with normal ontology:

To train:
```
java -jar KALE.jar -train datasets/family_small/train.txt -valid datasets/family_small/valid.txt -test datasets/family_small/test.txt -rule datasets/family_small/groundings.txt -m 12 -n 2411 -w 0.1 -k 80 -d 0.3 -ge 0.1 -gr 0.1 -# 1500 -skip 50
```
To test:
```
java -cp src test.Eval_LinkPrediction 2411 12 80 MatrixE-k80-d0,3-ge0,1-gr0,1-w0,1.best MatrixR-k80-d0,3-ge0,1-gr0,1-w0,1.best datasets/family_small/train.txt datasets/family_small/valid.txt datasets/family_small/test.txt datasets/family_small/train_sat.txt
```


  - On family_small with less rules:

To train:
```
java -jar KALE.jar -train datasets/family_small/train.txt -valid datasets/family_small/valid.txt -test datasets/family_small/test.txt -rule datasets/family_small/groundings_less.txt -m 12 -n 2411 -w 0.1 -k 80 -d 0.3 -ge 0.1 -gr 0.1 -# 1500 -skip 50
```
To test:
```
java -cp src test.Eval_LinkPrediction 2411 12 80 MatrixE-k80-d0,3-ge0,1-gr0,1-w0,1.best MatrixR-k80-d0,3-ge0,1-gr0,1-w0,1.best datasets/family_small/train.txt datasets/family_small/valid.txt datasets/family_small/test.txt datasets/family_small/train_sat_less.txt
```




  - On family_small with wrong rules:

To train:
```
java -jar KALE.jar -train datasets/family_small/train.txt -valid datasets/family_small/valid.txt -test datasets/family_small/test.txt -rule datasets/family_small/groundings_wrong.txt -m 12 -n 2411 -w 0.1 -k 80 -d 0.3 -ge 0.1 -gr 0.1 -# 1500 -skip 50
```
To test:
```
java -cp src test.Eval_LinkPrediction 2411 12 80 MatrixE-k80-d0,3-ge0,1-gr0,1-w0,1.best MatrixR-k80-d0,3-ge0,1-gr0,1-w0,1.best datasets/family_small/train.txt datasets/family_small/valid.txt datasets/family_small/test.txt datasets/family_small/train_sat.txt
```




  - On family_medium:

To train:
```
java -jar KALE.jar -train datasets/family_medium/train.txt -valid datasets/family_medium/valid.txt -test datasets/family_medium/test.txt -rule datasets/family_medium/groundings.txt -m 12 -n 2968 -w 0.1 -k 80 -d 0.3 -ge 0.1 -gr 0.1 -# 1500 -skip 50
```
To test:
```
java -cp src test.Eval_LinkPrediction 2968 12 80 MatrixE-k80-d0,3-ge0,1-gr0,1-w0,1.best MatrixR-k80-d0,3-ge0,1-gr0,1-w0,1.best datasets/family_medium/train.txt datasets/family_medium/valid.txt datasets/family_medium/test.txt datasets/family_medium/train_sat.txt
```




  - On FB15k-237:

First unzip the fb15k.zip file

Then create groundings.txt: 
```
java -cp src basic.dataProcess.GroundAllRules fb15k
```
To train (-Xmx32g and -Xms8g are optionnal):
```
java -Xmx32g -Xms8g -jar KALE.jar -train datasets/fb15k/train.txt -valid datasets/fb15k/valid.txt -test datasets/fb15k/test.txt -rule datasets/fb15k/groundings.txt -m 237 -n 14505 -w 0.1 -k 120 -d 0.3 -ge 0.1 -gr 0.1 -# 2000 -skip 50
```
To test:
```
java -cp src test.Eval_LinkPrediction 14505 237 120 MatrixE-k120-d0,3-ge0,1-gr0,1-w0,1.best MatrixR-k120-d0,3-ge0,1-gr0,1-w0,1.best datasets/fb15k/train.txt datasets/fb15k/valid.txt datasets/fb15k/test.txt none
```






## To test ExpressGNN:
from: https://github.com/expressGNN/ExpressGNN

Go inside ExpressGNN repository

On family_small with normal ontology:
```
python3 -m main.train -data_root data/family_small -rule_filename rules.txt -slice_dim 16 -batchsize 16 -embedding_size 256 -gcn_free_size 255 -load_method 1 -exp_folder exp -exp_name family_small
```

On family_small with less rules:
```
python3 -m main.train -data_root data/family_small -rule_filename less_rules.txt -slice_dim 16 -batchsize 16 -embedding_size 256 -gcn_free_size 255 -load_method 1 -exp_folder exp -exp_name family_small
```

On family_small with wrong rules:
```
python3 -m main.train -data_root data/family_small -rule_filename wrong_rules.txt -slice_dim 16 -batchsize 16 -embedding_size 256 -gcn_free_size 255 -load_method 1 -exp_folder exp -exp_name family_small
```

On family_medium:
```
python3 -m main.train -data_root data/family_medium -rule_filename rules.txt -slice_dim 16 -batchsize 16 -embedding_size 256 -gcn_free_size 255 -load_method 1 -exp_folder exp -exp_name family_medium 
```

On FB15k-237:
```
python3 -m main.train -data_root data/fb15k-237 -rule_filename cleaned_rules_weight_larger_than_0.9.txt -slice_dim 16 -batchsize 16 -use_gcn 1 -num_hops 1 -embedding_size 128 -gcn_free_size 127 -patience 20 -lr_decay_patience 100 -entropy_temp 1 -load_method 1 -exp_folder exp -exp_name freebase
```






## To test sub-symbolic algorithms (TransE, RotatE, BoxE):
see pykeen documentation (https://pykeen.readthedocs.io/en/stable/)

Go inside sub_symbolics repository

On family_small:
```
python KGE_family.py conf_kge.json family_small
```

On family_medium:
```
python KGE_family.py conf_kge.json family_medium
```

On FB15k-237:
```
python KGE_family.py conf_kge.json FB15k-237
```








## To test the symbolic algorithm (DLV):
see DLV documentation (https://www.dlvsystem.it/dlvsite/dlv-user-manual/)

Go inside DLV repository

On family_small with normal ontology:

To generate the saturated file:
```
./run.sh family_small/train.txt family_small/rules.txt family_small/train_sat.txt
```
To evaluate it:
```
python compute_metrics.py family_small/test.txt family_small/train_sat.txt family_small/train.txt
```


On family_small with less rules:

To generate the saturated file:
```
./run.sh family_small/train.txt family_small/less_rules.txt family_small/train_sat_less_rules.txt
```
To evaluate it:
```
python compute_metrics.py family_small/test.txt family_small/train_sat_less_rules.txt family_small/train.txt
```


On family_small with wrong rules --> timeout:
```
./run.sh family_small/train.txt family_small/wrong_rules.txt family_small/train_sat_wrong_rules.txt
```
Then if files in_dlv and out_dlv are present:
```
rm in_dlv
rm out_dlv
```


On family_medium:

To generate the saturated file:
```
./run.sh family_medium/train.txt family_medium/rules.txt family_medium/train_sat.txt
```
To evaluate it:
```
python compute_metrics.py family_medium/test.txt family_medium/train_sat.txt family_medium/train.txt
```


On FB15k-237 --> timeout:
```
./run.sh fb15k-237/train.txt fb15k-237/rules.txt fb15k-237/train_sat.txt
```
Then if files in_dlv and out_dlv are present:
```
rm in_dlv
rm out_dlv
```





## To test AnyBURL:
see documentation (https://web.informatik.uni-mannheim.de/AnyBURL/)

On family_small:
```
./run_family_small.sh
```

On family_medium:
```
./run_family_medium.sh
```

On FB15k-237:
```
./run_fb15k-237.sh
```

