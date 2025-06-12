# Training Knowledge Graph Embeddings with `pykeen.pipeline`
## Principle Idea 
Training knowledge graph embeddings on the family dataset with [pykeen](https://pykeen.readthedocs.io/en/stable/)
Here is no symbolic part involved. This can be used for getting pretrained models or benchmarking. 

## How to run 
**Software setup**  
Make sure the requirements are installed.
I am using Python `3.11.5`.

To setup a new environment do:
```conda create -n <name> python==3.11```

To install the packages from the `requirements.txt`, go at first to the project directory

```cd ..```

Then install the packages from the file: 

``` pip install -r requirements.txt```


**Run the code**   
Activate the environment and run the code:
```
cd KGE
conda activate <name>
python KGE_family.py conf_kge.json
```

## Overview of file architecture
* `KGE_results` 
contains the result directories of the trained models in the concerned subdirectory.
There is one subdirectory per model with results (`results.json`), metadata (`metadata.json`) and the trained model (`trained_model.pkl`)
* `KGE_family.py`
The main script to run the experiments. 
* `conf_kge.json`

### How to set config.json
The configurations stored in `config.json` contains a list of multiple experiment configurations. This allows to define a series of experiments to be run. One configuration in the list will correspond to one run on Weights and Biases. 

Each run has the following parameters:
* `device` choose 0 or 1 for multiple gpus. *default: 0`
* `epochs` number of training epochs. *default: 1000*
* `model` model from pykeen *default "ConvE"
* `seed` random seed for reproducibility. *default 1234*
* `create_inverse_triples` required argument for model ConvE *default: false*
