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
    print(" ")
    time_last = time_manager.print_interval(time_begin, datetime.datetime.now())
    os.system('adb shell screencap -p /sdcard/0_answer/autojump.png')
    time_last = time_manager.print_interval(time_begin, time_last)
    os.system('adb pull /sdcard/0_answer/autojump.png ./screenShot/autojump.png')
    time_last = time_manager.print_interval(time_begin, time_last)


def pull_screenshot(i_frame):

    process = subprocess.Popen('adb shell screencap -p', shell=True, stdout=subprocess.PIPE)
    screenshot = process.stdout.read()

    if sys.platform == 'win32':
        screenshot = screenshot.replace(b'\r\n', b'\n')
    f = open(path_screenShot + "autojump_%d.png" % i_frame, 'wb')
    f.write(screenshot)
    f.close()


def imshow_screen(i_frame, answers_label, has_answer, question_sum):
    pull_screenshot(i_frame)
    if 1:
        img = cv2.imread(path_screenShot + "autojump_%d.png" % i_frame)

        # press_rushNum
        if 1:
            image_begin_for_judge = img[1183:1388, 190:870]
            color_begin_for_judge = np.average(np.average(image_begin_for_judge, 0), 0)
            if color_begin_for_judge[2] > 220 \
                    and color_begin_for_judge[2] - 100 > color_begin_for_judge[0] \
                    and color_begin_for_judge[2] - 100 > color_begin_for_judge[1]:
                anser_wechat.press_rushNum()

        # press_skip
        if 1:
            image_begin_for_judge = img[1608:1750, 94:992]
            color_begin_for_judge = np.average(np.average(image_begin_for_judge, 0), 0)
            if color_begin_for_judge[2] > 220 \
                    and color_begin_for_judge[2] - 100 > color_begin_for_judge[0] \
                    and color_begin_for_judge[2] - 100 > color_begin_for_judge[1]:
                anser_wechat.press_skip()


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


        if 1:
            colors_judge_answer = np.zeros(shape=(4, 3))
            for i_key in range(4):
                image_judge_answer = img[start_top + interval_height * i_key:start_top + interval_height * i_key + box_height, 174:174 + 50, :]
                colors_judge_answer[i_key, :] = np.average(np.average(image_judge_answer, 0), 0)



        names = locals()

        # answer
        if has_answer == False:

            should_answer = True
            for i_key in range(4):
                for i_color in range(3):
                    # 4
                    if colors_judge_answer[i_key, i_color] < 246 or colors_judge_answer[i_key, i_color] > 249:
                        should_answer = False
                        break

            if should_answer == True:

                # img_question = img[1000:1215, 59:1000]
                imshow_screen.img_question = img[1054:1215, 59:1000]
                if 0:
                    imshow_screen.key_question = np.sum(np.sum(np.sum(imshow_screen.img_question)))
                else:
                    imshow_screen.key_question = match_answer.cal_num(imshow_screen.img_question, match_answer.WHITE)

                print("答题")
                if 0:
                    imshow_screen.answer_origin4 = [np.sum(np.sum(np.sum(names["img_%d" % (0 + 1)]))),
                                                    np.sum(np.sum(np.sum(names["img_%d" % (1 + 1)]))),
                                                    np.sum(np.sum(np.sum(names["img_%d" % (2 + 1)]))),
                                                    np.sum(np.sum(np.sum(names["img_%d" % (3 + 1)])))]
                else:
                    imshow_screen.answer_origin4 = [match_answer.cal_num(names["img_%d" % (0 + 1)], match_answer.GREY),
                                                    match_answer.cal_num(names["img_%d" % (1 + 1)], match_answer.GREY),
                                                    match_answer.cal_num(names["img_%d" % (2 + 1)], match_answer.GREY),
                                                    match_answer.cal_num(names["img_%d" % (3 + 1)], match_answer.GREY)]
                    # cv2.imshow('1', names["img_%d" % (0 + 1)])
                    # cv2.imshow('2', names["img_%d" % (1 + 1)])
                    # cv2.imshow('3', names["img_%d" % (2 + 1)])
                    # cv2.imshow('4', names["img_%d" % (3 + 1)])
                    # cv2.waitKey()
                    imshow_screen.image_origin4 = [names["img_%d" % (0 + 1)], names["img_%d" % (1 + 1)], names["img_%d" % (2 + 1)], names["img_%d" % (3 + 1)]]

                if str(imshow_screen.key_question) in answers_label:
                    value = answers_label[str(imshow_screen.key_question)]

                    id = match_answer.selection(value,
                                                imshow_screen.answer_origin4[0],
                                                imshow_screen.answer_origin4[1],
                                                imshow_screen.answer_origin4[2],
                                                imshow_screen.answer_origin4[3])
                    imshow_screen.my_choice = id

                    anser_wechat.press_answer(id + 1)
                    utility.print_red("choice in label: %d" % id)
                else:
                    anser_wechat.press_answer(1)
                    print("question not in dict_label.")

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


                    if i_key == imshow_screen.my_choice:
                        utility.print_red("Correct!!!")
                        question_sum.append(1)
                    else:
                        question_sum.append(0)


                    cv2.imwrite(path.screenShot_keys + "question_%d.png" % imshow_screen.num_question, imshow_screen.img_question, [int(cv2.IMWRITE_PNG_COMPRESSION), 0])
                    cv2.imwrite(path.screenShot_keys + "answer_%d.png" % imshow_screen.num_question, imshow_screen.image_origin4[i_key], [int(cv2.IMWRITE_PNG_COMPRESSION), 0])
                    # cv2.imwrite(path.screenShot_keys + "answer_%d.png" % imshow_screen.num_question, names["img_%d" % (i_key + 1)], [int(cv2.IMWRITE_PNG_COMPRESSION), 0])

                    imshow_screen.num_question += 1

                    value = imshow_screen.answer_origin4[i_key]

                    answers_label[str(imshow_screen.key_question)] = value

                    print("题库label大小：%d" % answers_label.__len__())
                    if 1:


                        with open(path.dict_answer_label, 'w') as outfile:
                            json.dump(answers_label, outfile, ensure_ascii=False)
                            outfile.write('\n')

                    time.sleep(0.5 * 1)

                    has_answer = False

                    break

    return has_answer


if __name__ == "__main__":
    class Config:
        def __init__(self):
            self.image_size = (1080, 1920)
    config = Config()

    class Path:
        def __init__(self):
            self.screenShot = "./screenShot/4/"
            self.screenShot_keys = "./screenShot/4_keys/"
            self.dict_answer = "K:/code/answer_AI/screenShot/answers4_smallImage.json"
            self.dict_answer_label = "K:/code/answer_AI/screenShot/answers4_label.json"

            self.__make_dir__()
        def __make_dir__(self):
            utility.mkdir(self.screenShot)
            utility.mkdir(self.screenShot_keys)
    path = Path()

    path_screenShot = path.screenShot

    time_manager = utility.TimeManager()
    time_begin = datetime.datetime.now()
    time_last = time_begin

    # try:
    #     f=open(path.dict_answer,"r")
    #     for line in f:
    #         answers=json.loads(line)
    #     f.close()
    # except:
    #     print("题库不存在，创建题库。")
    #     answers = {}
    try:
        f=open(path.dict_answer_label,"r")
        for line in f:
            answers_label=json.loads(line)
        f.close()
    except:
        print("label不存在，创建题库。")
        answers_label = {}

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
            imshow_screen.num_question = 207
            has_answer = False
            question_sum = []
            correct_change = []
            while 1:
                has_answer = imshow_screen(i_frmae, answers_label, has_answer, question_sum)
                i_frmae = np.mod(i_frmae + 1, 1000)
                if np.mod(question_sum.__len__(), 100) == 0 and question_sum.__len__() > 100:
                    sum_correct = 0
                    for i in range(1, 100):
                        sum_correct += question_sum[-i]
                    utility.print_red("正确率：%.2f" % (sum_correct / 100))
                    correct_change.append((sum_correct / 100))
                    print(correct_change)
                # time_last = time_manager.print_interval(time_begin, time_last)
    thread1 = MyThread(1, "Thread-1")
    thread1.start()


    class Phone:
        def __init__(self):
            pass


        def tap(self, x, y):
            cmd = 'adb shell input tap %d %d' % (x, y)
            os.system(cmd)

        def press_key(self, key):
            cmd = 'adb shell input keyevent 3'
            print(cmd)
            os.system(cmd)
    phone = Phone()

    class AnswerWechat:
        def __init__(self):
            pass


        def return_last_UI(self):
            phone.tap(56, 140)
            print("返回")


        def press_skip(self):
            # phone.tap(551, 1843)
            phone.tap(56, 140)
            print("跳过")


        def press_beginAnswer(self):
            phone.tap(556, 1331)
            print("开始答题")


        def press_rushNum(self):
            phone.tap(556, 1428)
            print("开始答题")


        def press_again(self):
            phone.tap(551, 1683)
            print("再来一局")


        def press_answer(self, id_answer):
            if id_answer == 1:
                phone.tap(530, 1297)
            elif id_answer == 2:
                phone.tap(530, 1467)
            elif id_answer == 3:
                phone.tap(530, 1645)
            elif id_answer == 4:
                phone.tap(530, 1814)
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
