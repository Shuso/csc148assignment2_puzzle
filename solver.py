# Assignment 2 - Puzzle Game
#
# CSC148 Fall 2015, University of Toronto
# Instructor: David Liu
# ---------------------------------------------
"""This module contains functions responsible for solving a puzzle.

This module can be used to take a puzzle and generate one or all
possible solutions. It can also generate hints for a puzzle (see Part 4).
"""


def solve(puzzle, verbose=False):
    """Return a solution of the puzzle.

    Even if there is only one possible solution, just return one of them.
    If there are no possible solutions, return None.

    In 'verbose' mode, print out every state explored in addition to
    the final solution. By default 'verbose' mode is disabled.

    Uses a recursive algorithm to exhaustively try all possible
    sequences of moves (using the 'extensions' method of the Puzzle
    interface) until it finds a solution.

    @type puzzle: Puzzle
    @type verbose: bool
    @rtype: Puzzle | None
    """
    if puzzle.is_solved():
        return puzzle
    else:
        solved = []
        for state in puzzle.extensions():
            if verbose:
                print(state)
            s = solve(state)
            if verbose:
                print(s)
            if s is not None:
                solved.append(s)
        if len(solved) == 0:
            return None
        if verbose:
            print(solved[0])
        return solved[0]


def solve_complete(puzzle, verbose=False):
    """Return all solutions of the puzzle.

    Return an empty list if there are no possible solutions.

    In 'verbose' mode, print out every state explored in addition to
    the final solution. By default 'verbose' mode is disabled.

    Uses a recursive algorithm to exhaustively try all possible
    sequences of moves (using the 'extensions' method of the Puzzle
    interface) until it finds all solutions.

    @type puzzle: Puzzle
    @type verbose: bool
    @rtype: list[Puzzle]
    """

    if puzzle.is_solved():
        return [puzzle]
    else:
        solved = []
        for state in puzzle.extensions():
            if verbose:
                print(state)
            s = solve_complete(state)
            if s is not []:
                solved += s
        if len(solved) == 0:
            return []
        if verbose:
            for s in solved:
                print(s)
        return solved


def hint_by_depth(puzzle, n):
    """Return a hint for the given puzzle state.

    Precondition: n >= 1.

    If <puzzle> is already solved, return the string 'Already at a solution!'
    If <puzzle> cannot lead to a solution or other valid state within <n> moves,
    return the string 'No possible extensions!'

    @type puzzle: Puzzle
    @type n: int
    @rtype: str
    """
    if puzzle.is_solved():
        return 'Already at a solution!'
    l = []
    for item in puzzle.extensions():
        l.append(return_depth(item))
    if min(l) > n:
        return "No possible extensions!"
    l = []
    for i in range(1,n+1):
        l.append(i)
    m = []
    for d in l:
        m.append(items_at_depth(puzzle, d))
    for item in m:
        if item.is_solved():
            pass
    # not completed yet

# ------------------------------------------------------------------------
# Helpers for  'hint_by_depth'
# ------------------------------------------------------------------------


def return_depth(puzzle):
    """Return the smallest depth to solutions could be reached by puzzle state

    @type puzzle: Puzzle
    @rtype: int
    """
    if puzzle.is_solved() or len(puzzle.extensions()) == 0:
        return 0
    else:
        l = []

        m = puzzle.extensions()
        for state in m:
            l.append(return_depth(state))

        return 1 + min(l)


def items_at_depth(puzzle, d):
    """Return a list of all items in this puzzle at depth <d>.

    Precondition: d >= 1.

    @type puzzle: Puzzle
    @type d: int
    @rtype: list[Puzzle]
    """
    l = []
    m = []
    if puzzle.is_solved() or len(puzzle.extensions()) == 0:
        return []
    elif d == 1:
        return [puzzle.extensions()]

    else:
        for item in puzzle.extensions():
            l += items_at_depth(item, d-1)
    for item in l:
        if not item:
            m.append(item)
    return m


if __name__ == '__main__':
    from word_ladder_puzzle import *
    from sudoku_puzzle import *
    w = WordLadderPuzzle('care', 'mire')
    print(return_depth(w))
    solve_complete(w, True)
    s = items_at_depth(w, 1)

    print(items_at_depth(w, 1))
    for item in s[0]:
        print(item)











