python myhammerdecoder.py > b15message 
awk 'BEGIN{FIELDWIDTHS="2 1 1 3 1 7"}{print $2 $4 $6}' b15message >b7message
cat b7message |tr -d $'\n'|while read -N4 nibble;do printf '%x' "$((2#${nibble}))"; done| xxd -r -p > btext
hexer btext
