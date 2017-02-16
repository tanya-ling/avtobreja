import re
import numpy as np
from matplotlib import pyplot as plt, mlab
from sklearn.tree import DecisionTreeClassifier
from sklearn import metrics
import random


def median(lst):
    return np.median(np.array(lst))


def lenletters(sent):
    # print(sent)
    # print(len(re.sub('[,()\-\'":; \r\n]', '', sent)))
    return len(re.sub('[,()\-\'":; \r\n]', '', sent))


def letternumbers1(sent):
    letters = set(list(sent))
    # print(sent)
    # print(len(letters & (cons | vow)))
    return len(letters & (cons | vow | {'ь', 'ъ'}))


def letternumbers2(sent):
    letters = [t for t in list(sent) if t in vow]
    # print(sent)
    # print(len(letters))
    return len(letters)


def medians1(sent):
    sent = re.sub('[,()\-\'":;]', '', sent)
    sent = re.split('[ \r\n]', sent)
    medlet = median([len(x) for x in sent])
    return medlet


def medians2(sent):
    sent = re.sub('[,()\-\'":;]', '', sent)
    sent = re.split('[ \r\n]', sent)
    medvow = median([len(re.sub('[йцкнгшщзхъфвпрлджчсмтьб]', '', x)) for x in sent])
    return medvow


def mainfirst():

    with open('korenina.txt', encoding='utf-8') as f:
        anna = f.read().lower()
    with open('shkspr.txt', encoding='utf-8') as f:
        sonets = f.read().lower()

    anna_sentences = re.split(r'(?:[.]\s*){3}|[.?!]', anna)
    sonet_sentences = re.split(r'(?:[.]\s*){3}|[.?!]', sonets)

    anna_data = [(lenletters(sentence), letternumbers1(sentence), letternumbers2(sentence), medians1(sentence), medians2(sentence))
                 for sentence in anna_sentences if lenletters(sentence) > 0]

    sonet_data = [(lenletters(sentence), letternumbers1(sentence), letternumbers2(sentence), medians1(sentence), medians2(sentence))
                  for sentence in sonet_sentences if lenletters(sentence) > 0]

    anna_data = np.array(anna_data)
    sonet_data = np.array(sonet_data)

    anna_sentences = [t for t in anna_sentences if lenletters(t) > 0]
    sonet_sentences = [t for t in sonet_sentences if lenletters(t) > 0]
    data = np.vstack((anna_data, sonet_data))
    p = mlab.PCA(data, True)
    N = len(anna_data)
    plt.plot(p.Y[:N, 0], p.Y[:N, 1], 'or', p.Y[N:, 0], p.Y[N:, 1], 'sb')
    plt.title('кажется, ничего не скажешь на основании этих параметров :(')

    return anna_data, sonet_data, anna_sentences, sonet_sentences


def main():
    ann_data, son_data, anna_sentences, sonet_sentences = mainfirst()
    all_sent = anna_sentences + sonet_sentences

    tr_anna = random.sample(range(len(ann_data)), 1000)
    tr_sonet = random.sample(range(len(son_data)), 1000)
    training_anna = [ann_data[i] for i in tr_anna]
    training_sonet = [son_data[i] for i in tr_sonet]
    train_data = training_anna + training_sonet
    test_anna = [ann_data[i] for i in range(len(ann_data)) if i not in tr_anna]
    test_sonet = [son_data[i] for i in range(len(son_data)) if i not in tr_sonet]
    test_data = test_anna + test_sonet

    clf = DecisionTreeClassifier(min_samples_leaf=2)
    clf.fit(train_data, ['anna' for i in range(1000)] + ['sonets' for i in range(1000)])

    expected = ['anna' for i in range(len(test_anna))] + ['sonets' for i in range(len(test_sonet))]
    predicted = clf.predict(test_data)

    print(metrics.classification_report(expected, predicted))

    j = 0
    for k in range(len(expected)):
            if expected[k] != predicted[k]:
                # print(test_data[k])
                print(all_sent[k])
                j += 1
            if j == 3:
                break

    plt.show()


cons = set(list('йцкнгшщзхфвпрлджчсмтб'))
vow = set(list('уеыаоэяию'))
main()
