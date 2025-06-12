# Saturate Triples With DLV
With this tool we can saturate a knowledge graph stored in a `*.txt` file with containing triples with a given ruleset specified in  `rules`. 
The rules have to be compliant with the expected format of DLV. Triples are separated by `\n`. Head, relation and tail are 
expected to be stored as `<head>\t<relation>\t<tail>\n`.
The input file name has to be specified in the `run.sh` script.

*TODO: can be done with command I guess.* 

### References
* DLV User Manual [Link](https://www.dlvsystem.it/dlvsite/dlv-user-manual/)
* DLV Tutorial [Link](https://www.dbai.tuwien.ac.at/proj/dlv/tutorial/)

## How to run 
1. Specify the desired rules in `rules`. Each line has to end with a dot `.`!
2. Put the triple file `<name>.txt` in the directory. Set the filename in `run.sh`. 
3. Execute `run.sh`
4. The new triples of the saturated graph according to the rules are stored in `<name>_sat.txt`
