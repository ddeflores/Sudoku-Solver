from flask import Flask, render_template, request
from backtrack import prepare_puzzle, turn_puzzle_into_csp, backtrack
from sudoku_constraints9x9 import constraint9x9

app = Flask(__name__)

# initialize each puzzle
puzzle_1 = [
    [7, None, None, 4, None, None, None, 8, 6],
    [None, 5, 1, None, 8, None, 4, None, None],
    [None, 4, None, 3, None, 7, None, 9, None],
    [3, None, 9, None, None, 6, 1, None, None],
    [None, None, None, None, 2, None, None, None, None],
    [None, None, 4, 9, None, None, 7, None, 8],
    [None, 8, None, 1, None, 2, None, 6, None],
    [None, None, 6, None, 5, None, 9, 1, None],
    [2, 1, None, None, None, 3, None, None, 5]
]
puzzle_2 = [
    [1, None, None, 2, None, 3, 8, None, None],
    [None, 8, 2, None, 6, None, 1, None, None],
    [7, None, None, None, None, 1, 6, 4, None],
    [3, None, None, None, 9, 5, None, 2, None],
    [None, 7, None, None, None, None, None, 1, None],
    [None, 9, None, 3, 1, None, None, None, 6],
    [None, 5, 3, 6, None, None, None, None, 1],
    [None, None, 7, None, 2, None, 3, 9, None],
    [None, None, 4, 1, None, 9, None, None, 5]
]
puzzle_3 = [
    [1, None, None, 8, 4, None, None, 5, None],
    [5, None, None, 9, None, None, 8, None, 3],
    [7, None, None, None, 6, None, 1, None, None],
    [None, 1, None, 5, None, 2, None, 3, None],
    [None, 7, 5, None, None, None, 2, 6, None],
    [None, 3, None, 6, None, 9, None, 4, None],
    [None, None, 7, None, 5, None, None, None, 6],
    [4, None, 1, None, None, 6, None, None, 7],
    [None, 6, None, None, 9, 4, None, None, 2]
]
puzzle_4 = [
    [None, None, None, None, 9, None, None, 7, 5],
    [None, None, 1, 2, None, None, None, None, None],
    [None, 7, None, None, None, None, 1, 8, None],
    [3, None, None, 6, None, None, 9, None, None],
    [1, None, None, None, 5, None, None, None, 4],
    [None, None, 6, None, None, 2, None, None, 3],
    [None, 3, 2, None, None, None, None, 4, None],
    [None, None, None, None, None, 6, 5, None, None],
    [7, 9, None, None, 1, None, None, None, None]
]
puzzle_5 = [
    [None, None, None, None, None, 6, None, 8, None],
    [3, None, None, None, None, 2, 7, None, None],
    [7, None, 5, 1, None, None, 6, None, None],
    [None, None, 9, 4, None, None, None, None, None],
    [None, 8, None, None, 9, None, None, 2, None],
    [None, None, None, None, None, 8, 3, None, None],
    [None, None, 4, None, None, 7, 8, None, 5],
    [None, None, 2, 8, None, None, None, None, 6],
    [None, 5, None, 9, None, None, None, None, None]
]

empty_board = [[None]*9 for _ in range(9)]

@app.route("/")
def sudoku():
    return render_template('index.html', empty_board=empty_board, board0=puzzle_1, board1=puzzle_2, board2=puzzle_3, board3=puzzle_4, board4=puzzle_5)

@app.route("/solve", methods=['POST'])
def solve():
    # form request when button is clicked
    form = request.form.to_dict()
    # parse the data
    index = list(form.keys())[0]
    # empty 9x9 board
    board = [[None for _ in range(9)] for _ in range(9)]

    # Fill the board with the values from the form
    if index[5] == '0':
        board = puzzle_1
    elif index[5] == '1':
        board = puzzle_2
    elif index[5] == '2':
        board = puzzle_3
    elif index[5] == '3':
        board = puzzle_4
    elif index[5] == '4':
        board = puzzle_5
    else:
        # if the puzzle is given from user input, fill in the board based on the data
        for key in form.keys():
            x = int(key[4])
            y = int(key[6])
            if form.get(key) != '':
                board[x][y] = form.get(key, None)

    # combine puzzle constraints and variables into CSP 
    to_solve = turn_puzzle_into_csp(constraint9x9, prepare_puzzle(board))
    solved = backtrack(to_solve)

    # if there is a solution, get the data ready to be displayed (convert back to lists)
    if solved:
        solution = [[' ']*9 for _ in range(9)]
        for key in solved[0].keys():
            x = int(key[1]) - 1
            y = int(key[2]) - 1
            solution[x][y] = solved[0][key]
        remaining = getRemaining(solved[2])
        order = solved[1]
    else:
        # if there is no solution, reset everything 
        solution = [[' ']*9 for _ in range(9)]
        remaining = []
        order = []
    return render_template('solved.html', solved=solution, remaining=remaining, order=order)

# helper function to preprocess the remaining domains at each step
def getRemaining(remaining):
    boards = []
    for board in remaining:
        current_board = [[' ']*9 for _ in range(9)]
        for var in board.keys():
            x = int(var[1]) - 1
            y = int(var[2]) - 1
            if len(board[var]) == 1:
                current_board[x][y] = board[var][0]
        boards.append(current_board)
    return boards

app.run(debug=True)
