from nltk.probability import FreqDist, ConditionalFreqDist


def backoff_tagger(train_sents, tagger_classes, backoff=None):
    for cls in tagger_classes:
        backoff = cls(train_sents, backoff=backoff)

    return backoff


def word_tag_model(words, tagged_words, limit=200):
    fd = FreqDist(words)
    cfd = ConditionalFreqDist(tagged_words)

    most_freq = (word for word, count in fd.most_common(limit))

    return dict((word, cfd[word].max()) for word in most_freq)

patterns = [
    (r'^\d+$', 'CD'),  # cardinal numbers i.e 1 2 3
    (r'.*ing$', 'VBG'),  # gerunds, i.e. wondering
    (r'.*ment$', 'NN'),  # i.e. wonderment
    (r'.*ful$', 'JJ')  # i.e. wonderful
           ]
