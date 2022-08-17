import json
import jsonlines
import os
import sys
from collections import Counter
from pathlib import Path

ROOT_DIR = "/home/suehyun/datasets/wmt-splits"

def count_tokens(split: str):
    root_path = Path(ROOT_DIR)
    dir_name = split if split == "test" else "time_stratified_" + split
    split_path = root_path / dir_name
    
    tokens_cnt = Counter()
    
    for root, dirs, files in os.walk(split_path):
        for file in files:
            if file.endswith(".tokenized.jsonl"):
                file_path = Path(root) / file
                assert file_path.is_file()
                
                with jsonlines.open(file_path, 'r') as f:
                    for line in f.iter():
                        tokens = line["tokenized"]
                        for token in tokens:
                            tokens_cnt[token] += 1
                
    
    DICT_NAME = "wmt_{}_word_freq.json".format(split)
    write_stats_path = split_path / DICT_NAME
    tokens_dict = dict(tokens_cnt.most_common())
    with open(str(write_stats_path), 'w') as f:
        f.write(json.dumps(tokens_dict, indent=4))
    write_stats_path.chmod(0o444)  # read-only

    print(f"{split} set:")
    print(f"\tNumber of unique words: {len(tokens_cnt.keys())}\n\tTotal tokens count: {tokens_cnt.total()}")
    
if __name__ == "__main__":
    split = sys.argv[1]
    count_tokens(split)