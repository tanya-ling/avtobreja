import codecs
from pymystem3 import Mystem

letters = {
    'й': 'q',
    'ц': 'w',
    'у': 'e',
    'к': 'r',
    'е': 't',
    'ё': 't',
    'н': 'y',
    'г': 'u',
    'ш': 'i',
    'щ': 'o',
    'з': 'p',
    'х': 'O',
    'ъ': 'P',
    'ф': 'a',
    'ы': 's',
    'в': 'd',
    'а': 'f',
    'п': 'g',
    'р': 'h',
    'о': 'j',
    'л': 'k',
    'д': 'l',
    'ж': 'K',
    'э': 'L',
    'я': 'z',
    'ч': 'x',
    'с': 'c',
    'м': 'v',
    'и': 'b',
    'т': 'n',
    'ь': 'm',
    'б': 'N',
    'ю': 'M',
}

def kill_cyr(text):
    new_text = ''
    for letter in text:
        try:
            new_text += letters[letter]
        except KeyError:
            new_text += letter
    return new_text
KEYWORDS = {
    1: 'меч копье живой'.split(' '),
    2: 'фанерный деревянный лист'.split(' '),
    6: 'рекламный реклама фанерный'.split(' '),
    8: 'мяч кольцо под'.split(' '),
    9: 'доска дощечка фанерный'.split(' '),
    10: 'железо магма кора'.split(' '),
    11: 'прибор кнопка панель'.split(' '),
    13: 'пожарный распределительный пробка'.split(' '),
    14: 'атомный воздушный ядерный'.split(' '),
}

mystem = Mystem()

f = codecs.open('щит.csv', 'r', 'cp1251')
ds = codecs.open('shit_dataset.csv', 'w', 'utf-8')
first = True
for line in f:
    found = False
    if first:
        ds.write('sent;class;prev_lemma;prev_pos;next_lemma;next_pos;kw_1;kw_2;kw_6;kw_8;kw_9;kw_10;kw_11;kw_13;kw_14\r\n')
        first = False
        continue
    data = line.rstrip().split(';')
    try:
        sent = data[1]
        clas = data[0]
    except IndexError:
        print('no data', line)
        continue
    sent_parsed = mystem.analyze(sent)
    kw_1 = 0
    kw_2 = 0
    kw_6 = 0
    kw_8 = 0
    kw_9 = 0
    kw_10 = 0
    kw_11 = 0
    kw_13 = 0
    kw_14 = 0
    for token_i in range(len(sent_parsed)):
        if 'analysis' in sent_parsed[token_i]:
            try:
                if sent_parsed[token_i]['analysis'][0]['lex'] in KEYWORDS[1]:
                    kw_1 += 1
                if sent_parsed[token_i]['analysis'][0]['lex'] in KEYWORDS[2]:
                    kw_2 += 1
                if sent_parsed[token_i]['analysis'][0]['lex'] in KEYWORDS[6]:
                    kw_6 += 1
                if sent_parsed[token_i]['analysis'][0]['lex'] in KEYWORDS[8]:
                    kw_8 += 1
                if sent_parsed[token_i]['analysis'][0]['lex'] in KEYWORDS[9]:
                    kw_9 += 1
                if sent_parsed[token_i]['analysis'][0]['lex'] in KEYWORDS[13]:
                    kw_13 += 1
                if sent_parsed[token_i]['analysis'][0]['lex'] in KEYWORDS[10]:
                    kw_10 += 1
                if sent_parsed[token_i]['analysis'][0]['lex'] in KEYWORDS[11]:
                    kw_11 += 1
                if sent_parsed[token_i]['analysis'][0]['lex'] in KEYWORDS[14]:
                    kw_14 += 1
            except IndexError:
                print('why indexerror there?', sent_parsed[token_i])
        try:
            if sent_parsed[token_i]['analysis'][0]['lex'] == 'щит':
                found = True
                try:
                    prev_lemma = sent_parsed[token_i-2]['analysis'][0]['lex']
                    prev_pos = sent_parsed[token_i-2]['analysis'][0]['gr'].split(',')[0]
                except KeyError:
                    # print('Key error', sent, sent_parsed, sent_parsed[token_i - 1], sent_parsed[token_i])
                    prev_lemma = 'not_word'
                    prev_pos = 'not_word'
                try:
                    next_lemma = sent_parsed[token_i+2]['analysis'][0]['lex']
                    next_pos = sent_parsed[token_i+2]['analysis'][0]['gr'].split(',')[0]
                except KeyError:
                    next_lemma = 'not_word'
                    next_pos = 'not_word'
                # break
        except KeyError:
            continue
        except IndexError:
            print('indexerror', sent_parsed[token_i])
    if found:
        ds.write(kill_cyr(';'.join([sent, clas, prev_lemma, prev_pos, next_lemma, next_pos, str(kw_1), str(kw_2), str(kw_6), str(kw_8), str(kw_9), str(kw_10), str(kw_11), str(kw_13), str(kw_14)]) + '\r\n'))
        continue
    print('not found', sent_parsed)
ds.close()

