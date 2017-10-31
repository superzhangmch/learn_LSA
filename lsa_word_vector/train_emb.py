#encoding: gbk
from scipy import sparse
from sklearn.decomposition import TruncatedSVD
import math

min_word_frequency = 32
train_data = "query_log.txt1.out_random.txt"
# train_data line format(space seperated words): word1 word2 ... wordN \n
max_line_cnt = 10000000
# read how many lines from file train_data
word_dict_file = "word_dict.txt"
# word_dict_file: word dictionary file, line format: exists_in_doc_cnt \t doc_cnt \t word \n
emb_file = "emb_rand"
# emb_file: output file

# -----------
print "load word dict file"
# word dict file line format: exists_in_doc_cnt \t doc_cnt \t word \n
word_dict_map = {}
id_2_word_map = {}
total_words = 0
i = 0
for line in open(word_dict_file):
    LL = line.strip().split("\t")
    total_words = total_words if total_words > 0 else int(LL[1])
    cnt = int(LL[0])
    if cnt > min_word_frequency:
        word_dict_map[LL[2]] = [i, math.log(1. * total_words / cnt)]
        id_2_word_map[i] = LL[2]
        i += 1
    else:
        break
total_words = i

print "load train data file"
# train_file line format: word1 word2 word3 ... wordN \n
data = []
j = 0
for line in open(train_data):
    LL = set(line.strip().split(" "))
    arr = []
    for L in LL:
        if L in word_dict_map:
            arr.append([word_dict_map[L][0], j, word_dict_map[L][1]])
    if len(arr) >= 3:
        data += arr
        j += 1
    if j % 100000 == 0:
        print "j =", j
    if j >= max_line_cnt:
        break
max_line_cnt = j

print "sort"
data = sorted(data, key=lambda x: (x[0], x[1]))

print "trans to sparse matrix"
x_coor = []
y_coor = []
data_coor = []
for x, y, d in data:
    x_coor.append(x)
    y_coor.append(y)
    data_coor.append(d)
spr_matrix = sparse.coo_matrix((data_coor, (x_coor, y_coor)),shape=(total_words, max_line_cnt))

print "train by SVD"
svd = TruncatedSVD(n_components=128, n_iter=5, random_state=42, 
        algorithm ="arpack")
        #algorithm ="randomized") # 两种训练方法；当=random方法时，n_iter 不生效。那么arpack应该是精确求解吧？
word_emb = svd.fit_transform(spr_matrix) # M=UEV≈U_k*E_k*V_k', 则transform(M)=V_k*M

print "save to file", 
print len(word_emb)
fp = open(emb_file, "w")
for emb in word_emb:
    emb_str = ["%.6f" % e for e in emb]
    fp.write(" ".join(emb_str) + "\n")
fp.close()
