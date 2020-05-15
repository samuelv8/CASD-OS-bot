from bot_da_os.statemachine.person.person_action import PersonAction
from bot_da_os.statemachine.state import State
from bot_da_os.statemachine.state_machine import StateMachine
from random import randint
import sys
sys.path += ['../statemachine', '../person']

# NOTES:
# -'next' methods must be updated!
# -need more classes


class Waiting(State):
    def run(self, first=True):
        print("        [Waiting: Waiting for request]")

    def next(self, inputs, info=None):
        if inputs == PersonAction.request or inputs == PersonAction.informing:
            return ChatBot.processing
        elif inputs == PersonAction.greet or inputs == PersonAction.angry:
            print("-- Hi! How can I help you?")
        elif inputs == PersonAction.thanks:
            print("-- You're welcome! #ocasdnaopara")
        return ChatBot.waiting


class Processing(State):
    def run(self, first=True):
        if first:
            print("-- Can you tell me the information bla bla?")
        print("        [Processing: Receiving information]")

    @staticmethod
    def store(inputs):
        # here check if it has all the information
        if inputs == PersonAction.informing:
            print("-- Can you brief the problem?")
        elif inputs == PersonAction.briefing:
            return True
        return False

    def next(self, inputs, info=None):
        if Processing.store(inputs):
            return ChatBot.tracking
        return ChatBot.processing


class Tracking(State):
    def run(self, first=True):
        if first:
            print("-- Okay, your request was recorded. If you want to know about it's status, tell me! ;)")
        print("        [Tracking: Order sent, following it]")

    @staticmethod
    def status():
        # here communicates with the db
        n = randint(0, 10)
        return n

    def next(self, inputs, info=None):
        if inputs == PersonAction.query or inputs == PersonAction.angry:
            n = Tracking.status()
            if not n:
                print("-- Your order is done!")
                return ChatBot.waiting
            else:
                print(f'Your order is in position {n} of the list')

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
ChatBot().run_all(map(PersonAction, moves))
print("############################################################################")
moves = map(str.strip, open("../statemachine/person/person_moves2.txt").readlines())
ChatBot().run_all(map(PersonAction, moves))
