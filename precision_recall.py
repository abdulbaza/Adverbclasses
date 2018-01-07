import collections
import sys
import random
import pylab as pl
from sklearn import svm, datasets
from sklearn.metrics import precision_recall_curve
from sklearn.metrics import auc

adverbs = [
('FREQUENCY', ['often', 'generally', 'always', 'rarely', 'never', 'usually', 'normally', 'ever', 'hardly', 'sometimes']),
('LOCATION_DEFINITE_TIME', ['earlier', 'up', 'now', 'then', 'here', 'there','afterwards', 'once', 'today', 'down']),
('DURATION' , ['briefly', 'momentarily', 'forever', 'temporarily', 'shortly', 'constantly','permanently', 'repeatedly', 'regularly', 'occasionally']),
('ASPECTUAL_INDEFINITE_TIME', ['still', 'already', 'yet', 'eventually','finally','ultimately','ago','nearly','previously','formerly']),
('FOCUSING', ['even', 'only', 'merely', 'just', 'solely', 'precisely','simply','purely','exactly','particularly']),
('SPEAKER_ORIENTED', ['particularly', 'indeed','probably', 'clearly', 'necessarily','seriously','remarkably','unfortunately','certainly','especially']),
('SUBJECT_ORIENTED', ['intentionally', 'deliberately','heavily', 'accurately', 'perfectly','effectively','quickly','carefully','correctly','secretly']),
('EXOCOMPARATIVE', ['similarly', 'likewise','accordingly','closely','comparably','consequently','additionally','alternatively','equally','hence']),
('PURE_MANNER', ['roughly', 'directly', 'indirectly', 'tightly', 'strongly','actively','firmly','formally','perfectly','publicly']),
('DOMAIN', ['internationally', 'academically','economically', 'legally','evolutionarily','politically','culturally','socially','historically','nominally']),
('WH_ADVERB', ['when', 'where', 'why', 'how', 'whence']),
('CONJUNCTIVE_ADVERB', ['otherwise','furthermore','however','instead','moreover','meanwhile','nonetheless','rather','thereafter','therefore'])
]
adverbs = collections.OrderedDict(adverbs)

def count_from_file(filename):
    sub_classes = {}
    counts = {}
    target = None
    with open(filename, 'r+') as f:
        temp = None
        for line in f:
            if not line.startswith('Similar') and not line.startswith('(') and not line.startswith('Count'):
                if temp:
                    temp[target] = result
                    sub_classes[c] = temp
                c = line.strip()
                temp = {}
                new = True
            elif line.startswith('Similar'):
                if target and not new:
                    temp[target] = result
                target = line.split()[-1]
                result = []
                new = False
            elif line.startswith('('):
                result.append(line.split("'")[1])
            elif line.startswith('Count'):
                counts[target] = float(line.split()[-1])
    if temp:
        temp[target] = result
        sub_classes[c] = temp
    return sub_classes, counts


sub_classes, counts = count_from_file(sys.argv[1])


recall = {}
for c in sub_classes:
    n_targets = len(sub_classes[c])
    r = .0
    for target in sub_classes[c]:
        r += len(sub_classes[c][target])/float(n_targets)

    recall[c] = r/float(n_targets)

precision = {}
for c in sub_classes:
    appeared = set()
    n_targets = len(sub_classes[c])
    for target in sub_classes[c]:
        appeared.update(sub_classes[c][target])
    print(appeared)
    p = .0
    for target in sub_classes[c]:
        if counts[target] != 0:
            p += float(len(sub_classes[c][target]))/counts[target]

    precision[c] = p/float(n_targets)

recall_sorted_keys = sorted(recall, key=lambda x: recall[x])
precision_val = [precision[x] for x in recall_sorted_keys]
recall_val = [recall[x] for x in recall_sorted_keys]

area = auc(recall_val, precision_val)
print("Area Under Curve: %0.2f" % area)

pl.clf()
pl.plot(recall_val, precision_val, label='Precision-Recall curve')
pl.xlabel('Recall')
pl.ylabel('Precision')
pl.ylim([0.0, 1.05])
pl.xlim([0.0, 1.0])
pl.title(sys.argv[3] + " Cosine Threshold =" + sys.argv[2] + ": AUC=%0.2f" % area)
pl.legend(loc="lower left")
pl.savefig(sys.argv[4])


print 'Precision:'
print(precision)
print 'Recall:'
print(recall)
print recall_val
