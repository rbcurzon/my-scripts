import pandas as pd
import argparse
from datasets import load_dataset
from datasets import concatenate_datasets
from datasets import DatasetDict

# read file 
if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='Concatenate train directories.')
    parser.add_argument('input_directories', nargs='+', help='List of input metadata files to concatenate')
    parser.add_argument('--output_file', default='concatenated_metadata.csv', help='Output file name')
    args = parser.parse_args()

    ds = DatasetDict()

    first_dir = parser.input_directories[0]
    
    ds = load_dataset('audiofolder', data_dir=first_dir)

    for directory in args.input_directories[1:]:
        
        if directory == first_dir:
            continue

        print("Appending", directory)

        ds['train'] = concatenate_datasets([ds['train'], load_dataset('audiofolder', data_dir=directory)['train']])
    