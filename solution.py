from utils import *

assignments = []

def assign_value(values, box, value):
    """
    Please use this function to update your values dictionary!
    Assigns a value to a given box. If it updates the board record it.
    """

    # Don't waste memory appending actions that don't actually change any values
    if values[box] == value:
        return values

    values[box] = value
    if len(value) == 1:
        assignments.append(values.copy())
    return values

def naked_twins(values):
    """Eliminate values using the naked twins strategy.
    Args:
        values(dict): a dictionary of the form {'box_name': '123456789', ...}

    Returns:
        the values dictionary with the naked twins eliminated from peers.
    """
    # Find all instances of naked twins
    # Eliminate the naked twins as possibilities for their peers

    #Loop through all units to find duplicate values that fit the naked twin criteria 
    for unit in unitlist:
        #Reverse the dictionary such that duplicate values are indentified through keys with 2 or more items
        inverse = {}
        for box in unit:
            if len(values[box]) == 2: #only add values with two options
                inverse.setdefault(values[box],[]).append(box)
        #Check the reversed dictionary for naked twins
        for vKey in inverse:
            if len(inverse[vKey]) > 1:
                for box in unit:
                    #Loop though boxes in the same unit and remove the values in te naked twins
                    if box not in inverse[vKey]:
                        for c in vKey:
                            values = assign_value(values, box, values[box].replace(c, ''))

    return values
                        

def grid_values(grid):
    """
    Convert grid into a dict of {square: char} with '123456789' for empties.
    Args:
        grid(string) - A grid in string form.
    Returns:
        A grid in dictionary form
            Keys: The boxes, e.g., 'A1'
            Values: The value in each box, e.g., '8'. If the box has no value, then the value will be '123456789'.
    """
    r = dict(zip(boxes, grid))
    for k, v in r.items():
        if v == '.':
            r = assign_value(r, k, '123456789')
    return r

def eliminate(values):
    for kBox, vBox in values.items():
        if len(vBox) == 1:
            for peer in peers[kBox]:
                values = assign_value(values, peer, values[peer].replace(vBox, ''))
    return values

def only_choice(values):
    for unit in unitlist:
        for d in '123456789':
            b = ''
            for box in unit:
                if d in values[box]:
                    b = b + box
            if len(b) == 2:
                values = assign_value(values, b, d)
    return values

def reduce_puzzle(values):
    stalled = False
    while not stalled:
        # Check how many boxes have a determined value
        solved_values_before = len([box for box in values.keys() if len(values[box]) == 1])

        # Use the Eliminate Strategy
        values = eliminate(values)
        # Use the Only Choice Strategy
        values = only_choice(values)
        # Use the Naked Twins Strategy
        values = naked_twins(values)
        # Check how many boxes have a determined value, to compare
        solved_values_after = len([box for box in values.keys() if len(values[box]) == 1])
        # If no new values were added, stop the loop.
        stalled = solved_values_before == solved_values_after
        # Sanity check, return False if there is a box with zero available values:
        if len([box for box in values.keys() if len(values[box]) == 0]):
            return False
    return values

def search(values):
    "Using depth-first search and propagation, create a search tree and solve the sudoku."
    # First, reduce the puzzle using the previous function
    values = reduce_puzzle(values)
    if values is False:
        return False ## Failed earlier
    if all(len(values[s]) == 1 for s in boxes): 
        return values ## Solved!
    # Choose one of the unfilled squares with the fewest possibilities
    d = {}
    for k, v in values.items():
        if len(v) > 1:
            d.update({k:v})
    b = min(d, key=d.get)
    # Now use recursion to solve each one of the resulting sudokus, and if one returns a value (not False), return that answer!
    for v in values[b]:
        d = values.copy()
        d[b] = v
        attempt = search(d)
        if attempt:
            return attempt

def solve(grid):
    """
    Find the solution to a Sudoku grid.
    Args:
        grid(string): a string representing a sudoku grid.
            Example: '2.............62....1....7...6..8...3...9...7...6..4...4....8....52.............3'
    Returns:
        The dictionary representation of the final sudoku grid. False if no solution exists.
    """
    sudoku = grid_values(grid)
    return search(sudoku)

if __name__ == '__main__':
    diag_sudoku_grid = '2.............62....1....7...6..8...3...9...7...6..4...4....8....52.............3'
    display(solve(diag_sudoku_grid))
    try:
        from visualize import visualize_assignments
        visualize_assignments(assignments)

    except SystemExit:
        pass
    except:
        print('We could not visualize your board due to a pygame issue. Not a problem! It is not a requirement.')
