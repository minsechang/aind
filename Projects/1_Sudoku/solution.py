import itertools
from utils import *
from copy import deepcopy

row_units = [cross(r, cols) for r in rows]
column_units = [cross(rows, c) for c in cols]
square_units = [cross(rs, cs) for rs in ('ABC','DEF','GHI') for cs in ('123','456','789')]

# Misunderstood the requirement. diag_units mean main diagonals only.
# diag_units_NE = []
# diag_units_SE = []
# for idx_c in range(len(rows)):
#     idx_r = 0
#     unit_list_above = []
#     unit_list_below = []
#     while idx_c >= 0:
#         unit_list_above.append("{}{}".format(rows[idx_r], cols[idx_c]))
#         idx_r_T = len(rows)-1-idx_r
#         idx_c_T = len(rows)-1-idx_c
#         unit_list_below.append("{}{}".format(rows[idx_r_T], cols[idx_c_T]))
#         idx_c -= 1
#         idx_r += 1
#     diag_units_NE.append(unit_list_above)
#     if idx_r < len(rows):
#         diag_units_NE.append(unit_list_below)
#
# for idx_r in range(len(cols)):
#     idx_c = len(cols)-1
#     unit_list_above = []
#     unit_list_below = []
#     while idx_r >= 0:
#         unit_list_above.append("{}{}".format(rows[idx_r], cols[idx_c]))
#         idx_r_T = len(rows)-1-idx_r
#         idx_c_T = len(rows)-1-idx_c
#         unit_list_below.append("{}{}".format(rows[idx_r_T], cols[idx_c_T]))
#         idx_c -= 1
#         idx_r -= 1
#     diag_units_SE.append(unit_list_above)
#     if idx_c >= 0:
#         diag_units_SE.append(unit_list_below)

unitlist = row_units + column_units + square_units
diag_unit1 = [rows[i]+cols[i] for i in range(len(rows))]
diag_unit2 = [rows[i]+cols[len(rows)-1-i] for i in range(len(rows))]
unitlist.append(diag_unit1)
unitlist.append(diag_unit2)


# Must be called after all units (including diagonals) are added to the unitlist
units = extract_units(unitlist, boxes)
peers = extract_peers(units, boxes)

def naked_twins(values):
    """Eliminate values using the naked twins strategy.

    The naked twins strategy says that if you have two or more unallocated boxes
    in a unit and there are only two digits that can go in those two boxes, then
    those two digits can be eliminated from the possible assignments of all other
    boxes in the same unit.

    Parameters
    ----------
    values(dict)
        a dictionary of the form {'box_name': '123456789', ...}

    Returns
    -------
    dict
        The values dictionary with the naked twins eliminated from peers

    Notes
    -----
    Your solution can either process all pairs of naked twins from the input once,
    or it can continue processing pairs of naked twins until there are no such
    pairs remaining -- the project assistant test suite will accept either
    convention. However, it will not accept code that does not process all pairs
    of naked twins from the original input. (For example, if you start processing
    pairs of twins and eliminate another pair of twins before the second pair
    is processed then your code will fail the PA test suite.)

    The first convention is preferred for consistency with the other strategies,
    and because it is simpler (since the reduce_puzzle function already calls this
    strategy repeatedly).

    See Also
    --------
    Pseudocode for this algorithm on github:
    https://github.com/udacity/artificial-intelligence/blob/master/Projects/1_Sudoku/pseudocode.md
    """
    display(values)
    new_values = values.copy()
    for group in unitlist:
        twoElems = [box for box in group if len(values[box]) == 2]
        for idxA, box_idx_A in enumerate(twoElems):
            for idxB in range(idxA+1, len(twoElems)):
                box_idx_B = twoElems[idxB]
                if values[box_idx_B] == values[box_idx_A]:
                    for peer in group:
                        if peer == box_idx_A or peer == box_idx_B or values[peer] == values[box_idx_B]:
                            continue
                        oldVal = values[peer]
                        for digit in values[box_idx_A]:
                            oldVal = oldVal.replace(digit, '')
                        new_values = assign_value(new_values, peer, oldVal)
                    if (values != new_values):
                        #The puzzle is unstuck now. Return this solution.
                        return new_values
                    else:
                        # This naked twin didn't make a differece. Let's find another pair.
                        break
    return values


def eliminate(values):
    """Apply the eliminate strategy to a Sudoku puzzle

    The eliminate strategy says that if a box has a value assigned, then none
    of the peers of that box can have the same value.

    Parameters
    ----------
    values(dict)
        a dictionary of the form {'box_name': '123456789', ...}

    Returns
    -------
    dict
        The values dictionary with the assigned values eliminated from peers
    """
    """Eliminate values from peers of each box with a single value.

    Go through all the boxes, and whenever there is a box with a single value,
    eliminate this value from the set of values of all its peers.

    Args:
        values: Sudoku in dictionary form.
    Returns:
        Resulting Sudoku in dictionary form after eliminating values.
    """
    solved_values = [box for box in values.keys() if len(values[box]) == 1]
    for box in solved_values:
        digit = values[box]
        for peer in peers[box]:
            # if len(values[peer]) > 1:
            values[peer] = values[peer].replace(digit,'')
    return values


def only_choice(values):
    """Apply the only choice strategy to a Sudoku puzzle

    The only choice strategy says that if only one box in a unit allows a certain
    digit, then that box must be assigned that digit.

    Parameters
    ----------
    values(dict)
        a dictionary of the form {'box_name': '123456789', ...}

    Returns
    -------
    dict
        The values dictionary with all single-valued boxes assigned

    Notes
    -----
    You should be able to complete this function by copying your code from the classroom
    """
    """Finalize all values that are the only choice for a unit.

    Go through all the units, and whenever there is a unit with a value
    that only fits in one box, assign the value to this box.

    Input: Sudoku in dictionary form.
    Output: Resulting Sudoku in dictionary form after filling in only choices.
    """
    # values_copy = deepcopy(values)
    for unit in unitlist:
        for digit in '123456789':
            dplaces = [box for box in unit if digit in values[box]]
            if len(dplaces) == 1:
                # for diag in diag_units_SE:
                #     if dplaces[0] in diag:
                #         se_diag = diag
                #         break
                # for diag in diag_units_NE:
                #     if dplaces[0] in diag:
                #         ne_diag = diag
                #         break
                # digitFound = False
                # for box in ne_diag+se_diag:
                #     if values[box] == digit:
                #         digitFound = True
                #         break
                #
                # if not digitFound:
                values[dplaces[0]] = digit
    return values



def reduce_puzzle(values):
    """Reduce a Sudoku puzzle by repeatedly applying all constraint strategies

    Parameters
    ----------
    values(dict)
        a dictionary of the form {'box_name': '123456789', ...}

    Returns
    -------
    dict or False
        The values dictionary after continued application of the constraint strategies
        no longer produces any changes, or False if the puzzle is unsolvable 
    """
    """
    Iterate eliminate() and only_choice(). If at some point, there is a box with no available values, return False.
    If the sudoku is solved, return the sudoku.
    If after an iteration of both functions, the sudoku remains the same, return the sudoku.
    Input: A sudoku in dictionary form.
    Output: The resulting sudoku in dictionary form.
    """
    stalled = False
    while not stalled:
        # Check how many boxes have a determined value
        display(values)
        solved_values_before = len([box for box in values.keys() if len(values[box]) == 1])
        # Use the Eliminate Strategy
        values = eliminate(values)
        display(values)
        # Use the Only Choice Strategy
        values = only_choice(values)

        display(values)
        # Check how many boxes have a determined value, to compare
        solved_values_after = len([box for box in values.keys() if len(values[box]) == 1])
        # If no new values were added, stop the loop.
        stalled = solved_values_before == solved_values_after

        if stalled:
            values = naked_twins(values)
            stalled = solved_values_before == solved_values_after
        # Sanity check, return False if there is a box with zero available values:
        if len([box for box in values.keys() if len(values[box]) == 0]):
            return False
    return values


def search(values):
    """Apply depth first search to solve Sudoku puzzles in order to solve puzzles
    that cannot be solved by repeated reduction alone.

    Parameters
    ----------
    values(dict)
        a dictionary of the form {'box_name': '123456789', ...}

    Returns
    -------
    dict or False
        The values dictionary with all boxes assigned or False

    Notes
    -----
    You should be able to complete this function by copying your code from the classroom
    and extending it to call the naked twins strategy.
    """
    "Using depth-first search and propagation, try all possible values."
    # First, reduce the puzzle using the previous function
    values = reduce_puzzle(values)
    if values is False:
        return False ## Failed earlier
    if all(len(values[s]) == 1 for s in boxes):
        return values ## Solved!
    # Choose one of the unfilled squares with the fewest possibilities
    n,s = min((len(values[s]), s) for s in boxes if len(values[s]) > 1)
    # Now use recurrence to solve each one of the resulting sudokus, and
    for value in values[s]:
        new_sudoku = values.copy()
        new_sudoku[s] = value
        attempt = search(new_sudoku)
        if attempt:
            return attempt


def solve(grid):
    """Find the solution to a Sudoku puzzle using search and constraint propagation

    Parameters
    ----------
    grid(string)
        a string representing a sudoku grid.
        
        Ex. '2.............62....1....7...6..8...3...9...7...6..4...4....8....52.............3'

    Returns
    -------
    dict or False
        The dictionary representation of the final sudoku grid or False if no solution exists.
    """
    values = grid2values(grid)
    values = search(values)
    return values


if __name__ == "__main__":
    diag_sudoku_grid = '2.............62....1....7...6..8...3...9...7...6..4...4....8....52.............3'
    display(grid2values(diag_sudoku_grid))
    result = solve(diag_sudoku_grid)
    display(result)

    try:
        import PySudoku
        PySudoku.play(grid2values(diag_sudoku_grid), result, history)

    except SystemExit:
        pass
    except:
        print('We could not visualize your board due to a pygame issue. Not a problem! It is not a requirement.')
