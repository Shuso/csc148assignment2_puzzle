# Assignment 2 - Puzzle Game
#
# CSC148 Fall 2015, University of Toronto
# Instructor: David Liu
# ---------------------------------------------
"""Word ladder module.

Your task is to complete the implementation of this class so that
you can use it to play Word Ladder in your game program.

Rules of Word Ladder
--------------------
1. You are given a start word and a target word (all words in this puzzle
   are lowercase).
2. Your goal is to reach the target word by making a series of *legal moves*,
   beginning from the start word.
3. A legal move at the current word is to change ONE letter to get
   a current new word, where the new word must be a valid English word.

The sequence of words from the start to the target is called
a "word ladder," hence the name of the puzzle.

Example:
    Start word: 'make'
    Target word: 'cure'
    Solution:
        make
        bake
        bare
        care
        cure

    Note that there are many possible solutions, and in fact a shorter one
    exists for the above puzzle. Do you see it?

Implementation details:
- We have provided some starter code in the constructor which reads in a list
  of valid English words from wordsEn.txt. You should use this list to
  determine what moves are valid.
- **WARNING**: unlike Sudoku, Word Ladder has the possibility of getting
  into infinite recursion if you aren't careful. The puzzle state
  should keep track not just of the current word, but all words
  in the ladder. This way, in the 'extensions' method you can just
  return the possible new words which haven't already been used.
"""
from puzzle import Puzzle


CHARS = 'abcdefghijklmnopqrstuvwyxyz'


class WordLadderPuzzle(Puzzle):
    """A word ladder puzzle."""

    # TODO: add to this list of private attributes!
    # === Private attributes ===
    # @type _words: list[str]
    #     List of English words
    # @type _ladder: list[str]
    #     List of words in the "ladder" (excluding the target word)

    # === Private attributes ===
    # @type start: str
    #     The start word
    # @type target: str
    #     The target word

    def __init__(self, start, target):
        """Create a new word ladder puzzle with given start and target words.

        Note: you may add OPTIONAL arguments to this constructor,
        but you may not change the purpose of <start> and <target>.

        @type self: WordLadderPuzzle
        @type start: str
        @type target: str
        @rtype: None
        """
        # Code to initialize _words - you don't need to change this.
        self._words = []
        with open('wordsEnTest.txt') as wordfile:
            for line in wordfile:
                self._words.append(line.strip())
        self.start = start
        self.target = target
        self._ladder = [start]

    def __str__(self):
        """Return a human-readable string representation of <self>.

        @type self: WordLadderPuzzle
        @rtype: str
        """

        l = 'start word: {}\ntarget word: {}\n'.format(self.start, self.target)
        for item in self._ladder:
            l += ("\n**** {} ****\n".format(item))
        return l

    def is_solved(self):
        """Return whether <self> is solved.

        @type self: WordLadderPuzzle
        @rtype: bool

        """
        return self._ladder[-1] == self.target

    def extensions(self):
        """Return a list of possible new states after a valid move.

        The valid move must change exactly one character of the
        current word, and must result in an English word stored in
        self._words.

        You should *not* perform any moves which produce a word
        that is already in the ladder.

        The returned moves should be sorted in alphabetical order
        of the produced word.

        @type self: WordLadderPuzzle
        @rtype: list[WordLadderPuzzle]
        """
        result = []
        lst_words = sorted(self._differ_by_one(self.start))
        target = self.target
        for word in lst_words:
            if word not in self._ladder:
                new_ladder = self._ladder[:]
                new_ladder.append(word)
                new_state = WordLadderPuzzle(word, target)
                new_state._ladder = new_ladder
                result.append(new_state)
        return result

    def move(self, move):
        """Return a new puzzle state specified by making the given move.

        @type self: WordLadderPuzzle
        @type move: str
        @rtype: WordLadderPuzzle

        """
        ladder = self._ladder[:]
        if not self.is_valid(move):
            raise ValueError
        else:
            new_state = WordLadderPuzzle(move, self.target)
            new_state._ladder = ladder + new_state._ladder
            return new_state

    def is_valid(self, move):
        """Return whether a move is a valid move

        @type self: WordLadderPuzzle
        @type move: str
        @rtype: bool

        """
        if move.isalpha() and move.islower():
            if len(move) == len(self.target):
                if move in self._differ_by_one(self.start) and move not in self._ladder:
                    return True
        return False

    # ------------------------------------------------------------------------
    # Helpers for method 'extensions'
    # ------------------------------------------------------------------------
    def _same_length_words(self, word):
        """Return a list of words the same length as the word.

        @type self: WordLadderPuzzle
        @rtype: list[str]
        """
        result = []
        for item in self._words:
            if len(item) == len(word):
                result.append(item)
        return result

    def _differ_by_one(self, word):
        """Return a list of words that differ the word by one character.

        @type self: WordLadderPuzzle
        @type word: str
        @rtype: list[str]
        """
        result = []
        for item in self._same_length_words(self.start):
            counter = 0
            for i in range(len(word)):
                if word[i] == item[i]:
                    counter += 1
            if counter == len(word)-1:
                result.append(item)
        return result


if __name__ == '__main__':
    word_ladder = WordLadderPuzzle('mare', 'mire')








