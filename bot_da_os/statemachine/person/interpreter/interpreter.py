# module to process the natural language

import re
# import nltk
# import string


# function will receive a message string and return a tuple (message_type, info)
def person_interpreter(message: object, state: str) -> tuple:
    msg = message.__str__().lower()
    # print(msg)
    # words = nltk.word_tokenize(msg)
    if state == "Waiting":
        if re.search(r'^(oi)$', msg):
            message.action = 'greet'
        elif re.search(r'^(quero).*$', msg):
            message.action = 'request'
        else:
            message.action = 'unknown'
        print(message)
        return message, None
    elif state == "ReceivingName":
        return message, None
    elif state == "ReceivingApartment":
        # lista de Aps e vagas  # wut? -- samuel
        # apartment = []
        # for word in words:
        #     apartment.append(re.search(r'(\d+).*(\w)', word))
        return message, None
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
