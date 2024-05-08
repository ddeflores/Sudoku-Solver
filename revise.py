def revise(csp, var1, var2):
    removed = False
    # for each possible value remaining for the cell_i cell
    for value in csp["variables"][var1]:
        # if var1 is in conflict with var2 for each possibility in the domains
        if not any([value != poss for poss in csp["variables"][var2]]):
            # remove the value from var1's domain
            csp["variables"][var1] = remove(csp["variables"][var1], value) 
            removed = True

    # returns true if the domain is smaller
    return removed

# helper function to remove a value from a domain
def remove(domain, value):
    new_domain = []
    # append each value in the domain if it isnt the one to be removed
    for d in domain:
        if d != value:
            new_domain.append(d)
    return new_domain

