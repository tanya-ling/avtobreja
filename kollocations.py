import nltk
import codecs
from nltk.collocations import *
from nltk.metrics.spearman import *
trigram_measures = nltk.collocations.TrigramAssocMeasures()

f = codecs.open('court-V-N.csv', 'r', 'utf-8')
gs = codecs.open('gold_standart.txt', 'r', 'utf-8')
gs_lines = gs.readlines()
gs.close()
i = 0
gs_matrix = [None for k in range(10)]

for line in gs_lines:
    gs_matrix[i] = line.rstrip().split(' ')
    i += 1

a = f.readlines()
f.close()
ab = [a[i].replace(', ', ',').rstrip().lower().split(' ,') for i in range(len(a))]


finder = TrigramCollocationFinder.from_documents(ab)

scored_trigrams1 = finder.score_ngrams(trigram_measures.raw_freq)
scored_trigrams2 = finder.score_ngrams(trigram_measures.likelihood_ratio)

def stupid_me(scored_trigrams1, gs_matrix):
    scored_trigrams1_gold = ['None' for k in range(10)]
    i = 0
    for trigram in sorted(scored_trigrams1, key = lambda x: x[1]):
        if list(trigram[0]) in gs_matrix:
            scored_trigrams1_gold[i] = list(trigram[0])
            i += 1
            if i == 10:
                break
    j = 1
    while 'None' in scored_trigrams1_gold:
                for k in gs_matrix:
                    if k not in scored_trigrams1_gold:
                        scored_trigrams1_gold[-j] = k
                        j += 1
    return scored_trigrams1_gold

scored_trigrams1_gold = stupid_me(scored_trigrams1, gs_matrix)
scored_trigrams2_gold = stupid_me(scored_trigrams2, gs_matrix)

gs_matrix = [' '.join(k) for k in gs_matrix]
scored_trigrams1_gold = [' '.join(k) for k in scored_trigrams1_gold]
scored_trigrams2_gold = [' '.join(k) for k in scored_trigrams2_gold]
print('raw_freq')
print('%0.1f' % spearman_correlation(ranks_from_sequence(gs_matrix), ranks_from_sequence(scored_trigrams1_gold)))
print('likelihood_ratio')
print('%0.1f' % spearman_correlation(ranks_from_sequence(gs_matrix), ranks_from_sequence(scored_trigrams2_gold)))
print('кажется, просто частотность работает лучше логлайклихуд, но всё не очень. Или я плохо зс сделала.')

