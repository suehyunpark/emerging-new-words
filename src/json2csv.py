import pandas as pd
import json
import sys

ROOT_DIR = "../output"


def json2csv(read_path: str, write_path: str, orient: str=None, field: str=None):
    if field:
        with open(read_path, 'r') as j:
            data = json.load(j)
        df = pd.json_normalize(data[field])
        df.to_csv(write_path)
    else:
        data = pd.read_json(read_path, orient=orient)
        data.to_csv(write_path)
    
    
if __name__ == "__main__":
    dataset, file_name, orient, field = sys.argv[1:]
    read_path = ROOT_DIR + '/' + dataset + "/json/" + file_name
    write_path = ROOT_DIR + '/' + dataset + "/csv/" + file_name[:-5] + ".csv"
    json2csv(read_path, write_path, orient, field)
    
    # orient=index for *word_freq.json