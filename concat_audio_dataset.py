import pandas as pd
import argparse
from datasets import load_dataset
from datasets import concatenate_datasets
from datasets import DatasetDict

# read file 
if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='Concatenate train directories.')
    parser.add_argument('input_directories', nargs='+', help='List of folders to concatenate')
    parser.add_argument('--output_file', default='concatenated_audio_dataset', help='Output file name')
    args = parser.parse_args()

    ds = DatasetDict()

    first_dir = args.input_directories[0]
    
    print("First directory", first_dir)
    
    try:
        ds = load_dataset('audiofolder', data_dir=first_dir)
    except Exception as e:
        print(f"Input should be a valid audio folder. Error: {e}")
        exit(1)

    for directory in args.input_directories[1:]:
        
        if directory == first_dir:
            continue

        print("Appending", directory)

        ds['train'] = concatenate_datasets([ds['train'], load_dataset('audiofolder', data_dir=directory)['train']])

    # Save the concatenated dataset to disk
    ds.save_to_disk(args.output_file)
    print("Output", args.output_file)
    