import json
import os
from pathlib import Path
from string import punctuation

from sacremoses import MosesTokenizer
from tqdm import tqdm

ROOT_DIR = "/home/suehyun/datasets/wmt-splits"

punctuation_remove = punctuation.replace("'", "").replace("-", "")  # a valid word may contain a dash or an apostrophe
tokenizer = MosesTokenizer(lang='en')

def print_title(title: str):
    print("=" * 80)
    print(title)
    print("=" * 80)
    
def tokenize_file(file_path: Path):
    write_path = str(file_path)[:-3] + "tokenized.jsonl"
    write_f = open(write_path, 'w')
    
    with open(file_path, 'r') as f:
        for line in f:
            processed_line = line.translate(str.maketrans('', '', punctuation_remove))  # remove punctuation
            tokens = tokenizer.tokenize(processed_line.rstrip('\n'))  # tokenization using Moses
            data = {"orig": line, "tokenized": tokens}
            write_f.write(json.dumps(data) + '\n')
            write_f.flush()
            
    write_f.close()
    Path(write_path).chmod(0o444) # read-only
    
def process_split(split: str, begin_year: int, end_year: int):
    print_title("Start tokenizing split ...")
    root_path = Path(ROOT_DIR)
    
    dir_name = split if split == "test" else "time_stratified_" + split
    split_path = root_path / dir_name
    for year in range(begin_year, end_year+1):  # need to specify year range because tokenization can halt mid-process
        print(f"Process {split} dataset for {year} ...")
        split_year_path = split_path / str(year)
        for root, dirs, files in os.walk(split_year_path):
            for file in files:
                file_path = split_year_path / file
                tokenize_file(file_path)
    
if __name__ == "__main__":
    process_split("train", 2012, 2017)
    # process_split("test", 2018, 2019, debug)
