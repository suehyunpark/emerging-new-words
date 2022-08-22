import json
import os
from pathlib import Path
from string import punctuation
import re

from sacremoses import MosesTokenizer
from tqdm import tqdm

ROOT_DIR = "/home/suehyun/datasets/arxiv-splits"

punctuation_remove = punctuation.replace("'", "").replace("-", "").replace("&", "")  # a valid word may contain a dash or an apostrophe
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
            processed_line = re.sub(r"(\${1,2})(?:(?!\1)[\s\S])*\1", '', line)  # remove math expressions
            processed_line = processed_line.translate(str.maketrans('', '', punctuation_remove))  # remove punctuation
            tokens = tokenizer.tokenize(processed_line.rstrip('\n'))  # tokenization using Moses
            data = {"orig": line, "tokenized": tokens}
            write_f.write(json.dumps(data) + '\n')
            write_f.flush()
            
    write_f.close()
    Path(write_path).chmod(0o444) # read-only
    
def process_all_files():
    print_title("Start tokenizing ...")
    
    # path = Path("/home/suehyun/datasets/arxiv-splits/test/20180102_1801.00574.txt")
    # tokenize_file(path)
    # return
    
    root_path = Path(ROOT_DIR)
    for root, dirs, files in os.walk(root_path):
        for file in tqdm(files):
            file_path = Path(root, file)
            assert file_path.is_file()
            tokenize_file(file_path)
    
if __name__ == "__main__":
    process_all_files()