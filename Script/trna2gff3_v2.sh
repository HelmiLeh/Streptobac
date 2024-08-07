#!/bin/bash

################################################################################
# trna2gff3.sh                                                                 #
#                                                                              #
# This script is used to change format from trna-scan output into gff3         #
#                                                                              #
#                                                                              #
# 		                                                               #
# edited by Yusuf in June 2018 for tRNAscan-SE version 2.0                     #
# v2.0 uses Infernal instead of Cove score                                     #
# shuhaila129@gmail.com                                                        #
################################################################################
echo "USAGE: ./trna2gff3_v2.sh <trna_scans_result> <Outputfile>";

echo "##gff-version 3" > $2;

while read line; do
        chromosome=`echo "$line" | cut -f 1`;
        trna_count=`echo "$line" | cut -f 2`;
        start=`echo "$line" | cut -f 3`;
        end=`echo "$line" | cut -f 4`;
        type=`echo "$line" | cut -f 5`;
        anticodon=`echo "$line" | cut -f 6`;
        infernal_score=`echo "$line" | cut -f 9`;
        #hmm_score=`echo "$line" | cut -f 10`;
        #sec_score=`echo "$line" | cut -f 11`;
        if [ $start -lt $end ]; then #-lt is less than
                direction="+";
        else
                direction="-";
                start=`echo "$line" | cut -f 4`;
                end=`echo "$line" | cut -f 3`;
        fi
        if [[ $trna_count =~ ^[0-9]+$ ]]; then
                echo -ne "${chromosome}\t";
                echo -ne "tRNAscan-SE\t";
                echo -ne "tRNA\t";
                echo -ne "${start}\t";
                echo -ne "${end}\t";
                echo -ne ".\t";
                echo -ne "${direction}\t";
                echo -ne ".\t";
                echo -ne "Name=${chromosome}_tRNA_${trna_count};";
                echo -ne "ID=\"tRNA_type:${type}-${anticodon}\";";
                echo -ne "Note=\"score:infernal-${infernal_score}\"";
                echo;
        fi;
done < $1 >> $2

