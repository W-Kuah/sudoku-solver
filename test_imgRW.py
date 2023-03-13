from imgRW import *

def test_calculate_length_correctly_case1():
    assert calculate_length([20,23], [41,-23]) == 50.566787519082126

def test_calculate_length_correctly_case2():
    assert calculate_length([-20,50], [39,100]) == 77.33692520394123

def test_calculate_length_correctly_case3():
    assert calculate_length([10,23], [10,90]) == 67

def test_calculate_quadArea_correctly_case1():
    area_coordinates = [
        [[5,5]],
        [[0,0]],
        [[10, 15]],
        [[5,10]]
    ]
    assert calculate_quadArea(area_coordinates) == 79.06
    

def test_calculate_quadArea_correctly_case2():
    area_coordinates = [
        [[345,158]],
        [[326,161]],
        [[388,222]],
        [[326,224]]
    ]
    assert calculate_quadArea(area_coordinates) == 2669.29

def test_calculate_quadArea_correctly_case3():
    area_coordinates = [
        [[90,15]],
        [[396,15]],
        [[91,320]],
        [[396,319]]
    ]
    assert calculate_quadArea(area_coordinates) == 93025.00

def test_calculate_quadArea_correctly_case4():
    area_coordinates = [
        [[140,93]],
        [[370,98]],
        [[126,338]],
        [[389,336]]
    ]
    assert calculate_quadArea(area_coordinates) == 59536.03

def test_calculate_quadArea_correctly_case5():
    area_coordinates = [
        [[387,158]],
        [[325,161]],
        [[388,222]],
        [[326,224]]
    ]
    assert calculate_quadArea(area_coordinates) == 3940.69



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


def test_detect_incorrect_filetype_uploaded1():
    assert solveSudokuImg('mail.svg',pathToFile="testInput") == "Invalid file. Please upload an jpg image file."

def test_detect_incorrect_filetype_uploaded2():
    assert solveSudokuImg('landscape.png',pathToFile="testInput") == "Invalid file. Please upload an jpg image file."

def test_can_board_be_read_as_too_small_correctly_case1():
    assert solveSudokuImg('math.jpg',pathToFile="testInput") == "Board detected is too small or does not exist."

def test_can_board_be_read_as_too_small_correctly_case2():
    assert solveSudokuImg('squares.jpg',pathToFile="testInput") == "Board detected is too small or does not exist."

def test_can_board_be_read_as_invalid_correctly_case1():
    assert solveSudokuImg('unsolvable.jpg',pathToFile="testInput") == "Solution doesn't exist. Or Model misread digits."

def test_can_board_be_right_sized_correctly_case1():
    assert solveSudokuImg('sudokuImg0.jpg',pathToFile="testInput") == "Solution found and returned."

def test_can_board_be_right_sized_correctly_case2():
    assert solveSudokuImg('sudokuImg1.jpg',pathToFile="testInput") == "Solution found and returned."

def test_can_board_be_right_sized_correctly_case1():
    assert solveSudokuImg('sudokuImg0.jpg',pathToFile="testInput") == "Solution found and returned."

def test_can_board_be_right_sized_correctly_case2():
    assert solveSudokuImg('sudokuImg1.jpg',pathToFile="testInput") == "Solution found and returned."




