# module to process the natural language

import re
import nltk
# import string


# function will receive a message string and return a tuple (message_type, info)
def person_interpreter(message: object, state: str) -> tuple:
    msg = message.__str__().lower()
    words = nltk.word_tokenize(msg)

    if state == "Waiting":
        if re.search(r'^.*(obrigado|boa|valeu|obg|vlw|thanks|thx).*$', msg):
            message.action = 'thanks'
        elif re.search(r'^.*(quero|gostaria|poderia|preciso|estou).*$', msg):
            message.action = 'request'
        elif re.search(r'^.*(oi|ola|ei|olá|hey|bom dia|boa tarde|boa noite|opa).*$', msg):
            message.action = 'greet'
        else:
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

    elif state == "ReceivingProblemType":
        # lista de tipos
        # re.search("", words)
        return message, None

    elif state == "ReceivingRoom":
        return message, None

    elif state == "ReceivingDescription":
        return message, None

    elif state == "Tracking":
        return message, None

    elif state == "Finishing":
        return message, None

    else:
        return message, None
