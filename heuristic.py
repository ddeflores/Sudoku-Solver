def minimum_remaining_values(CSP, vars):
    # store the unassigned variables in a dict
    unassigned_variables = {}

    # go through each cell and check if it is assigned
    for square in CSP["variables"]:
        if square not in vars:
            # add it to the list with its length
            unassigned_variables[square] = len(CSP["variables"][square])
            
    # get the smallest length
    mrv = min(unassigned_variables, key=unassigned_variables.get)
    return mrv

