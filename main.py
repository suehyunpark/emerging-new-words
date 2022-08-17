import json

# Total number of tokens - denominator of unigram probability
TRAIN_TOKENS_CNT = 3905056067
TEST_TOKENS_CNT = 12749939

TRAIN_PATH = "/home/suehyun/datasets/wmt-splits/time_stratified_train/wmt_train_word_freq.json"
TEST_PATH = "/home/suehyun/datasets/wmt-splits/test/wmt_test_word_freq.json"
OUT_DIR = "./output/wmt/"

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
    train_freq_dict = json_to_dict(TRAIN_PATH)
    test_freq_dict = json_to_dict(TEST_PATH)
    # freq_dict_stats(test_freq_dict, "test")
    get_emerging_new_words(train_freq_dict, test_freq_dict)