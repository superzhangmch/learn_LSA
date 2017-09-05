#encoding: gbk
import sys
import math

min_word_frequency = 32
word_dict = "word_dict.txt"
# word_dict: word dictionray file
emb_file = "word_emb.data"
# emb_file: word vector file
# ------------------------

word_dict_map = {}
id_2_word_map = {}
total_words = 0
i = 0
for line in open(word_dict):
    LL = line.strip().split("\t")
    total_words = total_words if total_words > 0 else int(LL[1])
    cnt = int(LL[0])
    if cnt > min_word_frequency:
        word_dict_map[LL[2]] = [i, math.log(1. * total_words / cnt)]
        id_2_word_map[i] = LL[2]
        i += 1
    else:
        break

def find_most_like(word_emb, target_id, cnt=10):
    vec1 = word_emb[target_id]
    arr = []
    for i in xrange(len(word_emb)):
        if i != target_id:
            vec2 = word_emb[i]
            score = sum([vec1[k]*vec2[k] for k in xrange(len(vec1))])
            arr.append([i, score])
    arr = sorted(arr, key=lambda x: x[1], reverse=True)
    for i in xrange(cnt):
        print id_2_word_map[arr[i][0]], arr[i]

LL = []
for line in open(emb_file):
    LLL = line.strip().split(" ") 
    LLL = [float(l) for l in LLL]
    aa = math.sqrt(sum([a**2 for a in LLL]))
    aa = aa if aa != 0 else 1.
    LLL = [l/aa for l in LLL]
    LL.append(LLL)

target_id =  word_dict_map["长治".decode("utf8").encode("gbk")][0]
find_most_like(LL, target_id)

while True:
    print ">",
    word = raw_input().strip()
    if not word:
        continue
    if word == "exit":
        break
    word_id = 0
    if word.isdigit() and int(word) in id_2_word_map:
        word_id = int(word)
    if word in word_dict_map:
        find_most_like(LL, word_dict_map[word][0])
    elif word.isdigit() and int(word) in id_2_word_map:
        word_id = int(word)
        print id_2_word_map[word_id]
        find_most_like(LL, word_id)
    else:
        print word, "not found"
        continue
