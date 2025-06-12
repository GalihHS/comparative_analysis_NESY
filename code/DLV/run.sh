echo -e "\n#################### Start DLV for triples ######################"

# Get parameters from user input
TRAINFILE="$1"
RULEFILE="$2"
OUTFILE="$3"

# parse triple file in dlv format and join rules
python3 in_parser.py  --trainfile "$TRAINFILE" --rulefile "$RULEFILE"

./dl in_dlv > out_dlv

# save new triples file as *_sat.txt
python3 out_parser.py --outfile "$OUTFILE"

# delete temporary files
rm in_dlv
rm out_dlv
