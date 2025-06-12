# The Family Dataset
Knowledge Graph with Family relations

Data Source: [LERP Github](https://github.com/Glaciohound/LERP) 

**12 different relation types:** 
* aunt
* brother
* daughter
* father
* husband
* mother
* nephew
* niece
* sister
* son
* uncle
* wife



## Files
* all.txt contains 28.356 triples
* `train.txt` contains 5.868 triples
* `valid.txt` contains 2.038 triples
* `test.txt` contains 2.835 triples


### Load Files
Code snippet to load `.txt` files and stores lists of `edge_index`  as tuples of head and tail id and `edge_type`. 
```python
from pathlib import Path

triples = open('./family/facts.txt').readlines()
edge_index, edge_type = [], []

for line in triples:
    head, relation, tail = line.split('\t')
    if tail.endswith('\n'):
        tail = tail[:-1]
    edge_index.append([int(head), int(tail)])
    edge_type.append(relation)
```
