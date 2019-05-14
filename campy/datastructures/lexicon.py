"""
This file exports a :class:`Lexicon` class, a compact structure for storing a list of words.

This :class:`Lexicon` implementation is backed by a data structure called a prefix tree or trie ("try").
"""

# from ..decorators import print_args
import collections as _collections
import collections.abc as _collections_abc

class Lexicon(_collections.abc.MutableSet):
    """Representation of a :class:`Lexicon`, or word list.

    The main difference between a lexicon and a dictionary is that
    a lexicon does not provide any mechanism for storing definitions;
    the lexicon contains only words, with no associated information.

    It is therefore similar to a set of strings, but with a more
    space-efficient internal representation. The :class:`Lexicon`
    class supports efficient lookup operations for words and prefixes.

    For example, the following program lists all of the two-letter words
    in the lexicon stored at `english.lex`::

        lex = Lexicon('english.lex')
        for word in lex:
            if len(word) == 2:
                print(word)

    """
    def __init__(self, file=None):
        """Initialize a new lexicon.

        The default constructor creates an empty lexicon. The second form reads
        in the contents of the lexicon from a specified data filename.

        Usage::

            lex = Lexicon()
            lex_with_words = Lexicon('english.lex')

     * Initializes a new lexicon.  The default constructor creates an empty
     * lexicon.  The second form reads in the contents of the lexicon from
     * the specified data file.  The data file must be in one of two formats:
     * (1) a space-efficient precompiled binary format or (2) a text file
     * containing one word per line.  The Stanford library distribution
     * includes a binary lexicon file named <code>English.dat</code>
     * containing a list of words in English.  The standard code pattern
     * to initialize that lexicon looks like this:
     *
     *<pre>
     *    Lexicon english("English.dat");
     *</pre>
     */
        """

        self._root = None
        self.size = 0
        if file:
            self._add_words_from_file(file)

    def _add_words_from_file(self, file, delimiter='\n'):
        with open(file, 'r') as f:
            raw = f.read()

        # TODO: make this dynamically loaded?
        for line in raw.split(delimiter):
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

    discard = remove

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


def _scrub(string):
    return ''.join(filter(str.islower, string))
