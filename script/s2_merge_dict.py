
import json

import utility


class Config:
    def __init__(self):
        self.image_size = (1080, 1920)
        self.__phone_sizes__ = ["Mi_note3", "Mi_redPro"]
        self.phone_size = self.__phone_sizes__[0]
        print("phone_size: %s" % self.phone_size)


config = Config()

class Path:
    def __init__(self):
        # self.screenShot = "./screenShot/origin/"
        # self.screenShot_keys = "./screenShot/keys_" + config.phone_size + "/"

        self.__my_dict__ = r"K:\code\answer_AI_jiang\screenShot/" + config.phone_size + "/"
        self.screenShot = self.__my_dict__ + "origin/"
        self.screenShot_keys = self.__my_dict__ + "keys/"
        self.dict_answer_label = self.__my_dict__ + "answers5_label.json"
        self.dict_answer_label_cat = self.__my_dict__ + "answers5_label_catlr.json"
        self.dict_answer_label_cat_add = self.__my_dict__ + "answers5_label_catlr_add.json"

        self.__make_dir__()
        # self.__cpy_last_dict__()

    def __make_dir__(self):
        utility.mkdir(self.screenShot)
        utility.mkdir(self.screenShot_keys)
        utility.mkdir(self.__my_dict__)

    def __cpy_last_dict__(self):
        if os.path.exists(self.dict_answer_label) or os.path.exists(self.dict_answer_label_cat):
            print("Not copy.")
            return
        self.__my_dict_old__ = r"K:\code\answer_AI_jiang\screenShot/"
        self.dict_read_answer_label = self.__my_dict_old__ + "answers4_label.json"
        self.dict_read_answer_label_cat = self.__my_dict_old__ + "answers4_label_catlr.json"
        utility.cpy_list2list([self.dict_read_answer_label, self.dict_read_answer_label_cat],
                              [self.dict_answer_label, self.dict_answer_label_cat])
        print("Copy fils.")


path = Path()

if __name__ == "__main__":

    if 1:
        f = open(path.dict_answer_label_cat, "r")
        for line in f:
            answers_cat = json.loads(line)
        f.close()

        f = open(path.dict_answer_label_cat_add, "r")
        for line in f:
            answers_cat_add = json.loads(line)
        f.close()
    else:
        answers_cat = {'1':"10", "2":"20"}
        answers_cat_add = {'1':["30"]}

    for (i_key, i_value) in answers_cat.items():
        if not(i_key in answers_cat_add):
            answers_cat_add[i_key] = [i_value]
        else:
            for j_value in answers_cat_add[i_key]:
                if j_value == i_value:
                    break
            else:
                answers_cat_add[i_key].append(i_value)

    print(answers_cat)
    print(answers_cat_add)
    print(answers_cat.__len__())
    print(answers_cat_add.__len__())

    with open(path.dict_answer_label_cat_add, 'w') as outfile:
        json.dump(answers_cat_add, outfile, ensure_ascii=False)
        outfile.write('\n')



