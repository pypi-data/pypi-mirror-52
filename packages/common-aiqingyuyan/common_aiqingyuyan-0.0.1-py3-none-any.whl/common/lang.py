import string


SOS_Token = 0
UNK_Token = 1
EOS_Token = 2


class Lang:

    def __init__(self, name):
        self.name = name
        self.word2index = {}
        self.word2count = {}
        self.index2word= { 0: 'SOS', 1: 'UNK', 2: 'EOS' }
        self.num_of_words = 3  # initial count (SOS, UNK & EOS)
    

    def addSentence(self, sentence):
        assert isinstance(sentence, str), 'input sentence must be of type str'
        for word in sentence.split(' '):
            self.addWord(word)
    

    def addWord(self, word):
        if word not in self.word2index:
            self.word2index[word] = self.num_of_words
            self.word2count[word] = 1
            self.index2word[self.num_of_words] = word
            self.num_of_words += 1
        else:
            self.word2count[word] += 1


    def fromPickle(self, data):
        assert isinstance(data, (list, tuple)), 'data must be of type list/tuple'
        assert len(data) == 4, 'length of data is not equal to 4'
        self.word2index = data[0]
        self.word2count = data[1]
        self.index2word = data[2]
        self.num_of_words = data[3]
