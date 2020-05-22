# module to process the natural language

# import re
# import nltk
# import string


# function will receive a message string and return a tuple (message_type, info)
def person_interpreter(message: str, state) -> tuple:
    # print(state)  # use this to see the class name
    # msg = message.lower()
    # words = nltk.word_tokenize(msg)
    if state == "Waiting":
        # re.search("", words)
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
