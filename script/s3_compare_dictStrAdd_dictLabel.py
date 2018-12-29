
from script.s2_merge_dict import *

assert False, "Error: algorithm is not consistent. "

f = open(path.dict_answer_label, "r")
for line in f:
    answers_label = json.loads(line)
f.close()

f = open(path.dict_answer_label_cat_add, "r")
for line in f:
    answers_cat_add = json.loads(line)
f.close()

count_not_exits = 0
for (i_key, i_value) in answers_label.items():
    if i_key not in answers_cat_add:
        count_not_exits += 1

print(count_not_exits)