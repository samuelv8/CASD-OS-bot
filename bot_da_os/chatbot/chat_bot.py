from bot_da_os.statemachine.person.person_action import PersonAction
from bot_da_os.statemachine.state import State
from bot_da_os.statemachine.state_machine import StateMachine
from random import randint
import sys

sys.path += ['../statemachine', '../person']


# NOTES:
# -'next' methods must be updated!
# -need more classes
# -fix contradiction between state_machine and chat_bot
# -actually store the information obtained in interpreter
# -connect person_action to interpreter and chat_bot

class Waiting(State):
    def run(self, first=True):
        print("\t[Waiting: Waiting for request]")

    def next(self, inputs, info=None):
        if inputs == PersonAction.request or inputs == PersonAction.informing:
            return ChatBot.processing
        elif inputs == PersonAction.greet or inputs == PersonAction.angry:
            print("-- Hi! How can I help you?")
        elif inputs == PersonAction.thanks:
            print("-- You're welcome! #ocasdnaopara")
        return ChatBot.waiting


class ReceivingName(State):
    def run(self, first=True):
        if first:
            print("-- Can you tell me your name?")
        print("\t[ReceivingName: Receiving name]")

    @staticmethod
    def store(inputs):
        # here check if it has all the information
        if inputs == PersonAction.name:
            return True
        return False

    def next(self, inputs, info=None):
        if ReceivingName.store(inputs):
            return ChatBot.receiving_apartment
        print('it did not work, try again something like: "Fulano Silva"')
        return ChatBot.receiving_name


class ReceivingApartment(State):
    def run(self, first=True):
        if first:
            print("-- Can you tell me your apartment number and your spot letter?")
        print("\t[ReceivingApartment: Receiving Apartment]")

    @staticmethod
    def store(inputs):
        # here check if it has all the information
        if inputs == PersonAction.apartment:
            return True
        return False

    def next(self, inputs, info=None):
        if ReceivingApartment.store(inputs):
            return ChatBot.receiving_room
        print('it did not work, try again something like: "222 D"')
        return ChatBot.receiving_apartment

class ReceivingProblemType(State):
    def run(self, first=True):
        if first:
            print("-- Can you tell me the nature of your problem?")
        print("\t[ReceivingProblemType: Receiving Problem Type]")

    @staticmethod
    def store(inputs):
        # here check if it has all the information
        if inputs == PersonAction.problem_type:
            return True
        return False

    def next(self, inputs, info=None):
        if ReceivingApartment.store(inputs):
            return ChatBot.ReceivingProblemDescription
        print('it did not work, try again something like: " Ap eletrica / Ap Geral /Ambientes comuns "')
        return ChatBot.receiving_problem_type

class ReceivingRoom(State):
    def run(self, first=True):
        if first:
            print("-- Can you tell me in what room is the problem located?")
        print("\t[ReceivingRoom: Receiving Room]")

    @staticmethod
    def store(inputs):
        # here check if it has all the information
        if inputs == PersonAction.problem_room:
            return True
        return False

    def next(self, inputs, info=None):
        if ReceivingRoom.store(inputs):
            return ChatBot.receiving_apartment
        print('it did not work, try again something like: "cozinha"')
        return ChatBot.receiving_room


class ReceivingDescription(State):
    def run(self, first=True):
        if first:
            print("-- Can you brief the problem?")
        print("\t[Processing: Receiving information]")

    @staticmethod
    def store(inputs):
        # here check if it has all the information
        if inputs == PersonAction.problem_description:
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
        print("\t[Tracking: Order sent, following it]")

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
                print(f'Your order is in position {0} of the list'.format(n))

        return ChatBot.tracking


class ChatBot(StateMachine):
    def __init__(self):
        # Initial state
        StateMachine.__init__(self, ChatBot.waiting)


# Static variable initialization:
ChatBot.waiting = Waiting()
ChatBot.tracking = Tracking()
ChatBot.receiving_room = ReceivingRoom()
ChatBot.receiving_apartment = ReceivingApartment()
ChatBot.receiving_description = ReceivingDescription()
ChatBot.receiving_name = ReceivingName()
ChatBot.receiving_problem_type = ReceivingProblemType()

moves = map(str.strip, open("../statemachine/person/person_moves.txt").readlines())
ChatBot().run_all(map(PersonAction, moves))
print("#" * 76)
moves = map(str.strip, open("../statemachine/person/person_moves2.txt").readlines())
ChatBot().run_all(map(PersonAction, moves))
