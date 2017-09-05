input_file = "query_log.txt1.out"
# input_file line format(space seperated): word1 word2 word3 ... wordN\n
word_dict_file = "word_dict.txt"
# output word_dict_file  line format: word_frequency \t total_word_cnt \t word \n

# ---
fp = open(input_file)
m = {}
i = 0
for line in fp:
        i += 1
        if i % 1000000 == 0:
                print i
        LL = set(line.strip().split(" "))
        for L in LL:
                if L not in m:
                        m[L] = 0
                m[L] += 1
total = i
arr = []
for k in m:
        arr.append([k, m[k]])
arr = sorted(arr, key=lambda x:x[1], reverse=True)

fp = open(word_dict_file, "w")
for i in xrange(len(arr)):
        fp.write("%d\t%d\t%s\n" % (arr[i][1], total, arr[i][0]))
fp.close()
