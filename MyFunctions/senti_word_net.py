from nltk.corpus import sentiwordnet as swn


def wordnet_sanitize(word):
    """
    Ensure that word is a (string, pos) pair that WordNet can understand.

    Argument: word (str, str) -- a (string, pos) pair

    Value: a possibly modified (string, pos) pair, where pos=None if
    the input pos is outside of WordNet.
    """
    string, tag = word
    string = string.lower()
    tag = tag.lower()
    if tag.startswith('v'):
        tag = 'v'
    elif tag.startswith('n'):
        tag = 'n'
    elif tag.startswith('j'):
        tag = 'a'
    elif tag.startswith('rb'):
        tag = 'r'
    if tag in ('a', 'n', 'r', 'v'):
        return (string, tag)
    else:
        return (string, None)


def senti_word_net_word(word):
    pos_score = 0.0
    neg_score = 0.0
    obj_score = 0.0

    string, tag = word

    if tag is None:
        return pos_score, neg_score, obj_score

    wordList = list(swn.senti_synsets(string, tag))

    word_num = len(wordList)

    if word_num:
        for word in wordList:
            pos_score += word.pos_score()
            neg_score += word.neg_score()
            obj_score += word.obj_score()

        return pos_score/word_num, neg_score/word_num, obj_score/word_num

    return pos_score, neg_score, obj_score


def pos_neg_score_words(words):
    pos_score = 0.0
    neg_score = 0.0
    obj_score = 0.0

    senti_words = 0

    for word in words:
        p, n, o = senti_word_net_word(word)

        if p or n:
            pos_score += p
            neg_score += n
            obj_score += o

            # senti_words += 1

    # if senti_words:
        # return pos_score/senti_words, neg_score/senti_words, obj_score/senti_words

    return pos_score, neg_score, obj_score
