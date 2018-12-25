# -*- coding: utf-8 -*-
import os
import time
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.animation as animation
from PIL import Image

VERSION = "1.1.4"


def pull_screenshot():
    os.system('adb shell screencap -p /sdcard/autojump.png')
    os.system('adb pull /sdcard/autojump.png .')


def imshow_screen():
    pull_screenshot()
    img = np.array(Image.open('autojump.png'))
    im = plt.imshow(img, animated=True)
    plt.show()


def tap(x, y):
    cmd = 'adb shell input tap %d %d' % (x, y)
    print(cmd)
    os.system(cmd)


def press_key(key):
    cmd = 'adb shell input keyevent 3'
    print(cmd)
    os.system(cmd)


# fig = plt.figure()

imshow_screen()

while 1:
    # coordinate = input("Input coordinate: ")
    # coordinate_num = coordinate.split(' ')
    # x = np.int32(coordinate_num[0])
    # y = np.int32(coordinate_num[1])
    # tap(x, y)

    press_key(1)

    imshow_screen()
