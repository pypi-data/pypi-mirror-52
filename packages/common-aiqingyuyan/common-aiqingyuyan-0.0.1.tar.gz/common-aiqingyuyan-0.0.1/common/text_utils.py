from __future__ import unicode_literals, print_function, division
from io import open
import unicodedata
import re
import string
from common.lang import Lang

# Since there are a lot of example sentences and we want to train something quickly,
# we’ll trim the data set to only relatively short and simple sentences.
# Here the maximum length is 30 words (that includes ending punctuation)
MAX_LENGTH = 30

# Files are all in Unicode, to simplify we will turn Unicode characters to ASCII
# make everything lowercase, and trim most punctuation.

def unicodeToAscii(s):
    """
    Turn a Unicode string to plain ASCII
    https://stackoverflow.com/a/518232/2809427
    """
    assert isinstance(s, str), 'input s must be type of str'
    return ''.join(
        c for c in unicodedata.normalize('NFD', s)
        if unicodedata.category(c) != 'Mn'
    )


def normalizeString(s):
    """
    Lowercase, trim and remove non-letter characters
    """
    assert isinstance(s, str), 'input s must be type of str'
    s = unicodeToAscii(s.lower().strip())
    s = re.sub(r'([.!?])', r' \1', s)
    s = re.sub(r'[^a-zA-Z0-9.!?]+', r' ', s)
    return s


def readQAPairs(file_name):
    print('Reading lines...')

    # Read file & split into lines
    pairs = []
    with open('data/{}.txt'.format(file_name), encoding='utf-8') as file:
        for line in file:
            line = line.strip()

            # Split every line into pairs & normailzie
            pair = [ normalizeString(s) for s in line.split('\t') ]
            pairs.append(pair)
    
    question_lang = Lang('question')
    answer_lang = Lang('answer')
    
    return question_lang, answer_lang, pairs


def filterPair(p):
    assert isinstance(p, (list, tuple)), 'input p must be list or tuple'
    return len(p) > 1 and p[1] != 'NULL' and \
        len(p[0].split(' ')) < MAX_LENGTH and \
        len(p[1].split(' ')) < MAX_LENGTH


def filterPairs(pairs):
    assert isinstance(pairs, list), 'input pairs must be list'
    pairs = [pair for pair in pairs if filterPair(pair)]
    return pairs


# The full process for preparing the data is:
#  1. Read text file and split into lines, split lines into pairs
#  2. Normalize text, filter by length and content
#  3. Make word lists from sentences in pairs

def prepareData(file_name):
    question_lang, answer_lang, pairs = readQAPairs(file_name)
    print('Read {} sentence pairs'.format(len(pairs)))

    pairs = filterPairs(pairs)
    print('Trimmed to {} sentence pairs'.format(len(pairs)))

    print('Counting words...')
    for pair in pairs:
        question_lang.addSentence(pair[0])
        answer_lang.addSentence(pair[1])
    print('Counted words:')

    print(question_lang.name, question_lang.num_of_words)
    print(answer_lang.name, answer_lang.num_of_words)
    
    return question_lang, answer_lang, pairs
