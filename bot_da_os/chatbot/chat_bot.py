from bot_da_os.statemachine.state import StateMachine, State
from bot_da_os.statemachine.person import person_action

import sys
sys.path += ['../statemachine', '../person']


class Waiting(State):
    def run(self):
        print("Waiting: Waiting for request")

    def next(self, input):
        if input == person_action.query:
            return ChatBot.processing
        return ChatBot.waiting


class Processing(State):
    def run(self):
        print("Processing: Receiving information")

    def store(self, input):
        # here check if it has all the information
        ...

    def next(self, store):
        if store:
            return ChatBot.tracking
        return ChatBot.processing


class Tracking(State):
    def run(self):
        print("Tracking: Order sent, following it")

    def status(self, input):
        # here communicates with the db
        ...

    def next(self, status):
        if status:
            return ChatBot.waiting
        return ChatBot.tracking


class ChatBot(StateMachine):
    def __init__(self):
        # Initial state
        StateMachine.__init__(self, ChatBot.waiting)


# Static variable initialization:
ChatBot.waiting = Waiting()
ChatBot.processing = Processing()
ChatBot.tracking = Tracking()


moves = map(str.strip, open("../statemachine/person/person_moves.txt").readlines())
ChatBot().run_all(map(person_action, moves))