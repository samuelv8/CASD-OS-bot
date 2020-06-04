# module to process the natural language

import re
import nltk
from similarity.normalized_levenshtein import NormalizedLevenshtein


# function will receive a message string and return a tuple (message_type, info)
def person_interpreter(message: object, state: str) -> tuple:
    msg = message.__str__().lower()
    words = nltk.word_tokenize(msg)

    if state == "Waiting":
        for w in words:
            if word_find(w, 1, dicw)[1] == 1:
                message.action = 'thanks'
                return message, None
            elif word_find(w, 2, dicw)[1] == 1:
                message.action = 'request'
                return message, None
            elif word_find(w, 3, dicw)[1] == 1:
                message.action = 'greet'
                return message, None
        message.action = 'unknown'
        return message, None

    elif state == "ReceivingName":
        if len(words) >= 2:
            message.action = 'name'
            trash_rm = re.compile(r'^(?!é|eh|e|meu|nome|o|sobrenome)(\w+)$')
            words = filter(trash_rm.search, words)
        else:
            message.action = 'unknown'
        return message, words

    elif state == "ReceivingApartment":
        apartment = []
        for word in words:
            match = re.search(r'^([1-3][0-4][0-9])$|^([a-f])$', word)
            if match:
                apartment.append(match.group(0))
        if len(apartment) == 2:
            message.action = 'apartment'
        else:
            message.action = 'unknown'
        return message, apartment

    elif state == "ReceivingRoom":
        for w in words:
            r = word_find(w, 4, dicw)
            if r[1] == 1:
                message.action = 'proom'
                return message, r[0]
        # else:  # aqui deve achar informações em mais de uma palavra. Ex.: Hall do B
            # prob_room = re.search(r'^.*(hall[abc]|corredor).*$', msg)
            # if prob_room:
        message.action = 'unknown'
        return message, None

    elif state == "ReceivingProblemType":
        for w in words:
            r = word_find(w, 5, dicw)
            if r[1] == 1:
                message.action = 'ptype'
                return message, r[0]

        message.action = 'unknown'
        return message, None

    elif state == "ReceivingDescription":
        return message, None

    elif state == "Tracking":
        return message, None

    elif state == "Finishing":
        return message, None

    else:
        return message, None


# function will try any match from word in a given dict, using Levenshtein distance, and return a tuple (match, type)
def word_find(word: str, key: int, dic: dict):
    normalized_levenshtein = NormalizedLevenshtein()
    dist = {}
    for k, v in dic.items():
        if v == key:
            dist[k] = 1.0

    for k, v in dist.items():
        dist[k] = normalized_levenshtein.distance(word, k)

    ordered_dist = {k: v for k, v in sorted(dist.items(), key=lambda item: item[1])}
    best_match = next(iter(ordered_dist.items()))
    if best_match[1] < 0.1:
        return best_match[0], 1  # 1 for exact match
    if best_match[1] < 0.3:
        return best_match[0], 0  # 0 for partial match
    return None, -1  # -1 for no match


##################################################################################################################
# Word database
words_1 = ['obrigado', 'boa', 'valeu', 'obg', 'vlw', 'thanks', 'thx']
words_2 = ['quero', 'gostaria', 'poderia', 'preciso', 'estou']
words_3 = ['oi', 'ola', 'ei', 'olá', 'hey', 'bom dia', 'boa tarde', 'boa noite', 'opa']
words_4 = ['quarto', 'vaga', 'cozinha', 'banheiro', 'apartamento', 'ap', 'sarcófago']
words_5 = ['elétrico', 'encanamento', 'geral', 'mofo', 'estrutura', 'cama', 'infiltração', 'vazamento', 'porta',
           'janela', 'piso', 'mesa', 'lâmpada', 'chuveiro', 'parede']

word_lists = [words_1, words_2, words_3, words_4, words_5]
dicw = {}
i = 0
for l in word_lists:
    i += 1
    for a in l:
        dicw[a] = i
