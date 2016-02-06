import collections
from nltk import metrics


def precision_recall(classifier, testfeats):
    refsets = collections.defaultdict(set)
    testsets = collections.defaultdict(set)
    for i, (feats, label) in enumerate(testfeats):
        refsets[label].add(i)
        observed = classifier.classify(feats)
        testsets[observed].add(i)

    precisions = {}
    recalls = {}

    for label in classifier.labels():
        precisions[label] = metrics.precision(refsets[label], testsets[label])
        recalls[label] = metrics.recall(refsets[label], testsets[label])

    return precisions, recalls
