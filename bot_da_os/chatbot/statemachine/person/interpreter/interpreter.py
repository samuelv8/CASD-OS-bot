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
            m, t = word_find(w, 1, dicw)
            if t > -1:
                message.action = 'thanks'
                if t == 0:
                    message.sure = False
                return message, m
            m, t = word_find(w, 2, dicw)
            if t > -1:
                message.action = 'request'
                if t == 0:
                    message.sure = False
                return message, m
            m, t = word_find(w, 3, dicw)
            if t > -1:
                message.action = 'greet'
                if t == 0:
                    message.sure = False
                return message, m
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
            m, t = word_find(w, 6, dicw)
            if t > -1:
                message.action = 'yes'
                if t == 0:
                    message.sure = False
                return message, m
            m, t = word_find(w, 7, dicw)
            if t > -1:
                message.action = 'no'
                if t == 0:
                    message.sure = False
                return message, m
            m, t = word_find(w, 4, dicw)
            if t > -1:
                message.action = 'proom'
                if t == 0:
                    message.sure = False
                return message, m
            m, t = word_find(w, 8, dicw)
            if t > -1:
                message.action = 'proom'
                if t == 0:
                    message.sure = False
                return message, m
            m, t = word_find(w, 9, dicw)
            if t > -1:
                message.action = 'proom'
                if t == 0:
                    message.sure = False
                lc = re.search(r'[abc] *[+\-]|mais|menos', msg)
                if lc:
                    r_lc = m + ' ' + lc.group(0)
                    return message, r_lc
        message.action = 'unknown'
        return message, None

    elif state == "ReceivingProblemType":
        for w in words:
            m, t = word_find(w, 5, dicw)
            if t > -1:
                message.action = 'ptype'
                if t == 0:
                    message.sure = False
                return message, m
            m, t = word_find(w, 6, dicw)
            if t > -1:
                message.action = 'yes'
                if t == 0:
                    message.sure = False
                return message, m
            m, t = word_find(w, 7, dicw)
            if t > -1:
                message.action = 'no'
                if t == 0:
                    message.sure = False
                return message, m
        message.action = 'unknown'
        return message, None

    elif state == "ReceivingDescription":
        message.action = 'pdescr'
        return message, msg

    elif state == "Tracking":
        for w in words:
            m, t = word_find(w, 2, dicw)
            if t > -1:
                message.action = 'status'
                if t == 0:
                    message.sure = False
                return message, m
            m, t = word_find(w, 10, dicw)
            if t > -1:
                message.action = 'angry'
                if t == 0:
                    message.sure = False
                return message, m
        message.action = 'unknown'
        return message, None

    else:
        raise Exception("Error: Invalid State.")


# # this could be useful to diminish repetition
# def is_at(word: str, group: int, message: object, action: str):
#     m, t = word_find(word, group, dicw)
#     if t > -1:
#         message.action = action
#         if t == 0:
#             message.sure = False
#         return message, m


# function will try any match from word in a given dict, using Levenshtein distance, and return a tuple (match, type)
def word_find(word: str, group: int, base_dic: dict):
    normalized_levenshtein = NormalizedLevenshtein()
    dist = {}
    for k, v in base_dic.items():
        if v == group:
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
words_1 = ['obrigado', 'valeu', 'obg', 'vlw', 'thanks', 'thx']
words_2 = ['quero', 'gostaria', 'poderia', 'preciso', 'estou', 'situação', 'ei', 'ow', 'aí', 'eai', 'status', 'está']
words_3 = ['oi', 'ola', 'olá', 'hey', 'bom', 'dia', 'boa', 'tarde', 'noite', 'opa']
words_4 = ['quarto', 'vaga', 'cozinha', 'banheiro', 'apartamento', 'ap', 'sarcofago']
words_5 = ['eletrico', 'encanamento', 'geral', 'mofo', 'estrutura', 'cama', 'infiltracao', 'vazamento', 'porta',
           'janela', 'piso', 'mesa', 'lâmpada', 'chuveiro', 'parede']
words_6 = ['sim', 'yes', 'é', 'isso', 'eh', 'exato', 'exatamente', 'uhum', 'aham']
words_7 = ['não', 'no', 'nao', 'nn', 'n', 'nem', 'nope']
# Words_8 is about common places which do not expect a letter as coordinate (such as Hall do C - place + letter)
words_8 = ['feijao', 'hallzinho', 'halzinho', 'comum', 'sala', 'jogos', 'gaga', 'lavanderia',
           'lavanderita', 'academia', 'maromba', 'musica', 'piano', 'bandas', 'piscina', 'quiosque',
           'adm', 'administracao', 'telhado', 'telhados']
# words_9, in the other hand, expects a letter coordinate
words_9 = ['hall', 'hal', 'corredor', 'jardins', 'jardim', 'gramado', 'quadra']
# person is pissed off
words_10 = ['caramba', 'casd', 'cade', 'poxa', 'bora', 'pior', 'aguento', 'ah', 'difícil', 'sugou', 'ocasdpara']

word_lists = [words_1, words_2, words_3, words_4, words_5, words_6, words_7, words_8, words_9, words_10]
dicw = {}
i = 0
for l in word_lists:
    i += 1
    for a in l:
        dicw[a] = i
