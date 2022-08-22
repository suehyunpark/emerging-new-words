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

'''
with open("output/wmt/rare_words.json", 'r') as j:
    rare_words = json.load(j)
    
with open("output/wmt/unseen_words.json", 'r') as j:
    unseen_words = json.load(j)
    
rare_words_df = pd.json_normalize(rare_words["rare_words"])
unseen_words_df = pd.json_normalize(unseen_words["unseen_words"])

rare_words_df.to_csv("output/wmt/rare_words.csv")
unseen_words_df.to_csv("output/wmt/unseen_words.csv")
'''