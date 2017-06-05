#!/usr/bin/env python3 -tt
"""
File: lexicon.py
-----------------
A Lexicon is a word list. This Lexicon is backed by a data
structure called a prefix tree or trie ("try").

TODO

"""

# from ..decorators import print_args
import collections as _collections

class Lexicon(_collections.abc.MutableSet):
    def __init__(self, file=None):
        self._root = None
        self.size = 0
        if file:
            self._add_words_from_file(file)

    def _add_words_from_file(self, file, delimiter='\n'):
        with open(file, 'r') as f:
            raw = f.read()

        # TODO: make this dynamically loaded?
        for line in raw.split(delimiter)[:10]:
            self.add(line)

    def add(self, word):
        if not word or not word.isalpha():
            return False
        word = word.lower()
        if not self._root:
            self._root = _TrieNode()
        return self._add_helper(self._root, word, word)

    def clear(self):
        self.size = 0
        self._root = None

    def __contains__(self, word):
        if not word or not word.isalpha():
            return False
        word = word.lower()
        return self._contains_helper(self._root, word, is_prefix=False)

    def contains_prefix(self, word):
        if not word or not word.isalpha():
            return False
        word = word.lower()
        return self._contains_helper(self._root, word, is_prefix=True)

    def remove(self, word):
        if not word or not word.isalpha():
            return False
        word = word.lower()
        return self._remove_helper(self._root, word, is_prefix=False)

    def remove_prefix(self, word):
        if not word or not word.isalpha():
            return False
        word = word.lower()
        return self._remove_helper(self._root, word, is_prefix=True)

    def __len__(self):
        return self.size

    def __str__(self):
        return "Lexicon(num_words={self.size})".format(self=self)

    def __lt__(self):
        pass


    # deep copy?

    def __eq__(self, other):
        pass

    #TODO: this is gross
    def __iter__(self):
        yield from self.__iter_helper__(self._root, '')

    def __iter_helper__(self, node, sofar):
        if not node:
            return
        if node.is_word:
            yield sofar
        for letter in 'abcdefghijklmnopqrstuvwxyz':
            yield from self.__iter_helper__(node.get_child(letter), sofar + letter)


    def __hash__(self):
        pass

    def _add_helper(self, node, word, original):

        if not word:  # We've reached the end, mark it as a word
            already_exists = node.is_word
            if not already_exists:
                self.size += 1
                node.is_word = True
            return already_exists

        first, *rest = word  # 'word' -> 'w', ['o', 'r', 'd']
        child = node.get_child(first)
        if not child:
            child = node.add_child(first)
        return self._add_helper(child, rest, original)

    def _contains_helper(self, node, word, is_prefix=False):
        if not node:
            # BC: No node reaches this far, so the prefix must not exist.
            return False
        if not word:
            # BC: Found nodes this far. We found it if we're looking for a prefix or we're at a word
            return is_prefix or node.is_word
        # RC: Take one step forward
        return self._contains_helper(node.get_child(word[0]), word[1:], is_prefix)

    def _remove_helper(self, node, word, ):
        if not node:
            # BC: Dead end!
            return False
        if not word:
            # BC: We've walked down the whole tree
            pass


class _TrieNode(object):
    ALPHABET_SIZE = 26

    def __init__(self):
        self.is_word = False
        self.children = [None for _ in range(_TrieNode.ALPHABET_SIZE)]
        self.num_children = 0
        self.num_descendants = 0

    def get_child(self, letter):
        """# pre: letter is between 'a' and 'z' in lowercase"""
        return self.children[ord(letter) - ord('a')]

    def add_child(self, letter):
        child = _TrieNode()
        self.children[ord(letter) - ord('a')] = child
        self.num_children += 1
        self.num_descendants += 1
        return child

    @property
    def is_leaf_node():
        return self.num_children == 0


def scrub(string):
    return ''.join(filter(str.islower, string))





def test_lexicon():
    lex = Lexicon(file='/usr/share/dict/words')
    print(lex)
    print('aaron' in lex)
    for word in lex:
        print(word)


if __name__ == '__main__':
    test_lexicon()

