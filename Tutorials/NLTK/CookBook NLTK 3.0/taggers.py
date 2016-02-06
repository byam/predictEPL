from nltk.tag import NgramTagger
from nltk.tag import SequentialBackoffTagger
from nltk.corpus import wordnet
from nltk.probability import FreqDist
from nltk.corpus import names


class QuadgramTagger(NgramTagger):
    def __init__(self, *args, **kwargs):
        NgramTagger.__init__(self, 4, *args, **kwargs)


# Now we can create a class that will look up words in WordNet,
# and then choose the most common tag from the Synsets it finds.
class WordNetTagger(SequentialBackoffTagger):
    '''
    >>> wt = WordNetTagger()
    >>> wt.tag(['food', 'is', 'great'])
    [('food', 'NN'), ('is', 'VB'), ('great', 'JJ')]
    '''
    def __init__(self, *args, **kwargs):
        SequentialBackoffTagger.__init__(self, *args, **kwargs)

        self.wordnet_tag_map = {
            'n': 'NN',
            's': 'JJ',
            'a': 'JJ',
            'r': 'RB',
            'v': 'VB'
        }

    def choose_tag(self, tokens, index, history):
        word = tokens[index]
        fd = FreqDist()

        for synset in wordnet.synsets(word):
            fd[synset.pos()] += 1

        if not fd:
            return None
        return self.wordnet_tag_map.get(fd.max())


class NamesTagger(SequentialBackoffTagger):
    '''
    >>> nt = NamesTagger()
    >>> nt.tag(['Jacob'])
    [('Jacob', 'NNP')]
    '''
    def __init__(self, *args, **kwargs):
        SequentialBackoffTagger.__init__(self, *args, **kwargs)
        self.name_set = set([n.lower() for n in names.words()])

    def choose_tag(self, tokens, index, history):
        word = tokens[index]

        if word.lower() in self.name_set:
            return 'NNP'
        else:
            return None
