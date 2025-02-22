# -*- coding: utf-8 -*-
import os, sys
import time
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.animation as animation
from PIL import Image
import cv2
import datetime
import subprocess
import threading
import json

import utility
import resource as rc
import match_answer


def pull_screenshot_imgOnPhone(i_frame):
    #time_last = time_manager.print_interval(time_begin, datetime.datetime.now())
    os.system('adb shell screencap -p /sdcard/0_answer/autojump.png')
    #time_last = time_manager.print_interval(time_begin, time_last)
    # os.system("adb pull /sdcard/0_answer/autojump.png " + path_screenShot + "autojump_%s.png" % datetime.datetime.now().strftime("hhmmss"))
    os.system("adb pull /sdcard/0_answer/autojump.png " + path_screenShot + "autojump_%d.png" % i_frame)
    # os.system("adb pull /sdcard/0_answer/autojump.png " + "./screenShot/4/autojump_%d.png" % i_frame)
    #time_last = time_manager.print_interval(time_begin, time_last)


def pull_screenshot(i_frame):

    process = subprocess.Popen('adb shell screencap -p', shell=True, stdout=subprocess.PIPE)
    screenshot = process.stdout.read()

    if sys.platform == 'win32':
        screenshot = screenshot.replace(b'\r\n', b'\n')
    f = open(path_screenShot + "autojump_%d.png" % i_frame, 'wb')
    f.write(screenshot)
    f.close()


def pull_screenshot_image():

    process = subprocess.Popen('adb shell screencap -p', shell=True, stdout=subprocess.PIPE)
    screenshot = process.stdout.read()

    if sys.platform == 'win32':
        screenshot = screenshot.replace(b'\r\n', b'\n')
    return screenshot


def imshow_screen(i_frame, answers_label, answers_cat, answers_cat_add, has_answer, question_sum):
    flag = False

    time_last = datetime.datetime.now()

    # get image
    if 0:
        pull_screenshot_imgOnPhone(i_frame)
        img = cv2.imread(path_screenShot + "autojump_%d.png" % i_frame)
    elif 0:
        pull_screenshot(i_frame)
        img = cv2.imread(path_screenShot + "autojump_%d.png" % i_frame)
    else:
        img_str = pull_screenshot_image()
        if 1:
            nparr = np.fromstring(img_str, dtype="uint8")
        else:
            nparr = np.asarray(bytearray(img_str), dtype="uint8")

        img = cv2.imdecode(nparr, cv2.IMREAD_COLOR)

        # 0.7s
        if 0:
            print("Time of get image")
            time_last = time_manager.print_interval(begin_time=time_begin, last_time=time_last)

    # press_rushNum
    if 1:
        image_begin_for_judge = img[1183:1388, 190:870]
        color_begin_for_judge = np.average(np.average(image_begin_for_judge, 0), 0)
        if color_begin_for_judge[2] > phone.redth \
                and color_begin_for_judge[2] - phone.reden > color_begin_for_judge[0] \
                and color_begin_for_judge[2] - phone.reden > color_begin_for_judge[1]:
            anser_wechat.press_rushNum()

    # press_skip
    if 1:
        image_begin_for_judge = img[1608:1750, 94:992]
        color_begin_for_judge = np.average(np.average(image_begin_for_judge, 0), 0)
        if color_begin_for_judge[2] > 220 \
                and color_begin_for_judge[2] - 100 > color_begin_for_judge[0] \
                and color_begin_for_judge[2] - 100 > color_begin_for_judge[1]:

            cv2.imwrite(path.screenShot_result + "%s.jpg" % (datetime.datetime.now().strftime('%m%d_%H%M%S')), img)

            flag = anser_wechat.press_skip()

    vertex_top = 1233
    vertex_left = 174

    box_width_all = 735
    box_height_all = 112

    start_top = 1257
    start_left = 352

    box_width = int(735 / 2)
    box_height = int(112 * 2/3)

    interval_height = int((1738 - 1233) / 3)
    interval_height = 168

    def get_color(id, top, left, height, width):
        image_local = img[top+interval_height*id:top+interval_height*id+height, left:left+width]
        return np.average(np.average(image_local, 0), 0)


    colors = np.zeros(shape=(4, 3))
    img_1 = img[start_top + interval_height * 0:start_top + interval_height * 0 + box_height,
            start_left:start_left + box_width]
    colors[0, :] = np.average(np.average(img_1, 0), 0)
    img_2 = img[start_top + interval_height * 1:start_top + interval_height * 1 + box_height,
            start_left:start_left + box_width]
    colors[1, :] = np.average(np.average(img_2, 0), 0)
    img_3 = img[start_top + interval_height * 2:start_top + interval_height * 2 + box_height,
            start_left:start_left + box_width]
    colors[2, :] = np.average(np.average(img_3, 0), 0)
    img_4 = img[start_top + interval_height * 3:start_top + interval_height * 3 + box_height,
            start_left:start_left + box_width]
    colors[3, :] = np.average(np.average(img_4, 0), 0)

    names = locals()

    # answer
    if has_answer == False:

        # 是否答题
        should_answer = True

        colors_judge_answer = np.zeros(shape=(4, 3))
        for i_key in range(4):
            image_judge_answer = img[start_top + interval_height * i_key:start_top + interval_height * i_key + box_height, 174:174 + 50, :]
            colors_judge_answer[i_key, :] = np.average(np.average(image_judge_answer, 0), 0)

        for i_key in range(4):
            for i_color in range(3):
                if colors_judge_answer[i_key, i_color] < 246 or colors_judge_answer[i_key, i_color] > 249:
                    should_answer = False
                    break

        image_time_bg = img[451:476, 526:571, :]
        color_image_time_bg = np.average(np.average(image_time_bg, 0), 0)
        if not(color_image_time_bg[0] > 229 and color_image_time_bg[0] < 239
               and color_image_time_bg[1] > 228 and color_image_time_bg[1] < 238
               and color_image_time_bg[2] > 248 and color_image_time_bg[2] < 258):
            pass

        if should_answer == True:

            # img_question = img[1000:1215, 59:1000]
            imshow_screen.img_question = img[1054:1215, 59:1000]
            if 1:
                imshow_screen.key_question = match_answer.cal_num(imshow_screen.img_question, match_answer.WHITE)
                imshow_screen.key_question2 = match_answer.cal_num_cat(imshow_screen.img_question, match_answer.WHITE)
                print(imshow_screen.key_question2, end=" ")

            print("答题: ", end="")

            # calcu question
            if 1:
                imshow_screen.answer_origin4 = [match_answer.cal_num(names["img_%d" % (0 + 1)], match_answer.GREY),
                                                match_answer.cal_num(names["img_%d" % (1 + 1)], match_answer.GREY),
                                                match_answer.cal_num(names["img_%d" % (2 + 1)], match_answer.GREY),
                                                match_answer.cal_num(names["img_%d" % (3 + 1)], match_answer.GREY)]
                imshow_screen.answer_origin42 = [match_answer.cal_num_cat(names["img_%d" % (0 + 1)], match_answer.GREY),
                                                match_answer.cal_num_cat(names["img_%d" % (1 + 1)], match_answer.GREY),
                                                match_answer.cal_num_cat(names["img_%d" % (2 + 1)], match_answer.GREY),
                                                match_answer.cal_num_cat(names["img_%d" % (3 + 1)], match_answer.GREY)]

                imshow_screen.image_origin4 = [names["img_%d" % (0 + 1)], names["img_%d" % (1 + 1)], names["img_%d" % (2 + 1)], names["img_%d" % (3 + 1)]]

            my_answer_output = []
            if str(imshow_screen.key_question2) in answers_cat_add:
                value_list = answers_cat_add[str(imshow_screen.key_question2)]

                value_id_min = 9999999999
                id_best = 0
                for value in value_list:

                    [id, value_id] = match_answer.selection_str_rValue(value,
                                                imshow_screen.answer_origin42[0],
                                                imshow_screen.answer_origin42[1],
                                                imshow_screen.answer_origin42[2],
                                                imshow_screen.answer_origin42[3])
                    if value_id < value_id_min:
                        value_id_min = value_id
                        id_best = id

                my_answer_output.append(id_best)

            imshow_screen.is_key_in_dict3 = False
            if str(imshow_screen.key_question2) in answers_cat:
                imshow_screen.is_key_in_dict3 = True

                value = answers_cat[str(imshow_screen.key_question2)]

                id = match_answer.selection_str(value,
                                            imshow_screen.answer_origin42[0],
                                            imshow_screen.answer_origin42[1],
                                            imshow_screen.answer_origin42[2],
                                            imshow_screen.answer_origin42[3])
                my_answer_output.append(id)

            if str(imshow_screen.key_question) in answers_label:
                value = answers_label[str(imshow_screen.key_question)]

                id = match_answer.selection(value,
                                            imshow_screen.answer_origin4[0],
                                            imshow_screen.answer_origin4[1],
                                            imshow_screen.answer_origin4[2],
                                            imshow_screen.answer_origin4[3])
                my_answer_output.append(id)

            if my_answer_output.__len__() > 0:

                if 0:
                    # print("before press_answer")
                    time_last = time_manager.print_interval(time_begin, time_last)

                anser_wechat.press_answer(my_answer_output[0] + 1)

                if 0:
                    print("Time of press_answer")
                    time_last = time_manager.print_interval(time_begin, time_last)

                print(my_answer_output, end=" ")
                imshow_screen.my_choice = my_answer_output[0]

            else:
                imshow_screen.my_choice = -1
                anser_wechat.press_answer(1)
                utility.print_red("question not in dict_label.")

            cv2.imwrite(path.screenShot + "%s_q_%s.jpg" % (imshow_screen.key_question2, datetime.datetime.now().strftime('%m%d_%H%M')), img)

            has_answer = True
        else:
            print(".", end="")


    # save answer
    if has_answer == True:
        for i_key in range(4):
            color_judge_saveAnswer = get_color(id=i_key, top=1743 - interval_height * 3, left=269, height=20, width=20)

            if ((color_judge_saveAnswer[1] > 200)
                and (color_judge_saveAnswer[1] - 100 > color_judge_saveAnswer[0])
                and (color_judge_saveAnswer[1] - 50 > color_judge_saveAnswer[2])):


                if hasattr(imshow_screen, 'my_choice') and i_key == imshow_screen.my_choice:
                    question_sum.append(1)
                    if imshow_screen.is_key_in_dict3 == False:
                        if not (str(imshow_screen.key_question2) in answers_cat_add):
                            value = imshow_screen.answer_origin42[i_key]
                            answers_cat_add[str(imshow_screen.key_question2)] = [value]

                            print("题库label大小：%d" % answers_label.__len__())
                            print("题库cat大小：%d" % answers_cat.__len__())
                            print("题库cat_add大小：%d" % answers_cat_add.__len__())

                            with open(path.dict_answer_label_cat_add, 'w') as outfile:
                                json.dump(answers_cat_add, outfile, ensure_ascii=False)
                                outfile.write('\n')
                else:
                    utility.print_red("\ncorrect_answer: %d" % i_key)
                    question_sum.append(0)

                    value = imshow_screen.answer_origin4[i_key]
                    answers_label[str(imshow_screen.key_question)] = value
                    value = imshow_screen.answer_origin42[i_key]
                    answers_cat[str(imshow_screen.key_question2)] = value
                    if str(imshow_screen.key_question2) in answers_cat_add:
                        answers_cat_add[str(imshow_screen.key_question2)].append(value)
                    else:
                        answers_cat_add[str(imshow_screen.key_question2)] = [value]
                    print("题库label大小：%d" % answers_label.__len__())
                    print("题库cat大小：%d" % answers_cat.__len__())
                    print("题库cat_add大小：%d" % answers_cat_add.__len__())
                    print("dict: ")
                    print(answers_cat_add[str(imshow_screen.key_question2)])

                    # write dict
                    if 1:
                        with open(path.dict_answer_label, 'w') as outfile:
                            json.dump(answers_label, outfile, ensure_ascii=False)
                            outfile.write('\n')
                        with open(path.dict_answer_label_cat, 'w') as outfile:
                            json.dump(answers_cat, outfile, ensure_ascii=False)
                            outfile.write('\n')
                        with open(path.dict_answer_label_cat_add, 'w') as outfile:
                            json.dump(answers_cat_add, outfile, ensure_ascii=False)
                            outfile.write('\n')

                    # imwrite
                    class ImageWrite:
                        def __init__(self, format):
                            self.format = format

                        def imwrite(self):
                            if self.format == ".png":
                                cv2.imwrite(path.screenShot_keys + "%s_q_%s.png" % (imshow_screen.key_question2, datetime.datetime.now().strftime('%m%d_%H%M')),
                                            imshow_screen.img_question, [int(cv2.IMWRITE_PNG_COMPRESSION), 0])
                                cv2.imwrite(path.screenShot_keys + "%s_a_%s.png" % (imshow_screen.key_question2, datetime.datetime.now().strftime('%m%d_%H%M')),
                                            imshow_screen.image_origin4[i_key], [int(cv2.IMWRITE_PNG_COMPRESSION), 0])
                                # cv2.imwrite(path.screenShot_keys + "answer_%d.png" % imshow_screen.num_question,
                                #             names["img_%d" % (i_key + 1)], [int(cv2.IMWRITE_PNG_COMPRESSION), 0])
                            elif self.format == ".jpg":
                                cv2.imwrite(path.screenShot_keys + "%s_q_%s.jpg" % (imshow_screen.key_question2, datetime.datetime.now().strftime('%m%d_%H%M')),
                                            imshow_screen.img_question)
                                cv2.imwrite(path.screenShot_keys + "%s_a_%s.jpg" % (imshow_screen.key_question2, datetime.datetime.now().strftime('%m%d_%H%M')),
                                            imshow_screen.image_origin4[i_key])
                                # cv2.imwrite(path.screenShot_keys + "answer_%d.jpg" % imshow_screen.num_question, names["img_%d" % (i_key + 1)])
                    image_write = ImageWrite(".jpg")
                    image_write.imwrite()

                has_answer = False
                break

    return has_answer, flag


if __name__ == "__main__":
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
            self.screenShot_result = self.__my_dict__ + "result2/"
            self.dict_answer_label = self.__my_dict__ + "answers5_label.json"
            self.dict_answer_label_cat = self.__my_dict__ + "answers5_label_catlr.json"
            self.dict_answer_label_cat_add = self.__my_dict__ + "answers5_label_catlr_add.json"

            self.__make_dir__()
            # self.__cpy_last_dict__()


        def __make_dir__(self):
            utility.mkdir(self.screenShot)
            utility.mkdir(self.screenShot_keys)
            utility.mkdir(self.screenShot_result)
            utility.mkdir(self.__my_dict__)



        def __cpy_last_dict__(self):
            if os.path.exists(self.dict_answer_label) or os.path.exists(self.dict_answer_label_cat):
                print("Not copy.")
                return
            self.__my_dict_old__ = r"K:\code\answer_AI_jiang\screenShot/"
            self.dict_read_answer_label = self.__my_dict_old__ + "answers4_label.json"
            self.dict_read_answer_label_cat = self.__my_dict_old__ + "answers4_label_catlr.json"
            utility.cpy_list2list([self.dict_read_answer_label, self.dict_read_answer_label_cat], [self.dict_answer_label, self.dict_answer_label_cat])
            print("Copy fils.")

    path = Path()

    path_screenShot = path.screenShot

    time_manager = utility.TimeManager()
    time_begin = datetime.datetime.now()
    time_last = time_begin
    try:
        f=open(path.dict_answer_label,"r")
        for line in f:
            answers_label=json.loads(line)
        f.close()
    except:
        print("label不存在，创建题库。")
        answers_label = {}

    try:
        f=open(path.dict_answer_label_cat,"r")
        for line in f:
            answers_cat=json.loads(line)
        f.close()
    except:
        print("题库不存在，创建题库。")
        answers_cat = {}

    try:
        f=open(path.dict_answer_label_cat_add,"r")
        for line in f:
            answers_cat_add=json.loads(line)
        f.close()
    except:
        print("题库不存在，创建题库。")
        answers_cat_add = {}

    class MyThread(threading.Thread):
        def __init__(self, threadID, name):
            threading.Thread.__init__(self)
            self.threadID = threadID
            self.name = name

        def run(self):
            # utility.mkdir(path_screenShot)
            print("开始截屏")
            time_last = datetime.datetime.now()
            i_frmae = 0
            # imshow_screen.num_question = 263
            has_answer = False
            question_sum = []
            correct_change = []
            show_rate_per = 20
            show_per_cycle = int(show_rate_per / 5)
            show_per_cycle_i = 0
            while 1:
                has_answer, flag = imshow_screen(i_frmae, answers_label, answers_cat, answers_cat_add ,has_answer, question_sum)
                i_frmae = np.mod(i_frmae + 1, 1000)
                if flag == True:
                    if question_sum.__len__() >= show_rate_per:
                        print("show_per_cycle_i: %d" % show_per_cycle_i)
                        print("np.mod(show_per_cycle_i, show_per_cycle): %d" % np.mod(show_per_cycle_i, show_per_cycle))
                        if np.mod(show_per_cycle_i, show_per_cycle) == 0:
                            show_per_cycle_i += 1
                            sum_correct = 0
                            for i in range(1, show_rate_per + 1):
                                sum_correct += question_sum[-i]
                            correct_change.append((sum_correct / show_rate_per))
                            print("correct rate: ", end=" ")
                            utility.print_red(str(correct_change))

    thread1 = MyThread(1, "Thread-1")
    thread1.start()


    class Phone:
        def __init__(self, size):
            if size == "Mi_note3":
                self.redth = 220
                self.reden = 100
            if size == "Mi_redPro":
                self.redth = 220
                self.reden = 80


        def tap(self, x, y):
            cmd = 'adb shell input tap %d %d' % (x, y)
            os.system(cmd)

        def press_key(self, key):
            cmd = 'adb shell input keyevent 3'
            print(cmd)
            os.system(cmd)
    phone = Phone(config.phone_size)

    class AnswerWechat:
        def __init__(self):
            pass


        def press_rushNum(self):
            phone.tap(556, 1428)
            print("\n开始冲榜", end=": ")


        def press_beginAnswer(self):
            phone.tap(556, 1331)
            print("开始答题")


        def press_answer(self, id_answer):
            if id_answer == 1:
                phone.tap(530, 1297)
            elif id_answer == 2:
                phone.tap(530, 1467)
            elif id_answer == 3:
                phone.tap(530, 1645)
            elif id_answer == 4:
                phone.tap(530, 1814)


        def press_skip(self):
            # phone.tap(551, 1843)
#            assert False, "exit"
            phone.tap(56, 140)
            # print("\n跳过")
            return True


        def press_again(self):
            phone.tap(551, 1683)
            print("再来一局")


        def return_last_UI(self):
            phone.tap(56, 140)
            print("返回")
    anser_wechat = AnswerWechat()


    while 1:
        # coordinate = input("Input coordinate: ")
        # coordinate_num = coordinate.split(' ')
        # x = np.int32(coordinate_num[0])
        # y = np.int32(coordinate_num[1])
        if 0:
            input_str = input("1, 2, 3, 4. 0 begin, 9 skip")
            input_num = np.int32(input_str)
            if input_num in [1, 2, 3, 4]:
                anser_wechat.press_answer(input_num)
        if 0:
            input_str = input("0: stop")
            input_num = np.int32(input_str)
            if input_num == 0:
                exit('0')
