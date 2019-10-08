"""Generate Markov text from text files."""

from random import choice
import sys, string


def open_and_read_file(file_path):
    """Take file path as string; return text as string.

    Takes a string that is a file path, opens the file, and turns
    the file's contents as one string of text.
    """

    f = open(file_path)
    file_string = f.read()

    return file_string


def make_chains(text_string):
    """Take input text as string; return dictionary of Markov chains.

    A chain will be a key that consists of a tuple of (word1, word2)
    and the value would be a list of the word(s) that follow those two
    words in the input text.

    For example:

        >>> chains = make_chains("hi there mary hi there juanita")

    Each bigram (except the last) will be a key in chains:

        >>> sorted(chains.keys())
        [('hi', 'there'), ('mary', 'hi'), ('there', 'mary')]

    Each item in chains is a list of all possible following words:

        >>> chains[('hi', 'there')]
        ['mary', 'juanita']
        
        >>> chains[('there','juanita')]
        [None]
    """

    chains = {}

    line_list = text_string.split('\n')
    words_list = []

    for line in line_list:
        words_list.extend(line.split(' '))

    for i in range(len(words_list) - 3):

        key_tuple = tuple(words_list[i:(i+3)])
        chains[key_tuple] = chains.get(key_tuple, [])
        chains[key_tuple].append(words_list[i + 3])

    return chains


def make_text(chains):
    """Return text from chains."""

    words = []

    key_tuple = choice(list(chains.keys()))

    for word in key_tuple:
        words.append(word)
        if contains_punctuation(word):
            return " ".join(words)

    next_word = choice(chains[key_tuple])
    words.append(next_word)
    if contains_punctuation(next_word):
        return " ".join(words)

    # Iterate through markov chain to randomly get next word.
    # Append the next word to the word list.  
    while next_word != '':
        next_tuple = (key_tuple[1], key_tuple[2], next_word)
        next_word = choice(chains[next_tuple])
        words.append(next_word)
        if contains_punctuation(next_word):
            return " ".join(words)
        
        key_tuple = next_tuple
       

    return " ".join(words)

def contains_punctuation(word):

    punctuations = string.punctuation
    for letter in word:
        if letter in punctuations:
            return True


# input_path = "green-eggs.txt"
input_text = ''
for filename in sys.argv:
    if '.txt' in filename:
        # Open the file and turn it into one long string
        input_text += open_and_read_file(filename)

# Get a Markov chain
chains = make_chains(input_text)

# Produce random text
random_text = make_text(chains)

print(random_text)
