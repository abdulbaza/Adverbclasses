import gensim
import collections
m = gensim.models.KeyedVectors.load_word2vec_format('depwordsw2vf.txt')
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
('DOMAIN', ['internationally', 'academically','economically', 'legally','evolutionarily','politically','economically','culturally','socially','historically','nominally']),
('WH_ADVERB', ['when', 'where', 'why', 'how', 'whence']),
('CONJUNCTIVE_ADVERB', ['otherwise','furthermore','however','instead','moreover','meanwhile','nonetheless','rather','thereafter','therefore'])
]
adverbs = collections.OrderedDict(adverbs)
threshold = 0.75
for c in adverbs:
    print c
    vocab = adverbs[c]
    for w in vocab:
        print('Similar to {}'.format(w))
        res = m.most_similar(w,topn=5000)
        count = 0
        for v,i in res:
            if i>=threshold:
                count += 1
                if v in vocab:
                    print(v,i)
        print 'Counts: ' + str(count)
        print
