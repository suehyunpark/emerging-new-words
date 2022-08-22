import json
import sys

# Total number of tokens - denominator of unigram probability
TRAIN_TOKENS_CNT = 0
TEST_TOKENS_CNT = 0

ROOT_DIR = "/home/suehyun/datasets"
OUT_DIR = "/home/suehyun/workspace/model/emerging-new-words/output"

def format_small_num(num):
    return '{0:.10f}'.format(num)


def json_to_dict(file_path: str) -> dict:
    with open(file_path) as d:
        freq_dict = json.loads(d.read())
    return freq_dict


def freq_dict_stats(freq_dict: dict, split: str):
    num_unique_tokens = len(freq_dict.keys())
    total_tokens_cnt = sum(freq_dict.values())
    print(f"{split} set:")
    print(
        f"\tNumber of unique words: {num_unique_tokens}\n\tTotal tokens count: {total_tokens_cnt}")


def get_emerging_new_words(train_dict: dict, test_dict: dict):
    unseen_words = list()  # (i) previously unseen on the training set
    rare_words = list()  # (ii) occured much less frequently on the training set than on the test set

    unseen_words_cnt, unseen_words_mentions = 0, 0
    rare_words_cnt, rare_words_mentions = 0, 0
    
    for token, freq in test_dict.items():
        if freq >= 50:  # occur frequently on the test set
            test_prob = freq / float(TEST_TOKENS_CNT)
            if token in train_dict:
                train_prob = train_dict[token] / float(TRAIN_TOKENS_CNT)
                if test_prob >= train_prob * 5:  # at least 5 times lower unigram probability
                    rare_words.append(
                        {"token": token, "freq": freq, "train_unigram_prob": format_small_num(train_prob), "test_unigram_prob": format_small_num(test_prob)})
                    rare_words_cnt += 1
                    rare_words_mentions += freq
            else:
                unseen_words.append({"token": token, "freq": freq, "test_unigram_prob": format_small_num(test_prob)})
                unseen_words_cnt += 1
                unseen_words_mentions += freq
    
    unseen_words_sorted = sorted(unseen_words, key=lambda d: d["freq"], reverse=True)
    rare_words_sorted = sorted(rare_words, key=lambda d: d["freq"], reverse=True)
    
    unseen_words_dict = {"count": unseen_words_cnt, "num_mentions_test": unseen_words_mentions, "unseen_words": unseen_words_sorted}
    rare_words_dict = {"count": rare_words_cnt, "num_mentions_test": rare_words_mentions, "rare_words": rare_words_sorted}
    
    with open(OUT_DIR + "unseen_words.json", 'w') as f:
        f.write(json.dumps(unseen_words_dict, indent=4))
    
    with open(OUT_DIR + "rare_words.json", 'w') as f:
        f.write(json.dumps(rare_words_dict, indent=4))
            
               
if __name__ == "__main__":
    dataset = sys.argv[1]
    TRAIN_TOKENS_CNT = sys.argv[2]  # wmt: 3905056067  arxiv: 100108282
    TEST_TOKENS_CNT = sys.argv[3]   # wmt: 12749939    arxiv: 3500702
    
    train_path = "{}/{}-splits/{}_train_word_freq.json".format(ROOT_DIR, dataset, dataset)
    test_path = "{}/{}-splits/{}_test_word_freq.json".format(ROOT_DIR, dataset, dataset)
    
    ROOT_DIR += '/' + dataset
    OUT_DIR += '/' + dataset + "/json/"
    
    train_freq_dict = json_to_dict(train_path)
    test_freq_dict = json_to_dict(test_path)
    
    get_emerging_new_words(train_freq_dict, test_freq_dict)