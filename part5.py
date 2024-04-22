from part2 import remove
from part3 import AC3
from part4 import minimum_remaining_values
from sudoku_constraints9x9 import constraint9x9
import copy

global puzzle_1
global puzzle_2
global puzzle_3
global puzzle_4
global puzzle_5

def backtrack(csp):
    # if assignment is complete, print and return it
    if is_complete(csp):
        print('Solution Found!')
        printSolution(csp)
        return [csp["assignment"], csp["order_assigned"], csp["remaining_unassigned"]]

    # select unassigned variable using mrv
    var = minimum_remaining_values(csp, csp["assignment"])

    # make a deep copy of the domain to revert to if a solution isnt found
    original_domain = copy.deepcopy(csp["variables"])
    
    # for each value in the domain values
    for value in csp["variables"][var]:
        # check if the value is consistent with the rest of the domain using AC3
        csp["variables"][var] = [value]  
        if AC3(csp):
            # if it is consistent, add it to the assignment
            csp["assignment"][var] = value 
            csp["order_assigned"].append(var)

            # store the domain after insertion
            current_domain_snapshot = copy.deepcopy(csp["variables"])
            csp["remaining_unassigned"].append(current_domain_snapshot)

            # recursively call with new values
            result = backtrack(csp)

            # if a solution was found, return it
            if result:
                return result
            csp["order_assigned"].pop()
            csp["remaining_unassigned"].pop()
        # revert to the original domain if the assignment didnt return a solution
        csp["variables"] = copy.deepcopy(original_domain)
        
        # remove the value from assignment since no solution was found with it
        if var in csp["assignment"]:
            del csp["assignment"][var]
            
    # return false when no solution is found
    return False



def is_complete(CSP):
    # check that every variable is assigned, no need to check for consistency since it was done at every step
    return set(CSP["assignment"].keys()) == set(CSP["variables"].keys())



# helper function to turn 2d puzzle list into 3d list of domains
def prepare_puzzle(puzzle):
    # get the size of the NxN puzzle
    size = len(puzzle)

    # get the entire domain of the puzzle
    nums = []
    for i in range(1,  size + 1):
        nums.append(i)

    # initialize list to hold each variable domain
    domain = []

    # go through each variable, and if the square is empty, set it to the entire domain of the puzzle (nums)
    # otherwise, set assign the domain to the number at the index
    for i in range(len(puzzle)):
        domain.append([])
        for j in range(len(puzzle[i])):
            if puzzle[i][j] is None:
                domain[i].append(nums)
            else:
                domain[i].append([puzzle[i][j]])
    # return the new 3d list of domains
    return domain




# helper function to turn a constraint list and 3d list of domains into a CSP
def turn_puzzle_into_csp(constraints, puzzle):
    # make new dict
    csp = {}
    # add given constraints
    csp["constraints"] = constraints

    # add each variable from the given assignment
    csp["variables"] = {}
    csp["assignment"] = {}
    csp["order_assigned"] = []
    csp["remaining_unassigned"] = []

    i = 1
    j = 1
    for i in range(len(puzzle)):
        for j in range(len(puzzle[i])):
            csp["variables"]['C'+str(i + 1) + str(j + 1)] = puzzle[i][j]

    # if using the 4x4 constraints that I defined (9x9 has size of 810)
    if len(csp["constraints"]) != 810:
        csp["constraints"] = constraints["constraints"]
        csp["variables"] = constraints["variables"]
    return csp




# print the solution like an actual sudoku board
def printSolution(csp):
    # print the order each variable was assigned and the domains of the remaining unassigned variables
    print('Order each variable was assigned: ')
    for i in range(len(csp["order_assigned"])):

        # if it ends in 1 or 2 change the suffix accordingly
        suffix = 'th'
        if (i + 1) % 10 == 1:
            suffix = 'st'
        elif (i + 1) % 10 == 2:
            suffix = 'nd'

        print('Inserted ' + str(i + 1) + suffix + ': ' + str(csp["order_assigned"][i]))
        print('Remaining domains after ' + str(csp["order_assigned"][i]) + ' was assigned')
        print(csp["remaining_unassigned"][i])
        print()

    # size is the square root of the number of variables
    size = int(len(csp["variables"].keys()) ** 0.5)
    # define 2d list to place each assignment 
    solution = [['X']*size for _ in range(size)]

    # count to keep track of how many values have been printed on each line
    count = 0
    # format the lines underneath the values
    num_spaces = 6 * int(len(csp["variables"]) ** 0.5)

    # for each key, get the index and add it to the solution list
    for key in csp["assignment"].keys():
        x = int(key[1]) - 1
        y = int(key[2]) - 1
        solution[x][y] = csp["assignment"][key]

    # print everything out from solution
    for i in range(int(len(csp["variables"].keys()) ** 0.5)):
        for j in range(int(len(csp["variables"].keys()) ** 0.5)):
            count += 1
            if solution[i][j] != ' ':
                print('| ' + str(solution[i][j]) + ' |', end= " ")
            else:
                print('| X |', end= " ")
            if count == int(len(csp["variables"]) ** 0.5):
                count = 0
                print()
                print('-' * num_spaces)




def main():
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

    # make sure the puzzles are compatible with the functions
    puzzle_1 = prepare_puzzle(puzzle_1)
    puzzle_2 = prepare_puzzle(puzzle_2)
    puzzle_3 = prepare_puzzle(puzzle_3)
    puzzle_4 = prepare_puzzle(puzzle_4)
    puzzle_5 = prepare_puzzle(puzzle_5)

    # combine puzzle constraints and variables into CSP map
    CSP1 = turn_puzzle_into_csp(constraint9x9, puzzle_1)
    CSP2 = turn_puzzle_into_csp(constraint9x9, puzzle_2)
    CSP3 = turn_puzzle_into_csp(constraint9x9, puzzle_3)
    CSP4 = turn_puzzle_into_csp(constraint9x9, puzzle_4)
    CSP5 = turn_puzzle_into_csp(constraint9x9, puzzle_5)

    # iterate through each CSP to find a solution
    CSPS = [CSP1, CSP2, CSP3, CSP4, CSP5]
    for i in range(5):
        print('Looking for a solution for Puzzle', str(i + 1) + ': ')
        result = backtrack(CSPS[i])
        if not result:
            print('No Solution Found')


if __name__ == "__main__":
    main()