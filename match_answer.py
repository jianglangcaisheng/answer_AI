from skimage import io
import os
import numpy as np

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
print(BASE_DIR)
PICS_DIR = os.path.join(BASE_DIR,"..\\pics\\test_match")
print(PICS_DIR)

GREY = [247, 247, 247]
GREEN = [148, 211, 77]
WHITE = [255, 255, 255]

vertex_top = 1233
vertex_left = 174
box_width_all = 735
box_height_all = 112
start_top = 1257
start_left = 352
box_width = int(735 / 2)
box_height = int(112 * 2/3)
interval_height = int((1738 - 1233) / 3)

question_pos = [1054, 1215, 59, 1000]

def crop_answer(whole_img):
    answer_1 = whole_img[start_top+interval_height*0:start_top+box_height+interval_height*0, start_left:start_left+box_width, 0:3]
    answer_2 = whole_img[start_top+interval_height*1:start_top+box_height+interval_height*1, start_left:start_left+box_width, 0:3]
    answer_3 = whole_img[start_top+interval_height*2:start_top+box_height+interval_height*2, start_left:start_left+box_width, 0:3]
    answer_4 = whole_img[start_top+interval_height*3:start_top+box_height+interval_height*3, start_left:start_left+box_width, 0:3]
    return answer_1, answer_2, answer_3, answer_4


def cal_num(image, color):
    num =0
    for loop in range(image.shape[0]):
        for loop2 in range(image.shape[1]):
            if sum(image[loop][loop2][0:3] == color) == 3:
                continue
            else:
                #print(image[loop][loop2][0:3])
                num = num+1
    return num

def selection(correct_loss, loss1, loss2, loss3, loss4):
    a = np.array([loss1, loss2, loss3, loss4])
    a = np.abs(a-correct_loss)
    sort_id = np.argmin(a)
    print("selection: ",a, sort_id)
    return sort_id


if __name__ == "__main__":
    #img_label_green_2 = io.imread(os.path.join(PICS_DIR,"answer_1.png"))
    #img_question = io.imread(os.path.join(PICS_DIR,"question_0.png"))
    #img_question_2 = io.imread(os.path.join(PICS_DIR,"question_1.png"))
    #img_whole_green = io.imread(os.path.join(PICS_DIR,"autojump_1.png"))


    ##raw grey image
    img_whole_grey = io.imread(os.path.join(PICS_DIR,"autojump_0.png"))
    ##crop question and answer,and get descriptor
    question = img_whole_grey[question_pos[0]:question_pos[1], question_pos[2]:question_pos[3],0:3]
    correct_question = cal_num(question, WHITE)

    ## another raw image
    img_whole_grey = io.imread(os.path.join(PICS_DIR,"autojump_1.png"))
    ##crop question and answer,and get descriptor
    question_new = img_whole_grey[question_pos[0]:question_pos[1], question_pos[2]:question_pos[3],0:3]
    correct_question_new = cal_num(question, WHITE)
    #########
    io.imshow(question-question_new)

    answer_1, answer_2, answer_3, answer_4 = crop_answer(img_whole_grey)
    loss1 = cal_num(answer_1, GREY)
    loss2 = cal_num(answer_2, GREY)
    loss3 = cal_num(answer_3, GREY)
    loss4 = cal_num(answer_4, GREY)

    ##calculate library's key value(questions')
    img_question = io.imread(os.path.join(PICS_DIR,"question_0.png"))
    loss_ques = cal_num(img_question, WHITE)

    correct_answer = io.imread(os.path.join(PICS_DIR,"answer_0.png"))
    correct_loss = cal_num(correct_answer, GREEN)

    id = selection(correct_loss, loss1, loss2, loss3, loss4)
    print(id)

    #i=3
    #img_label_grey_first = img_whole_grey[start_top+interval_height*i:start_top+box_height+interval_height*i, start_left:start_left+box_width, 0:3]
    #img_label_grey_second = img_whole_green[start_top+interval_height*i:start_top+box_height+interval_height*i, start_left:start_left+box_width, 0:3]
    #io.imshow(-img_label_grey_second+img_label_grey_first)
    #io.imshow(img_label_grey_second-img_label_grey_first)

    #label_num_pixel = cal_num(img_label_green, GREEN)
    #print("LABEL_NUM_PIXEL: ", label_num_pixel)
    #
    #
    #label_num_pixel_2 = cal_num(img_label_green_2, GREEN)
    #print("LABEL_NUM_PIXEL_2: ", label_num_pixel_2)
    #
    #label_num_pixel_3 = cal_num(img_label_green_3, GREEN)
    #print("LABEL_NUM_PIXEL_3: ", label_num_pixel_3)
    #
    #Q_num_pixel = cal_num(img_question, WHITE)
    #print("Q_NUM_PIXEL: ", Q_num_pixel)
    #
    #label_num_pixel_grey = cal_num(img_label_grey, GREY)
    #print("LABEL_NUM_PIXEL_GREY: ", label_num_pixel_grey)
    #
    #label_num_pixel_grey_first = cal_num(img_label_grey_first, GREY)
    #print("LABEL_NUM_PIXEL_GREY_F: ", label_num_pixel_grey_first)
    #
    #label_num_pixel_grey_second = cal_num(img_label_grey_second, GREEN)
    #print("LABEL_NUM_PIXEL_GREY_S: ", label_num_pixel_grey_second)
