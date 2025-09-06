import argparse
from datasets import load_dataset
from datasets import DatasetDict

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='Concatenate train directories.')
    parser.add_argument('data_dir', help='Directory containing the dataset to push to the Hugging Face Hub')
    parser.add_argument('--repo_id', default='username/repo_name', help='Hugging Face Hub repository ID')
    parser.add_argument('--config_name', help='Configuration name for the dataset')
    parser.add_argument('--token', help='Hugging Face Hub token for authentication')
    args = parser.parse_args()

    ds = DatasetDict()

    ds = DatasetDict.load_from_disk(args.data_dir)
    
    train_test_ds = ds['train'].train_test_split(test_size=0.2, seed=42, shuffle=True)

    train_test_ds.push_to_hub(
        repo_id=args.repo_id,
        config_name=args.config_name,
        token=args.token,
        # private=True,
    )