import sys
import csv
import re
import os
from pathlib import Path
from Bio import SeqIO
from Bio.Seq import Seq
from Bio.PDB import PDBParser
from Bio.PDB.DSSP import DSSP
#python merge_charge_reads_each_gene.py yeast.scaled.bowtie.Riboseq.codon.wave.adjusted.format.add.codon.filter.different.length.higher60.removed.all
input_data_wave = sys.argv[1]
input_path = sys.argv[2]
with open(input_data_wave) as f:
    for line2 in f.readlines():
        liness = line2.split()
        uniprotid = liness[0]
        count_reads = liness[2].split(',')
        position = []
        amino_acid = []
        charges = []

        chargefile = Path("/Your/work/path/Alpha-fold/"+input_path+"/AF-{}-F1-model_v2.pdb.pepinfo".format(uniprotid))
        if not chargefile.is_file():
            continue
        chargefile = "/Your/work/path/Alpha-fold/"+input_path+"/AF-{}-F1-model_v2.pdb.pepinfo".format(uniprotid)

        t=0
        with open(chargefile,"r") as charge:
            for line in charge.readlines():
                #Printing out Positive residues
                if (re.findall('Printing out Positive residues *?', line)):
                    t = 1
                    continue
                if (re.findall('Position *?', line) or line == '\n'):

                    continue

                if (re.findall('Printing out Negative residues *?', line) and t == 1):
                    break

                if (t == 1):
                    line = line.split()
                    #output = line[0] + "\t" + line[1] + "\t" + line[2] + "\n"
                    position.append(line[0])
                    amino_acid.append(line[1])
                    charges.append(line[2])
                    #output = line[0] + "\t" + line[1] + "\t" + line[2]

        print(len(count_reads))
        print(len(charges))
        print(uniprotid)
        if len(charges) == len(count_reads) - 1:
            for i in range(len(count_reads) - 1):
                extract_positive = ("{}\t{}\t{}\t{}".format(position[i], amino_acid[i], charges[i], count_reads[i], ))
                print(extract_positive, file=open("/Your/work/path/result/merge_charge_reads_each_gene/"+input_path+"/%s.txt" % uniprotid, "a"))
        else:
            continue
