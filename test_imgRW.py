from imgRW import *

def test_can_board_be_read_as_too_small_correctly_case1():
    pass

def test_can_board_be_read_as_too_small_correctly_case2():
    pass

def test_can_board_be_right_sized_correctly_case1():
    pass

def test_can_board_be_right_sized_correctly_case2():
    pass


def test_can_img_be_read_correctly_case1():
    img = orientateImg("sudokuImg0.jpg", "testInput")
    board_num_solution = np.array([
        [3,0,0,8,0,1,0,0,2],
        [2,0,1,0,3,0,6,0,4],
        [0,0,0,2,0,4,0,0,0],
        [8,0,9,0,0,0,1,0,6],
        [0,6,0,0,0,0,0,5,0],
        [7,0,2,0,0,0,4,0,9],
        [0,0,0,5,0,9,0,0,0],
        [9,0,4,0,8,0,7,0,5],
        [6,0,0,1,0,7,0,0,3]
        ])
    board, location, predicted_numbers, board_num = findNum(img)
    assert (board_num == board_num_solution).all()

def test_can_img_be_read_correctly_case2():
    img = orientateImg("sudokuImg0.jpg", "testInput")
    board_num_solution = np.array([
        [3,0,0,8,0,1,0,0,2],
        [2,0,1,0,3,0,6,1,4],
        [0,0,0,2,0,4,0,0,0],
        [8,0,9,0,0,0,1,0,6],
        [0,6,0,0,0,0,0,5,0],
        [7,0,2,0,0,0,4,0,9],
        [0,0,0,5,0,9,0,0,0],
        [9,0,4,0,8,0,7,0,5],
        [6,0,0,1,0,7,0,0,3]
        ])
    board, location, predicted_numbers, board_num = findNum(img)
    assert (board_num != board_num_solution).any()

def test_can_img_be_read_correctly_case3():
    img = orientateImg("sudokuImg2.jpg", "testInput")
    board_num_wrong_solution = np.array([
        [0,0,0,2,3,0,0,0,0],
        [0,6,7,0,0,0,9,2,0],
        [0,9,0,0,0,7,0,3,0],
        [0,0,4,0,7,0,0,0,8],
        [6,0,0,4,0,2,0,0,1],
        [7,0,0,0,1,0,6,0,0],
        [0,7,0,6,0,0,0,1,0],
        [0,1,8,0,0,0,3,7,0],
        [0,0,0,0,5,1,0,0,0]
        ])
    board, location, predicted_numbers, board_num = findNum(img)
    assert (board_num == board_num_wrong_solution).all()

def test_can_img_be_read_correctly_case4():
    img = orientateImg("sudokuImg2.jpg", "testInput")
    board_num_wrong_solution = np.array([
        [0,0,0,2,3,0,0,0,0],
        [0,6,7,0,0,0,9,2,0],
        [0,9,0,0,0,7,0,3,0],
        [0,0,4,0,7,0,0,0,8],
        [6,0,0,4,0,2,0,0,0],
        [7,0,0,0,1,0,6,0,0],
        [0,7,0,6,0,0,0,1,0],
        [0,1,8,0,0,0,3,7,0],
        [0,0,0,0,5,1,0,0,0]
        ])
    board, location, predicted_numbers, board_num = findNum(img)
    assert (board_num != board_num_wrong_solution).any()



def test_can_mask_num_be_created_correctly_case1():
    pass

def test_can_mask_num_be_created_correctly_case2():
    pass








