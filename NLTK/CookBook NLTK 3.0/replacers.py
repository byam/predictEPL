import re
# import enchant
from nltk.metrics import edit_distance
from nltk.corpus import wordnet

replacement_patterns = [
     (r'won\'t', 'will not'),
     (r'can\'t', 'cannot'),
     (r'i\'m', 'i am'),
     (r'ain\'t', 'is not'),
     (r'(\w+)\'ll', '\g<1> will'),
     (r'(\w+)n\'t', '\g<1> not'),
     (r'(\w+)\'ve', '\g<1> have'),
     (r'(\w+)\'s', '\g<1> is'),
     (r'(\w+)\'re', '\g<1> are'),
     (r'(\w+)\'d', '\g<1> would')
]


class RegexpReplacer(object):
    def __init__(self, patterns=replacement_patterns):
        self.patterns = [(re.compile(regex), repl)
                         for (regex, repl) in patterns]

    def replace(self, text):
        s = text
        for (pattern, repl) in self.patterns:
            s = re.sub(pattern, repl, s)
        return s


class RepeatReplacer(object):
    def __init__(self):
        self.repeat_regexp = re.compile(r'(\w*)(\w)\2(\w*)')
        self.repl = r'\1\2\3'

    def replace(self, word):
        repl_word = self.repeat_regexp.sub(self.repl, word)
        if repl_word != word:
            return self.replace(repl_word)
        else:
            return repl_word


class RepeatReplacerWordNet(object):
    def __init__(self):
        self.repeat_regexp = re.compile(r'(\w*)(\w)\2(\w*)')
        self.repl = r'\1\2\3'

    def replace(self, word):
        if wordnet.synsets(word):
            return word
        repl_word = self.repeat_regexp.sub(self.repl, word)
        if repl_word != word:
            return self.replace(repl_word)
        else:
            return repl_word


# the replace() method will check Enchant
# to see whether the word is valid.
# If not, we will look up the suggested alternatives
# and return the best match using nltk.metrics.edit_distance():
class SpellingReplacer(object):
    def __init__(self, dict_name='en', max_dist=2):
        self.spell_dict = enchant.Dict(dict_name)
        self.max_dist = max_dist

    def replace(self, word):
        if self.spell_dict.check(word):
            return word
        suggestions = self.spell_dict.suggest(word)
        if suggestions and\
                edit_distance(word, suggestions[0]) <= self.max_dist:
            return suggestions[0]
        else:
            return word
