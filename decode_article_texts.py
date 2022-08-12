import hashlib
import os
from pathlib import Path
import base64
from tqdm import tqdm

READ_DIR = "/home/suehyun/datasets/wmt/"
WRITE_DIR = "/home/suehyun/datasets/wmt-decoded"

def print_title(title: str):
    print("=" * 80)
    print(title)
    print("=" * 80)

def process_for_one_file(file_path: Path, write_dir: Path):
    cnt = 0
    with open(str(file_path), 'rb') as file:
        for line in tqdm(file):
            date, sentence_split_text, unsplit_text = line.decode('utf-8').strip().split('\t')
            docid = hashlib.sha256(unsplit_text.encode('utf-8')).hexdigest()  # SHA256 hashes of the Base64 encoded unsplit texts of articles as their IDs
            sentence_split_text = base64.b64decode(sentence_split_text).decode('utf-8')  # The article texts are encoded with base64 encoding
            
            file_name = date + '_' + docid + ".txt"
            write_path = Path(write_dir, file_name)
            if write_path.is_file():
                # raise FileExistsError
                continue
            else:
                with write_path.open('w+') as f:
                    f.write(sentence_split_text)
                write_path.chmod(0o444)  # read-only
    # assert cnt == len(os.listdir(write_dir))  # number of read lines == number of written files
    
def process_for_all_files(debug: bool):
    print_title("Start processing files...")
    root_path = Path(READ_DIR)
    
    write_root_dir = Path(WRITE_DIR)
    
    if debug:
        file = "news-docs.2019.en.filtered"
        year = file.split('.')[1]
        print_title(f"Process {year}: {file} ...")
        file_path = root_path / file
        write_dir = write_root_dir / year
        if not write_dir.is_dir():
            write_dir.mkdir()
        process_for_one_file(file_path, write_dir)
    else:
        for root, dirs, files in os.walk(root_path):
            files = sorted(files)[1:]  # exclude .DS_STORE
            for i, file in enumerate(files):
                year = file.split('.')[1]
                print_title(f"Process {year}: {file} ...")
                file_path = root_path / file
                write_dir = write_root_dir / year
                if not write_dir.is_dir():
                    write_dir.mkdir()
                process_for_one_file(file_path, write_dir)

if __name__ == "__main__":
    debug = False
    process_for_all_files(debug)