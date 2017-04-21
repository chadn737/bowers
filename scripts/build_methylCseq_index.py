#!/usr/local/apps/python/2.7.8/bin/python
import sys
import getopt
from methylpy.call_mc import build_ref

def main(argv):

	#Sample name
	sample = argv[0]

    #fasta file(s) of genome
    #Multiple files like input_files=['chr1.fa','chr2.fa',...,'chrY.fa','chrL.fa'] should also work
    input_files=[sample + '.fa']

    #Prefix of output files
    output=sample

    build_ref(input_files,output)

if __name__ == "__main__":
   main(sys.argv[1:])
