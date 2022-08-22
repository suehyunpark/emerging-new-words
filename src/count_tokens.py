import json
import jsonlines
import os
import sys
from tqdm import tqdm
from collections import Counter
from pathlib import Path

ROOT_DIR = "/home/suehyun/datasets"

def count_tokens(dataset: str, split: str):
    dataset_dir = dataset + "-splits"
    root_path = Path(ROOT_DIR, dataset_dir)
    dir_name = split if split == "test" else "time_stratified_" + split
    split_path = root_path / dir_name
    
    tokens_cnt = Counter()
    
    for root, dirs, files in os.walk(split_path):
        for file in tqdm(files):
            if file.endswith(".tokenized.jsonl"):
                file_path = Path(root) / file
                assert file_path.is_file()
                
                with jsonlines.open(file_path, 'r') as f:
                    for line in f.iter():
                        tokens = line["tokenized"]
                        for token in tokens:
                            tokens_cnt[token] += 1
                
    
    DICT_NAME = "{}_{}_word_freq.json".format(dataset, split)
    write_stats_path = root_path / DICT_NAME
    tokens_dict = dict(tokens_cnt.most_common())
    with write_stats_path.open('w') as f:
        f.write(json.dumps(tokens_dict, indent=4))
    write_stats_path.chmod(0o444)  # read-only

    print(f"{split} set:")
    print(f"\tNumber of unique words: {len(tokens_cnt.keys())}\n\tTotal tokens count: {tokens_cnt.total()}")
    
if __name__ == "__main__":
    dataset = sys.argv[1]
    split = sys.argv[2]
    count_tokens(dataset, split)