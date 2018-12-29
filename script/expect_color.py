
import numpy as np
import cv2

image = cv2.imread(r"K:\code\answer_AI_jiang\screenShot\history\4/autojump_82.png")
image_time_bg = image[430:495, 509:576, :]
color_image_time_bg = np.average(np.average(image_time_bg, 0), 0)
print(color_image_time_bg)
print(image_time_bg)

cv2.imshow('origin', image)
cv2.imshow('tmp', image_time_bg)
cv2.waitKey()


