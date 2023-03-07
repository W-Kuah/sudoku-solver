from imgRW import solveSudokuImg
import os

def main():
    files = os.listdir('Input')
    for file in files:
        if '.jpg' in file:
            solveSudokuImg(file)

if __name__ == "__main__":
    main()