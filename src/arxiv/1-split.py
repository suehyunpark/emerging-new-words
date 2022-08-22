from pathlib import Path
from tqdm import tqdm
import json

SRC_FILE = "/home/suehyun/datasets/arxiv/arxiv-metadata-oai-snapshot.json"
TRAIN_DIR = "/home/suehyun/datasets/arxiv-splits/time_stratified_train"
VALIDATION_DIR = "/home/suehyun/datasets/arxiv-splits/time_stratified_validation"
TEST_DIR = "/home/suehyun/datasets/arxiv-splits/test"
REF_DIR = "/home/suehyun/workspace/model/emerging-new-words/splits/arxiv"

def print_title(title: str):
    print("=" * 80)
    print(title)
    print("=" * 80)
    
def get_target_docs(split: str) -> dict():
    print_title(f"Parse target docs for {split} split ...")
    target_docs = dict()
    
    if split == "test":
        split_path = Path(REF_DIR, split)
    else:
        split_path = Path(REF_DIR, "time_stratified_" + split)
    with split_path.open('r') as f:
        while True:
            line = f.readline()
            if not line:
                break
            date, doc_id = line.strip().split('\t')
            target_docs[doc_id] = date
    print(f"Length of {split} target docs: {len(target_docs)}\n")
    return target_docs

def write_data(write_dir: Path, date: str, doc_id: str, abstract: str):
    doc_id = doc_id.replace('/', '=')  # file names do not allow slashes, e.g., "solv-int/9812025"
    abstract = abstract.strip().replace('\n', ' ')
    
    file_name = date + '_' + doc_id + ".txt"
    write_path = write_dir / file_name
    with write_path.open('w') as f:
        f.write(abstract)
    write_path.chmod(0o444)  # read-only

def parse_then_move_files(train_target: dict, validation_target: dict, test_target: dict):
    print_title("Start parsing json and move files ...")
    src_file_path = Path(SRC_FILE)
    
    train_dir_path = Path(TRAIN_DIR)
    validation_dir_path = Path(VALIDATION_DIR)
    test_dir_path = Path(TEST_DIR)
    
    with open(src_file_path) as f:
        for line in tqdm(f):
            meta_data = json.loads(line)
            doc_id = meta_data["id"]
            abstract = meta_data["abstract"]
            
            if train_target.get(doc_id):  # amortized O(1) time complexity
                write_data(train_dir_path, train_target.pop(doc_id), doc_id, abstract)
            elif validation_target.get(doc_id):
                write_data(validation_dir_path, validation_target.pop(doc_id), doc_id, abstract)
            elif test_target.get(doc_id):
                write_data(test_dir_path, test_target.pop(doc_id), doc_id, abstract)
    
    try:
        assert len(train_target) == 0
    except:
        print("Missing train docs", sorted(list(train_target)))
        
    try:
        assert len(validation_target) == 0
    except:
        print("Missing validation docs", sorted(list(validation_target)))
        
    try:
        assert len(test_target) == 0
    except:
        print("Missing test docs", sorted(list(test_target)))

if __name__ == "__main__":
    train_target = get_target_docs("train")
    validation_target = get_target_docs("validation")
    test_target = get_target_docs("test")
    parse_then_move_files(train_target, validation_target, test_target)
    