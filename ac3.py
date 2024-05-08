from revise import revise

def AC3(csp):
    # initialize queue with every arc in the constraints
    queue = [(xi, xj) for xi, xj in csp["constraints"].keys()]
    # while the queue isnt empty
    while queue:
        # pop an arc from the queue
        (xi, xj) = queue.pop(0)
        # if revise made the domain smaller
        if revise(csp, xi, xj):
            # exit if the domain is empty, no solution exists
            if len(csp["variables"][xi]) == 0:
                return False
            # for each xk in xi's neighbors - {xj}
            for xk in get_neighbors(csp, xi, xj):
                if xk != xj:
                    # add the arc to the queue
                    queue.append((xk, xi))
    return True


# helper function to get the neighbors of a given var
def get_neighbors(CSP, var, xj):
    neighbors = []
    # go through every constraint to find each one with var in it
    for (v1, v2) in CSP['constraints']:
        if v1 == var:
            neighbors.append(v2)
        elif v2 == var:
            neighbors.append(v1)
    return neighbors
