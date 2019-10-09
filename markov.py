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
    f.close()

    return file_string


def make_chains(text_string, n_gram):
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

    for i in range(len(words_list) - n_gram):
        key_tuple = tuple(words_list[i:i + n_gram])
        chains[key_tuple] = chains.get(key_tuple, [])
        chains[key_tuple].append(words_list[i + n_gram])

    return chains


def make_text(chains):
    """Return text from chains."""

    words = []

    # Check first word in tuple is capitalized.
    key_tuple = choice(list(chains.keys()))
    while not key_tuple[0][0].isupper():
        key_tuple = choice(list(chains.keys()))

    # Check for punctuation in a word.
    for word in key_tuple:
        words.append(word)
        if contains_punctuation(word):
            return " ".join(words)

    # Randomly choose next possible word and append to list of words.
    next_word = choice(chains[key_tuple])
    words.append(next_word)
    if contains_punctuation(next_word):
        return " ".join(words)

    # Iterate through markov chain to randomly get next word.
    # Append the next word to the word list.
    # Break from while loop if word contains a punctuation and return the string.
    while next_word != '':
        next_list = list(key_tuple[1:])
        next_list.append(next_word)
        next_tuple = tuple(next_list)
        next_word = choice(chains[next_tuple])
        words.append(next_word)

        if contains_punctuation(next_word):
            return " ".join(words)
        key_tuple = next_tuple

    return " ".join(words)


def contains_punctuation(word):
    """Return True if word contains punctuation mark."""

    for letter in word:
        if letter in set(string.punctuation):
            return True
    return False


input_text = ''
for filename in sys.argv:
    if '.txt' in filename:
        # Open the file and turn it into one long string
        input_text += open_and_read_file(filename)

# Get a Markov chain
chains = make_chains(input_text, int(input("What n_gram would you want? ")))

# Produce random text
random_text = make_text(chains)

print(random_text)
