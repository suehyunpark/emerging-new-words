import os
from pathlib import Path
from tqdm import tqdm
from shutil import copy

SRC_DIR = "/home/suehyun/datasets/wmt-decoded"
DEST_DIR = "/home/suehyun/datasets/wmt-splits"
REF_DIR = "/home/suehyun/workspace/model/emerging-new-words/splits/wmt"

def print_title(title: str):
    print("=" * 80)
    print(title)
    print("=" * 80)
    
def get_target_docs(split: str) -> set():
    print_title(f"Parse target docs for {split} split ...")
    target_docs = set()
    if split == "test":
        split_path = Path(REF_DIR, split)
    else:
        split_path = Path(REF_DIR, "time_stratified_" + split)
    with split_path.open('r') as f:
        while True:
            line = f.readline()
            if not line:
                break
            date, docid = line.strip().split('\t')
            target_docs.add(date + '_' + docid + ".txt")
    print("Length of target docs:", len(target_docs))
    return target_docs

def move_files(split: str, begin_year: int, end_year: int, debug: bool):
    print_title("Start moving files ...")
    target_docs = get_target_docs(split)
    src_root_path = Path(SRC_DIR)
    
    # 1. Create a file to write
    dest_root_path = Path(DEST_DIR)
    
    if debug:
        dest_path = dest_root_path / "test"
        assert dest_path.exists()
        for year in range(begin_year, end_year+1):
            print(f"Process {split} dataset for {year} ...")
            src_path = src_root_path / str(year)
            dest_path = dest_path / str(year)
            for root, dirs, files in os.walk(src_path):
                for file in files:
                    if file in target_docs:
                        target_docs.remove(file)
                        if not dest_path.is_dir():
                            dest_path.mkdir()
                        if Path(dest_path, file).is_file():
                            continue
                        src_file_path = src_path / file
                        copy(str(src_file_path), str(dest_path))
        try:
            assert len(target_docs) == 0
        except:
            print("Missing docs:", sorted(list(target_docs)))
            
    else:
        dir_name = split if split == "test" else "time_stratified_" + split
        _dest_path = dest_root_path / dir_name
        assert _dest_path.exists()
        for year in range(begin_year, end_year+1):
            print(f"Process {split} dataset for {year} ...")
            src_path = src_root_path / str(year)
            dest_path = _dest_path / str(year)
            for root, dirs, files in os.walk(src_path):
                for file in tqdm(files):
                    if file in target_docs:
                        target_docs.remove(file)
                        if not dest_path.is_dir():
                            dest_path.mkdir()
                        if Path(dest_path, file).is_file():
                            continue
                        src_file_path = src_path / file
                        copy(str(src_file_path), str(dest_path))
        try:
            assert len(target_docs) == 0
        except:
            missing_docs = sorted(list(target_docs))
            print(f"Missing {len(missing_docs)} docs for {split} split: {missing_docs}")

if __name__ == "__main__":
    debug = False
    # move_files("train", 2007, 2017, debug)
    # move_files("validation", 2017, 2017, debug)  # done
    move_files("test", 2018, 2019, debug)  # done in prior