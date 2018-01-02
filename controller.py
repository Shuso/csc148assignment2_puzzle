# Assignment 2 - Puzzle Game
#
# CSC148 Fall 2015, University of Toronto
# Instructor: David Liu
# ---------------------------------------------
"""Module containing the Controller class."""
from view import TextView, WebView
from solver import *
from tree import *


class Controller:
    """Class responsible for connection between puzzles and views.

    You may add new *private* attributes to this class to help you
    in your implementation.
    """
    # === Private Attributes ===
    # @type _puzzle: Puzzle
    #     The puzzle associated with this game controller
    # @type _view: View
    #     The view associated with this game controller
    # @type _tree: Tree
    #     The tree associated with this game controller
    # @type _previous: lst[Tree]
    #     A list of Tree associated with this game controller build for "UNDO"
    # @type _children_list: lst[Tree]
    #     A list of Tree associated with this game controller build for "ATTEMPTS"
    def __init__(self, puzzle, mode='text'):
        """Create a new controller.

        <mode> is either 'text' or 'web', representing the type of view
        to use.

        By default, <mode> has a value of 'text'.

        @type puzzle: Puzzle
        @type mode: str
        @rtype: None
        """
        self._puzzle = puzzle
        self._tree = Tree(puzzle)

        # build for UNDO
        self._previous = [Tree(puzzle)]
        # build for ATTEMPTS
        self._children_list = []

        if mode == 'text':
            self._view = TextView(self)
        elif mode == 'web':
            self._view = WebView(self)
        else:
            raise ValueError()

        print(self._display_config())

        # Start the game.
        self._view.run()

    def state(self):
        """Return a string representation of the current puzzle state.

        @type self: Controller
        @rtype: str
        """
        return str(self._puzzle)

    def act(self, action):
        """Run an action represented by string <action>.

        Return a string representing either the new state or an error message,
        and whether the program should end.

        @type self: Controller
        @type action: str
        @rtype: (str, bool)
        """
        if action == "SOLVE":
            if not solve(self._puzzle):
                return '* ERROR: no solution avaliable! *', True
            else:
                return solve(self._puzzle), True

        if action == "SOLVE-ALL":
            if solve_complete(self._puzzle) == []:
                return '* ERROR: no solution avaliable! *', True
            else:
                for item in solve_complete(self._puzzle):
                    print(item)
                return '', True

        if action == 'exit':
            return '', True

        if self._check_hint(action):
            n = int(action[4:].strip())

            return " ", False

        if action == "UNDO":
            if len(self._previous) == 1:
                print("======= ERROR =======\n  no previous states")
                return " ", False

            else:
                parent_state = self._tree.parent.root
                self._puzzle = parent_state
                self._previous.remove(self._previous[-1])
                self._tree = self._previous[-1]
                return parent_state, False

        if action == "ATTEMPTS":
            if self._tree.parent is None:
                print("======= ERROR =========\n no previous attempts")
                return '', False

            else:
                for item in self._children_list:
                    if item.parent.root == self._tree.parent.root:
                        s = " attempted move: {}\n".format(item.move)
                        print(s)
                        print(item.root)

                return '', False

        elif self._check(action):

            cur_state = self._puzzle.move(action)
            self._puzzle = cur_state
            children = Tree(cur_state, action, self._tree)

            if children not in self._tree.subtrees:
                self._tree.add_subtrees([children])
                self._children_list.append(children)
            self._tree = children
            self._previous.append(self._tree)

            return cur_state, False

        elif action == 'exit':
            return '', True

        else:
            return self.state(), False

    def _check(self, move):
        """"Return True if a move is valid or display an error message otherwise

        @type self: Controller
        @type move: str
        @rtype: bool
        """
        if not self._puzzle.is_valid(move):
            print('======= ERROR =======\n* Invalid input, please try again *\n')
            return False
        else:
            return True

    def _check_hint(self, action):
        """Return whether an action is asking for hint

        @type self: Controller
        @type action: str
        @rtype: bool

        """
        if "HINT" == action[:4]:
            if action[4:].strip() < 0:
                print('=========== Error ===========\n please enter a valid positive number')
            else:
                return True
        return False

    def _display_config(self):
        """Return a string representation of starting configuration

        @type self: Controller
        @rtype: str
        """
        a = '='*90 + '\n' + sudoku_config + '\n' + '='*90
        b = '='*90 + '\n' + word_ladder_config + '\n' + '='*90
        return a + '\n' + b


class Tree:

    """A tree data structure associated with this game controller.

       all attributes were design to be public.

    """
    # === Public Attributes ===
    # @type root: object | None
    #     The item stored at the tree's root, or None if the tree is empty.
    # @type subtrees: list[Tree]
    #     A list of all subtrees of the tree
    # @type parent: Tree | None
    #     A parent Tree of self if exists otherwise is None
    # @type move: str
    #     A move leads to current state if exists otherwise is None
    #

    def __init__(self, state, move=None, parent=None):
        """Initialize a Tree with the given puzzle_state, move, parent value.

        @type self: Tree
        @type state: Puzzle
        @type move: str
        @type parent: Tree
        @rtype: None
        """
        self.root = state
        self.move = move
        self.parent = parent
        self.subtrees = []

    def is_empty(self):
        """Return True if this tree is empty.

        @type self: Tree
        @rtype: bool
        """
        return self.root is None

    def add_subtrees(self, tree):
        """Add the trees in <new_trees> as subtrees of this tree.

        Raise ValueError if this tree is empty.

        @type self: Tree
        @type tree: list[Tree]
        @rtype: None
        """
        if self.is_empty():
            raise ValueError()
        else:
            self.subtrees.extend(tree)

    def __contains__(self, item):
        """Return whether <item> is in this tree.

        @type self: Tree
        @type item: object
        @rtype: bool

        """
        if self.is_empty():
            return False

        elif self.subtrees == []:
            return self.root == item
        else:
            a = []
            for tree in self.subtrees:
                m = item in tree
                a.append(m)
            a.append(self.root == item)
            return True in a


word_ladder_config = "Rules of Word Ladder\n\n  1. You are given a start word and a target word " \
                  "all words in this puzzle are lowercase.\n  2. Your goal is to reach the target word by making " \
                  "a series of *legal moves*,beginning from the start word.\n  3. A legal move the current word is " \
                  "to change ONE letter to get a current new word, where the new word must be a valid English word"

sudoku_config = "Here are the rules of Sudoku:\n\n- The puzzle consists of an n-by-n grid. " \
                  "Each square contains a uppercase letter between A and the n-th letter\n- The goal is to fill " \
                  "in all empty squares with available letters so that the board has the following property:\n" \
                  "  1.no two squares in the same row have the same letter\n " \
                  " 2.no two squares in the same column have the same letter\n  " \
                  "3.no two squares in the same *subsquare* has the same letter\n" \
                  "- Please enter in a form of (row,col)->letter, where row and col are integers and letter is " \
                  "uppercase"
if __name__ == '__main__':
    from word_ladder_puzzle import *
    from sudoku_puzzle import *
    w = WordLadderPuzzle('care','mire')
    s = SudokuPuzzle([['B', 'C', 'D', 'A'],
                      ['D', 'A', '', ''],
                      ['C', 'D', 'A', 'B'],
                      ['A', 'B', 'C', 'D']])
    c = Controller(w)









