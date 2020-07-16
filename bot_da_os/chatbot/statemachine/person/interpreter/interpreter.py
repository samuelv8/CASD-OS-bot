# module to process the natural language

import re
import nltk
from similarity.normalized_levenshtein import NormalizedLevenshtein
from unicodedata import normalize


# function will receive a message string and return a tuple (message_type, info)
def person_interpreter(message: object, state: str) -> tuple:
    msg = message.__str__().lower()
    msg_ascii = normalize('NFKD', msg).encode('ASCII', 'ignore').decode('ASCII')
    words = nltk.word_tokenize(msg_ascii)

    if state == "Waiting":
        for w in words:
            m, t = word_find(w, 11, dicw)
            if t > -1:
                message.action = 'status'
                if t == 0:
                    message.sure = False
                return message, m
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
                lc = re.findall(r'^.* +([abc]).*([+\-]).*$', msg_ascii)
                if lc is not None:
                    r_lc = m + ' ' + lc[0][0] + lc[0][1]
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
        message.action = 'unknown'
        return message, None

    elif state == "ReceivingDescription":
        message.action = 'pdescr'
        return message, msg

    elif state == "Tracking":
        for w in words:
            m, t = word_find(w, 11, dicw)
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

    elif state == "Deciding":  # to 'yes' or 'no' answers (it's not a State itself)
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
        message.action = 'no'  # denial by default

    else:
        raise Exception("Error: Invalid State.")


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


######################################################################################################################
# Word database
# 1: Words related to acknowledgment
words_1 = ['obrigado', 'valeu', 'obg', 'vlw', 'thanks', 'thx']
# 2: Words to request
words_2 = ['quero', 'gostaria', 'poderia', 'preciso', 'estou', 'favor']
# 3: Words related to greeting
words_3 = ['oi', 'ola', 'hey', 'bom', 'dia', 'boa', 'tarde', 'noite', 'opa', 'ei', 'ow', 'ai']
# 4: Words to (private) rooms
words_4 = ['quarto', 'vaga', 'cozinha', 'banheiro', 'apartamento', 'ap', 'sarcofago', 'entrada', 'box', 'tras',
           'atras', 'banhero', 'toalete']
# 5: Words related to problem types
words_5 = ['eletrico', 'encanamento', 'geral', 'mofo', 'estrutura', 'cama', 'infiltracao', 'vazamento', 'porta',
           'janela', 'piso', 'mesa', 'lâmpada', 'chuveiro', 'parede', 'entupido', 'entupida', 'fio', 'teto']
# 6: Words to agree
words_6 = ['sim', 'yes', 'isso', 'eh', 'exato', 'exatamente', 'uhum', 'aham']
# 7: Words to disagree
words_7 = ['no', 'nao', 'nem', 'nope']
# 8: Words to common places which do not expect a letter as coordinate (such as Hall do C - place + letter)
words_8 = ['feijao', 'hallzinho', 'halzinho', 'comum', 'sala', 'jogos', 'gaga', 'lavanderia',
           'lavanderita', 'academia', 'maromba', 'musica', 'piano', 'bandas', 'piscina', 'quiosque',
           'adm', 'administracao', 'telhado', 'telhados']
# 9: Words to common places which do expects a letter coordinate
words_9 = ['hall', 'hal', 'corredor', 'jardins', 'jardim', 'gramado', 'quadra']
# 10: Words related to rage
words_10 = ['caramba', 'casd', 'cade', 'poxa', 'bora', 'pior', 'aguento', 'ah', 'dificil', 'sugou', 'ocasdpara']
# 11: Words related to status
words_11 = ['situacao', 'status', 'eai', 'esta', 'entao']

word_lists = [words_1, words_2, words_3, words_4, words_5, words_6, words_7, words_8, words_9, words_10, words_11]
dicw = {}
i = 0
for l in word_lists:
    i += 1
    for a in l:
        dicw[a] = i
