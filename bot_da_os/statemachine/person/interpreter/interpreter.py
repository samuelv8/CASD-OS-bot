# module to process the natural language

import re
import nltk
import string

# function will receive a message string and return a tuple (message_type, info)
def person_interpreter(message: str, state) -> tuple:
    # print(state.__class__.__name__) use this to see the class name
    msg = message.lower()
    words = nltk.word_tokenize(msg)
    if state.__class__.__name__ == "Waiting":
        re.search("", words)
        return message, None
    elif state.__class__.__name__ == "Processing":
        re.search("", words)
        return message, None
    elif state.__class__.__name__ == "Tracking":
        re.search("", words)
        return message, None
    elif state.__class__.__name__ == "ReceivingName":
        return "name", msg
    elif state.__class__.__name__ == "ReceivingApartment":
        #lista de Aps e vagas
        Apartment = []
        for word in words:
            Apartment.append(re.search(r'(\d+).*(\w)', word))
        return message, Apartment
    elif state.__class__.__name__ == "ReceivingProblemType":
        #lista de tipos
        re.search("", words)
        return message, None
    elif state.__class__.__name__ == "ReceivingDescription":

        return message, None

