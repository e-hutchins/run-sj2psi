#!/usr/bin/env python

import sj2psi
from sj2psi import get_psis
import argparse
import pandas as pd

def main():
    # Set up argument parsing
    parser = argparse.ArgumentParser(description='Process a sample file with sj2psi.')
    parser.add_argument('filename', type=str, help='Input file (e.g., sample1.SJ.out.tab)')
    parser.add_argument('output', type=str, help='Output file (e.g., sample1.SJ.withPSIs.txt)')
    
    args = parser.parse_args()
    input_filename = args.filename
    output_filename = args.output

    # Read in the SJ.out.tab file
    sj_out_tab = sj2psi.read_sj_out_tab(input_filename)
    
    # Compute psis with the provided parameters
    sj_with_psis = get_psis(sj_out_tab, min_unique=1, min_multimap=10)
    
    # Export the results to a tab-delimited text file
    sj_with_psis.to_csv(output_filename, sep='\t', index=False)
    print(f"Output saved to {output_filename}")

if __name__ == '__main__':
    main()
