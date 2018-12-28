from skimage import io
import os
import numpy as np
DEBUG = 0
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
if DEBUG:
    print(BASE_DIR)
PICS_DIR = os.path.join(BASE_DIR,"..\\pics\\test_match")
if DEBUG:
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

def cal_num_scalar(image, color):
    num =0
    for loop in range(image.shape[0]):
        for loop2 in range(image.shape[1]):
            if image[loop][loop2][0] == color[0] :# and image[loop][loop2][1] == color[1] and image[loop][loop2][2] == color[2]:
                continue
            else:
                #print(image[loop][loop2][0:3])
                num = num+1
    return num

def cal_num(image, color):
    num = 0
    image_useful = image[:, :, 0] != color[0]
    num = np.sum(np.sum(image_useful))
    return int(num)

def cal_num_cat(image, color):
    if 0:
        height_split = int(image.shape[0]/3)
        num = ""
        
        for i in range(3):
        
            image_useful = image[height_split * i:height_split * (i+1), :, 0] != color[0]
            num1 = np.sum(np.sum(image_useful))
            
            num += str(num1)
        return int(np.int(num))
    else:
        width_split = int(image.shape[1]/2)
        data_str = ""
        for i in range(2):
        
            image_useful = image[:, width_split * i:width_split * (i+1), 0] != color[0]
            num = np.sum(np.sum(image_useful))
            num_str = str(num)
            if num_str.__len__() == 1:
                num_str = "0000" + num_str
            elif num_str.__len__() == 2:
                num_str = "000" + num_str
            elif num_str.__len__() == 3:
                num_str = "00" + num_str
            elif num_str.__len__() == 4:
                num_str = "0" + num_str
            elif num_str.__len__() == 5:
                pass
            else:
                assert False, "num_str length error. length: %d" % num_str.__len__()
            
            data_str += num_str
        return data_str

def cal_num1(image, color):
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
    #print("selection: ",a, sort_id)
    return sort_id

def selection_str(correct_loss, loss1, loss2, loss3, loss4):
    
    def split_str(loss):
        loss_1 = loss[0:5]
        loss_2 = loss[5:10]
        out = np.zeros(shape=(1, 2))
        out[0, 0] = int(loss_1)
        out[0, 1] = int(loss_2)
        return out
    
    a = np.concatenate([split_str(loss1), split_str(loss2), split_str(loss3), split_str(loss4)], axis=0)
    
    a = np.abs(a-split_str(correct_loss))
    
    b = np.max(a, axis=1)
    sort_id = np.argmin(b)
    # print("selection: ",b, sort_id)
    return sort_id

def selection_str_rValue(correct_loss, loss1, loss2, loss3, loss4):

    def split_str(loss):
        loss_1 = loss[0:5]
        loss_2 = loss[5:10]
        out = np.zeros(shape=(1, 2))
        try:
            out[0, 0] = int(loss_1)
            out[0, 1] = int(loss_2)
        except ValueError:
            print(loss)
            assert False, "ValueError"
        return out

    a = np.concatenate([split_str(loss1), split_str(loss2), split_str(loss3), split_str(loss4)], axis=0)

    a = np.abs(a-split_str(correct_loss))

    b = np.max(a, axis=1)
    sort_id = np.argmin(b)
    # print("selection: ",b, sort_id)
    return [sort_id, b[sort_id]]


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
