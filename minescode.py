"""
 Mines
"""

#!/usr/bin/env python3
# import pickle
# import os
# import sys
# import typing
import doctest


# NO ADDITIONAL IMPORTS ALLOWED!
directions = [
    (1, 0),
    (-1, 0),
    (0, 1),
    (0, -1),
    (1, 1),
    (-1, -1),
    (-1, 1),
    (1, -1),
    (0, 0),
]


def dump(game):
    """
    Prints a human-readable version of a game (provided as a dictionary)
    """
    for key, val in sorted(game.items()):
        if isinstance(val, list) and val and isinstance(val[0], list):
            print(f"{key}:")
            for inner in val:
                print(f"    {inner}")
        else:
            print(f"{key}:", val)


# 2-D IMPLEMENTATION


def new_game_2d(num_rows, num_cols, bombs):
    """
    Start a new game.

    Return a game state dictionary, with the 'dimensions', 'state', 'board' and
    'hidden' fields adequately initialized.

    Parameters:
       num_rows (int): Number of rows
       num_cols (int): Number of columns
       bombs (list): List of bombs, given in (row, column) pairs, which are
                     tuples

    Returns:
       A game state dictionary

    >>> dump(new_game_2d(2, 4, [(0, 0), (1, 0), (1, 1)]))
    board:
        ['.', 3, 1, 0]
        ['.', '.', 1, 0]
    dimensions: (2, 4)
    hidden:
        [True, True, True, True]
        [True, True, True, True]
    state: ongoing
    """
    return new_game_nd((num_rows, num_cols), bombs)


def dig_2d(game, row, col):
    """
    Reveal the cell at (row, col), and, in some cases, recursively reveal its
    neighboring squares.

    Update game['hidden'] to reveal (row, col).  Then, if (row, col) has no
    adjacent bombs (including diagonally), then recursively reveal (dig up) its
    eight neighbors.  Return an integer indicating how many new squares were
    revealed in total, including neighbors, and neighbors of neighbors, and so
    on.

    The state of the game should be changed to 'defeat' when at least one bomb
    is revealed on the board after digging (i.e. game['hidden'][bomb_location]
    == False), 'victory' when all safe squares (squares that do not contain a
    bomb) and no bombs are revealed, and 'ongoing' otherwise.

    Parameters:
       game (dict): Game state
       row (int): Where to start digging (row)
       col (int): Where to start digging (col)

    Returns:
       int: the number of new squares revealed

    >>> game = {'dimensions': (2, 4),
    ...         'board': [['.', 3, 1, 0],
    ...                   ['.', '.', 1, 0]],
    ...         'hidden': [[True, False, True, True],
    ...                  [True, True, True, True]],
    ...         'state': 'ongoing'}
    >>> dig_2d(game, 0, 3)
    4
    >>> dump(game)
    board:
        ['.', 3, 1, 0]
        ['.', '.', 1, 0]
    dimensions: (2, 4)
    hidden:
        [True, False, False, False]
        [True, True, False, False]
    state: victory

    >>> game = {'dimensions': [2, 4],
    ...         'board': [['.', 3, 1, 0],
    ...                   ['.', '.', 1, 0]],
    ...         'hidden': [[True, False, True, True],
    ...                  [True, True, True, True]],
    ...         'state': 'ongoing'}
    >>> dig_2d(game, 0, 0)
    1
    >>> dump(game)
    board:
        ['.', 3, 1, 0]
        ['.', '.', 1, 0]
    dimensions: [2, 4]
    hidden:
        [False, False, True, True]
        [True, True, True, True]
    state: defeat
    """
    return dig_nd(game, (row, col))


def render_2d_locations(game, xray=False):
    """
    Prepare a game for display.

    Returns a two-dimensional array (list of lists) of '_' (hidden squares),
    '.' (bombs), ' ' (empty squares), or '1', '2', etc. (squares neighboring
    bombs).  game['hidden'] indicates which squares should be hidden.  If
    xray is True (the default is False), game['hidden'] is ignored and all
    cells are shown.

    Parameters:
       game (dict): Game state
       xray (bool): Whether to reveal all tiles or just the that are not
                    game['hidden']

    Returns:
       A 2D array (list of lists)

    >>> render_2d_locations({'dimensions': (2, 4),
    ...         'state': 'ongoing',
    ...         'board': [['.', 3, 1, 0],
    ...                   ['.', '.', 1, 0]],
    ...         'hidden':  [[True, False, False, True],
    ...                   [True, True, False, True]]}, False)
    [['_', '3', '1', '_'], ['_', '_', '1', '_']]

    >>> render_2d_locations({'dimensions': (2, 4),
    ...         'state': 'ongoing',
    ...         'board': [['.', 3, 1, 0],
    ...                   ['.', '.', 1, 0]],
    ...         'hidden':  [[True, False, True, False],
    ...                   [True, True, True, False]]}, True)
    [['.', '3', '1', ' '], ['.', '.', '1', ' ']]
    """
    return render_nd(game, xray)


def render_2d_board(game, xray=False):
    """
    Render a game as ASCII art.

    Returns a string-based representation of argument 'game'.  Each tile of the
    game board should be rendered as in the function
        render_2d_locations(game)

    Parameters:
       game (dict): Game state
       xray (bool): Whether to reveal all tiles or just the ones allowed by
                    game['hidden']

    Returns:
       A string-based representation of game

    >>> render_2d_board({'dimensions': (2, 4),
    ...                  'state': 'ongoing',
    ...                  'board': [['.', 3, 1, 0],
    ...                            ['.', '.', 1, 0]],
    ...                  'hidden':  [[False, False, False, True],
    ...                            [True, True, False, True]]})
    '.31_\\n__1_'
    """
    word = ""
    board = render_nd(game, xray)
    for row in range(len(board)):
        if row > 0:
            word = word + "\n"
        for col in range(len(board[0])):
            word += board[row][col]
    return word


# N-D IMPLEMENTATION
def fill_n_cube(dimensions, value):
    """Creates a game with the specified nd"""
    if len(dimensions) == 1:
        return [value] * dimensions[0]
    else:
        cube = []
        for _ in range(dimensions[0]):
            cube.append(fill_n_cube(dimensions[1:], value))
            # make the n-1 dimensions cube n times to make an n dimension cube
        return cube


def find_bombs(board, bomb):
    """
    sets the value of the board to a bomb
    """
    if len(bomb) == 1:
        board[bomb[0]] = "."

    else:
        find_bombs(board[bomb[0]], bomb[1:])


def index_board(board, indexes):
    """sets the value of the neighbours of the board to the
    number of bombs that
    surround it
    """
    if len(indexes) == 1:

        if board[indexes[0]] == ".":
            return
        else:
            board[indexes[0]] += 1
    else:
        index_board(board[indexes[0]], indexes[1:])


def counter(game, board, dimensions, value):
    """Iterates through the board to find the number of time
    the given value shows up
    """
    count = 0
    f_coord = (0,) * len(dimensions)
    neighbours = find_neighbours(f_coord, dimensions)
    seen = {f_coord}
    while neighbours:
        neighbour = neighbours.pop()
        if (
            get_value(board, neighbour) == value
            and get_value(game["board"], neighbour) != "."
        ):
            return 1
        else:
            pass
        seen.add(neighbour)
        for neigh in find_neighbours(neighbour, dimensions):
            if neigh not in seen:
                neighbours.append(neigh)
    return count


def find_neighbours(coordinates, dimensions):
    "given specific coordinates of a board, returns the neighbours of the board"
    if len(coordinates) == 1:
        neighbours = []

        for dir in [-1, 0, 1]:
            first = coordinates[0]
            if 0 <= first + dir < dimensions[0]:
                neighbours.append((first + dir,))
        return neighbours
    else:
        neighbours = []
        for dir in [-1, 0, 1]:
            first = coordinates[0]
            if 0 <= first + dir < dimensions[0]:
                for neighbour in find_neighbours(coordinates[1:], dimensions[1:]):
                    neighbours.append((first + dir,) + neighbour)
        return neighbours


def new_game_nd(dimensions, bombs):
    """
    Start a new game

    Return a game state dictionary, with the 'dimensions', 'state', 'board' and
    'hidden' fields adequately initialized.


    Args:
       dimensions (tuple): Dimensions of the board
       bombs (list): Bomb locations as a list of tuples, each an
                     N-dimensional coordinate

    Returns:
       A game state dictionary

    >>> g = new_game_nd((2, 4, 2), [(0, 0, 1), (1, 0, 0), (1, 1, 1)])
    >>> dump(g)
    board:
        [[3, '.'], [3, 3], [1, 1], [0, 0]]
        [['.', 3], [3, '.'], [1, 1], [0, 0]]
    dimensions: (2, 4, 2)
    hidden:
        [[True, True], [True, True], [True, True], [True, True]]
        [[True, True], [True, True], [True, True], [True, True]]
    state: ongoing
    """
    cube = fill_n_cube(dimensions, 0)
    hidden = fill_n_cube(dimensions, True)

    for bomb in bombs:
        find_bombs(cube, bomb)
        neighbours = find_neighbours(bomb, dimensions)
        for neighbour in neighbours:
            index_board(cube, neighbour)

    return {
        "dimensions": dimensions,
        "board": cube,
        "hidden": hidden,
        "state": "ongoing",
    }


def get_value(board, coordinates):
    "gets the value of the specific index in the board"
    if len(coordinates) == 1:
        return board[coordinates[0]]
    else:

        return get_value(board[coordinates[0]], coordinates[1:])


def change_value(board, coordinates, new_value):
    "sets the value of the current board[coordinates] to the new_value"
    if len(coordinates) == 1:
        board[coordinates[0]] = new_value
    else:
        return change_value(board[coordinates[0]], coordinates[1:], new_value)


def dig_nd(game, coordinates):
    """
    Recursively dig up square at coords and neighboring squares.

    Update the hidden to reveal square at coords; then recursively reveal its
    neighbors, as long as coords does not contain and is not adjacent to a
    bomb.  Return a number indicating how many squares were revealed.  No
    action should be taken and 0 returned if the incoming state of the game
    is not 'ongoing'.

    The updated state is 'defeat' when at least one bomb is revealed on the
    board after digging, 'victory' when all safe squares (squares that do
    not contain a bomb) and no bombs are revealed, and 'ongoing' otherwise.

    Args:
       coordinates (tuple): Where to start digging

    Returns:
       int: number of squares revealed

    >>> g = {'dimensions': (2, 4, 2),
    ...      'board': [[[3, '.'], [3, 3], [1, 1], [0, 0]],
    ...                [['.', 3], [3, '.'], [1, 1], [0, 0]]],
    ...      'hidden': [[[True, True], [True, False], [True, True],
    ...                [True, True]],
    ...               [[True, True], [True, True], [True, True],
    ...                [True, True]]],
    ...      'state': 'ongoing'}
    >>> dig_nd(g, (0, 3, 0))
    8
    >>> dump(g)
    board:
        [[3, '.'], [3, 3], [1, 1], [0, 0]]
        [['.', 3], [3, '.'], [1, 1], [0, 0]]
    dimensions: (2, 4, 2)
    hidden:
        [[True, True], [True, False], [False, False], [False, False]]
        [[True, True], [True, True], [False, False], [False, False]]
    state: ongoing
    >>> g = {'dimensions': (2, 4, 2),
    ...      'board': [[[3, '.'], [3, 3], [1, 1], [0, 0]],
    ...                [['.', 3], [3, '.'], [1, 1], [0, 0]]],
    ...      'hidden': [[[True, True], [True, False], [True, True],
    ...                [True, True]],
    ...               [[True, True], [True, True], [True, True],
    ...                [True, True]]],
    ...      'state': 'ongoing'}
    >>> dig_nd(g, (0, 0, 1))
    1
    >>> dump(g)
    board:
        [[3, '.'], [3, 3], [1, 1], [0, 0]]
        [['.', 3], [3, '.'], [1, 1], [0, 0]]
    dimensions: (2, 4, 2)
    hidden:
        [[True, False], [True, False], [True, True], [True, True]]
        [[True, True], [True, True], [True, True], [True, True]]
    state: defeat
    """

    def do_it(game, coordinates):
        loc_val = get_value(game["board"], coordinates)
        if game["state"] == "defeat" or game["state"] == "victory":
            game["state"] = game["state"]  # keep the state the same
            return 0
        if loc_val == ".":
            game["state"] = "defeat"
            change_value(game["hidden"], coordinates, False)
            return 1
        if get_value(game["hidden"], coordinates) is not False:

            change_value(game["hidden"], coordinates, False)
            revealed = 1
        else:
            return 0

        if loc_val == 0:
            neighbours = find_neighbours(coordinates, game["dimensions"])

            for neighbour in neighbours:

                if get_value(game["board"], neighbour) != ".":
                    if get_value(game["hidden"], neighbour) is True:

                        revealed += do_it(game, neighbour)
        return revealed

    revealed = do_it(game, coordinates)
    if counter(game, game["hidden"], game["dimensions"], True) == 0:
        game["state"] = "victory"
        return revealed

    return revealed


def render_nd(game, xray=False):
    """
    Prepare the game for display.

    Returns an N-dimensional array (nested lists) of '_' (hidden squares), '.'
    (bombs), ' ' (empty squares), or '1', '2', etc. (squares neighboring
    bombs).  The game['hidden'] array indicates which squares should be
    hidden.  If xray is True (the default is False), the game['hidden'] array
    is ignored and all cells are shown.

    Args:
       xray (bool): Whether to reveal all tiles or just the ones allowed by
                    game['hidden']

    Returns:
       An n-dimensional array of strings (nested lists)

    >>> g = {'dimensions': (2, 4, 2),
    ...      'board': [[[3, '.'], [3, 3], [1, 1], [0, 0]],
    ...                [['.', 3], [3, '.'], [1, 1], [0, 0]]],
    ...      'hidden': [[[True, True], [True, False], [False, False],
    ...                [False, False]],
    ...               [[True, True], [True, True], [False, False],
    ...                [False, False]]],
    ...      'state': 'ongoing'}

    >>> render_nd(g, False)
    [[['_', '_'], ['_', '3'], ['1', '1'], [' ', ' ']],
     [['_', '_'], ['_', '_'], ['1', '1'], [' ', ' ']]]
    >>> render_nd(g, True)
    [[['3', '.'], ['3', '3'], ['1', '1'], [' ', ' ']],
     [['.', '3'], ['3', '.'], ['1', '1'], [' ', ' ']]]
    """
    board = game["board"]
    hidden = game["hidden"]

    def render(board, hidden):
        if isinstance(board, list):
            return [render(val, hidden[indx]) for indx, val in enumerate(board)]
        else:
            if xray is True or hidden is False:
                if board == 0:
                    return " "
                else:
                    return str(board)
            else:
                return "_"

    return render(board, hidden)


if __name__ == "__main__":
    # Test with doctests. Helpful to debug individual lab.py functions.
    _doctest_flags = doctest.NORMALIZE_WHITESPACE | doctest.ELLIPSIS
    doctest.testmod(optionflags=_doctest_flags)  # runs ALL doctests

    # Alternatively, can run the doctests JUST for specified function/methods,
    # e.g., for render_2d_locations or any other function you might want.  To
    # do so, comment out the above line, and uncomment the below line of code.
    # This may be useful as you write/debug individual doctests or functions.
    # Also, the verbose flag can be set to True to see all test results,
    # including those that pass.
    #
    # doctest.run_docstring_examples(
    #    render_2d_locations,
    #    globals(),
    #    optionflags=_doctest_flags,
    #    verbose=False
    # )
    # exp_fname = os.path.join( 'test_outputs', 'testnd_newsmall6dgame.pickle')
    # with open(exp_fname, 'rb') as f:
    #     expected = pickle.load(f)
    # print(expected['board'])
    game = new_game_nd((3, 4, 5), (2, 3, 4))
    revealed = dig_nd(game, (0, 0, 0))
    print(revealed)
