import cv2
import numpy as np
from tensorflow.keras.models import load_model
import imutils
from solver import *
import os

# As we are trying to predict any number from 1-9, we create an array containing 0 to 9
CLASSES = np.arange(0,10)

# Load pre-trained model to predict all digits
MODEL = load_model('model-OCR.h5')

INPUT = 48

# Find the sudoku board within an image
def find_board(img):
    ## Convert image into a grayscale
    img_grayed = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    ## Removes noise
    img_cleaned = cv2.bilateralFilter(img_grayed, 13, 20, 20)
    ## Detect the edges in the image using Hysteresis Thresholding
    img_edges = cv2.Canny(img_cleaned, 30, 180)
    ## Detect all the continuous points within the edges detected previously
    keypoints = cv2.findContours(img_edges.copy(), cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)
    ## Grab the contour coordinates using imutils
    contours = imutils.grab_contours(keypoints)
    ### Outline all the contours
    #newimg = cv2.drawContours(img.copy(), contours, -1, (0, 255, 0), 3)
    #cv2.imshow("Contours", newimg)
    ## Sort to prioritise larger objects
    contours = sorted(contours, key=cv2.contourArea, reverse=True)[:15]
    location = None
    ## Finds rectangular contour
    for contour in contours:
        ## Simplify contours with the epsilon value
        approx = cv2.approxPolyDP(contour, 15, True)
        ## If there are 4 vertices, then save the approximate coordinates 
        if len(approx) == 4:
            location = approx
            break
    result = get_perspective(img, location)
    return result, location

# Takes the image of the board and return it with a perspective transformation.
def get_perspective(source_img, location, dest_height = 900, dest_width = 900):
    source_coordinates = np.float32([location[0], location[3], location[1], location[2]])
    # Check if the board is too small
    area_size = calculate_quadArea(source_coordinates)
    if area_size < 4500:
        raise Exception
    destination_coordinates = np.float32([[0, 0], [dest_width, 0], [0, dest_height], [dest_width, dest_height]])
    ## Utilize Perspective Transform Algorithm
    matrix = cv2.getPerspectiveTransform(source_coordinates, destination_coordinates)
    trans_img = cv2.warpPerspective(source_img, matrix, (dest_width, dest_height))
    return trans_img

def calculate_quadArea(source_coordinates):
    # Brahmaguptas Formula
    a = source_coordinates[1][0]
    b = source_coordinates[3][0]
    c = source_coordinates[2][0]
    d = source_coordinates[0][0]
    AB = calculate_length(a,b)
    BC = calculate_length(b,c)
    CD = calculate_length(c,d)
    DA = calculate_length(d,a)

    semip = (AB + BC + CD + DA)/2
    area = ((semip-AB)*(semip-BC)*(semip-CD)*(semip-DA))**0.5
    return round(area,2)

def calculate_length(coordinate1,coordinate2):
    return ((coordinate2[0] - coordinate1[0])**2 + (coordinate2[1] - coordinate1[1])**2)**0.5
    

# Splits the sudoku board into the individual numbers
def split_boxes(board):
    ## Split the image vertically by 9 contours
    rows = np.vsplit(board,9)
    boxes = []
    for r in rows:
        ## Split the image horizontally
        cols = np.hsplit(r,9)
        for box in cols:
            box = cv2.resize(box, (INPUT, INPUT))/255.0
            #cv2.imshow("Splitted block", box)
            #cv2.waitKey(50)
            boxes.append(box)
    
    return boxes

def displayNumbers(img, numbers, color=(255,0,255)):
    W = int(img.shape[1]/9)
    H = int(img.shape[0]/9)
    for i in range (9):
        for j in range (9):
            if numbers[(j*9)+i] != 0:
                ## cv2.putText(image, text, where, font, font-size, color, line-thickness, line-type)
                cv2.putText(img, str(numbers[(j*9)+i]), (i*W+int(W/2)-int((W/4)),int((j+0.7)*H)),cv2.FONT_HERSHEY_COMPLEX,2,color,2,cv2.LINE_AA)
    return img

# Returns the image to its original perspective
def get_InvPerspective(trans_img, masked_num, location, trans_height = 900, trans_width = 900):
    trans_coordinates = np.float32([[0, 0], [trans_width, 0], [0, trans_height], [trans_width, trans_height]])
    original_coordinates = np.float32([location[0], location[3], location[1], location[2]])

    matrix = cv2.getPerspectiveTransform(trans_coordinates, original_coordinates)
    reverted_img = cv2.warpPerspective(masked_num, matrix, (trans_img.shape[1],trans_img.shape[0]))
    return reverted_img

def orientateImg(actual_image, pathToFile, def_height=368, def_width=490):
    img = cv2.imread(os.path.join(pathToFile, actual_image))
    height, width, channels = img.shape

    if height > def_height or width > def_width:
        height_diff = height - def_height
        width_diff = width - def_width
        if height_diff >= width_diff:
            ratio = def_height / height
            height = def_height
            width = int(ratio * width)
        else:
            ratio = def_width / width
            height = int(ratio * height)
            width = def_width
        dim = (width, height)
        img = cv2.resize(img, dim, interpolation = cv2.INTER_AREA)
        # print(f"New:\n   Height: {height}\n   Width: {width}")
    return img
    
def findNum(img):
    # Find image and location of the board
    board, location = find_board(img)
    #cv2.imshow("Board", board)

    # Convert board to grayscale
    gray = cv2.cvtColor(board, cv2.COLOR_BGR2GRAY)
    splitted_boxes = split_boxes(gray)
    splitted_boxes = np.array(splitted_boxes).reshape(-1, INPUT, INPUT, 1)
    #cv2.waitKey()

    # Predict numbers
    prediction = MODEL.predict(splitted_boxes)
    #print(prediction)

    predicted_numbers = []
    # get the classes variable which will contain the different range of numbesr to be selected
    for i in prediction:
        index = (np.argmax(i))
        predicted_number = CLASSES[index]
        predicted_numbers.append(predicted_number)

    # Reshape the array from a 1D flat list into a 9x9 2D matrix
    board_num = np.array(predicted_numbers).astype('uint8').reshape(9,9)
    return board, location, predicted_numbers, board_num



def solveSudokuImg(actual_image, pathToFile="input"):
    try:
        # Orientate image
        if actual_image[-4:] != '.jpg' and actual_image[-5:] != '.jpeg':
            raise Exception
        img = orientateImg(actual_image, pathToFile)
        try:
            # Find board locations and predicted numbers
            board, location, predicted_numbers, board_num = findNum(img)
            try: 
                solved_board_nums = get_board(board_num)

                # create a binary array indicating which parts are unsolved and which have a given number.
                binArr = np.where(np.array(predicted_numbers)>0,0,1)
                #print(binArr)
                ## Fetch the solved number from the board
                flat_solved_board_nums = solved_board_nums.flatten()*binArr
                ## Create a mask for the board
                mask = np.zeros_like(board)
                ## Show the numbers in the mask
                solved_board_mask = displayNumbers(mask, flat_solved_board_nums)
                #cv2.imshow("Solved Mask", solved_board_mask)
                ## Revert perspective
                inv = get_InvPerspective(img, solved_board_mask, location)
                #cv2.imshow("Inverse Perspective", inv)
                ## 
                combined = cv2.addWeighted(img, 0.6, inv, 1, 0)
                #cv2.imshow("Final result", combined)
                cv2.imwrite(os.path.join("Output", "Result-" + actual_image), combined)
                # cv2.waitKey(0)
                cv2.destroyAllWindows()
                return "Solution found and returned."
            except:
                return "Solution doesn't exist. Or Model misread digits."
        except:
            return "Board detected is too small or does not exist."
    except:
        return "Invalid file. Please upload an jpg image file."
    
    


def test():
    solveSudokuImg('unsolvable.jpg',pathToFile="testInput")



if __name__ == "__main__":
    test()