import utils
import copy
import re
import numpy as np
from os import path

day = 4

filename="input"+str(day)+".txt"
# filename="testinput"+str(day)+".txt"

basepath = path.dirname(__file__)
filepath = path.abspath(path.join(basepath, filename))

input = []
with open(filepath) as f:
    input = [l.strip() for l in f.readlines()] # One entry for each line
    
    # input = [x for x in input]
    
    # input = [int(x.strip()) for x in input]
    # input = [x.strip() for x in input]
    # input = [[int(s) for s in x] for x in input]

    numbers_to_call = [int(x) for x in input[0].split(',')]
    
    boards = []
    board = None
    for row in input[1:]:
        if row == "":
            if board is not None:
                boards.append(board)
            board = []
        else:
            board.append([int(s) for s in row.split()])
    boards.append(board)
 
# --- #
'''Return a board with the number replaced by x'''
def check_number_on_board(board, number):
    b = [["X" if s == number else s for s in row] for row in board]
    return b    

""" Return true if it's a winner """
def board_is_winner(board):
    # Check rows
    winner = ['X']*5
    for row in board:
        if row == winner:
            return True
    
    # Check columns
    for i in range(5):
        col = [r[i] for r in board]
        if col == winner:
            return True
            
    # Check diagonal
    # d1 = [board[i][i] for i in range(5)]
    # if d1 == winner:
    #     return True
    #
    # d2 = [board[4-i][i] for i in range(5)]
    # if d2 == winner:
    #     return True

def score_board(board):
    just_nums = [n for row in board for n in row if n != "X"]
    print(just_nums)
    return sum(just_nums)

def part1():
    # print(numbers_to_call)
    # print(boards)
    # print(len(boards), boards[0])
    
    boards_copy = copy.copy(boards)
    for num in numbers_to_call:
        # print("---- Checking: %d ----"%num)
        for idx, board in enumerate(boards_copy):
            # print("Checking %d on board %d"%(num,idx))
            b2 = check_number_on_board(board, num)

            if board_is_winner(b2):
                print("Winner winner!")
                print()
                utils.printMatrix(b2, " ")
                score = score_board(b2)
                print()
                return score * num

            # utils.printMatrix(b2, ' ')
            boards_copy[idx] = b2
            
            
    
def part2():
    boards_copy = copy.copy(boards)
    uncompleted = [i for i in range(len(boards_copy))]
    
    for num in numbers_to_call:
        # print("---- Checking: %d ----"%num)
        for idx, board in enumerate(boards_copy):
            if idx not in uncompleted:
                continue
                
            # print("Checking %d on board %d"%(num,idx))
            b2 = check_number_on_board(board, num)

            if board_is_winner(b2):
                # print("Winner winner!")
                # print()
                # utils.printMatrix(b2, " ")
                # score = score_board(b2)
                # print()
                uncompleted.remove(idx)
                if len(uncompleted) == 0:
                    print("Only one board left")
                    print("Loser is: %d"%idx)
                    score = score_board(b2)
                    utils.printMatrix(b2, " ")
                    print("Score: %d"%score)
                    print()
                    return score * num
                    
            # utils.printMatrix(b2, ' ')
            boards_copy[idx] = b2
    
    

# --- #

if __name__ == "__main__":
    utils.funWrapper(part1, "Part 1")
    utils.funWrapper(part2, "Part 2")