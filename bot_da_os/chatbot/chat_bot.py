from bot_da_os.statemachine.person.person_action import PersonAction
from bot_da_os.statemachine.state import State, NonInputState
from bot_da_os.statemachine.state_machine import StateMachine
from random import randint
import sys

sys.path += ['../statemachine', '../person']

# NOTES:
# -need to actually store the information obtained in interpreter


class Waiting(State):
    def run(self, first=True):
        print("\t[Waiting: Waiting for request]")

    def next(self, inputs, info=None):
        if inputs == PersonAction.request:
            return ChatBot.receiving_name
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
        print('-- It did not work, try again something like: "Fulano Silva"')
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
        print('-- It did not work, try again something like: "222 D"')
        return ChatBot.receiving_apartment


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
            return ChatBot.receiving_problem_type
        print('-- It did not work, try again something like: "Cozinha"')
        return ChatBot.receiving_room


class ReceivingProblemType(State):  # we could skip this state -- samuel
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
        if ReceivingProblemType.store(inputs):
            return ChatBot.receiving_description
        print('-- It did not work, try again something like: " Ap eletrica / Ap Geral /Ambientes comuns "')
        return ChatBot.receiving_problem_type


class ReceivingDescription(State):
    def run(self, first=True):
        if first:
            print("-- Can you brief the problem?")
        print("\t[Receiving Description: Receiving description]")

    @staticmethod
    def store(inputs):
        # here check if it has all the information
        if inputs == PersonAction.problem_description:
            return True
        return False

    def next(self, inputs, info=None):
        if ReceivingDescription.store(inputs):
            return ChatBot.tracking
        return ChatBot.receiving_description


class Tracking(State):
    def run(self, first=True):
        if first:
            print("-- Okay, your request was recorded. If you want to know about it's status, tell me! ;)")
        print("\t[Tracking: Order sent, following it]")

    def next(self, inputs, info=None):
        if inputs == PersonAction.status or inputs == PersonAction.angry:
            return ChatBot.verifying
        return ChatBot.tracking


class Verifying(NonInputState):
    def run(self, first=True):
        print("\t[Verifying: Checking the database]")

    @staticmethod
    def status():
        # here communicates with the db
        n = randint(0, 1)
        return n

    def next(self, info=None):
        n = Verifying.status()
        if n <= 0:
            print("-- Your order is done!")
            return ChatBot.finishing
        else:
            print(f'Your order is in position {n} of the list')
            return ChatBot.tracking


class Finishing(NonInputState):
    def run(self, first=True):
        print("-- Could you fill out this form to give us a feedback? <link>")
        print("\t[Finishing: service done, requesting feedback]")

    def next(self, info=None):
        return ChatBot.waiting


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
ChatBot.verifying = Verifying()
ChatBot.finishing = Finishing()

moves = map(str.strip, open("../statemachine/person/person_moves.txt").readlines())
ChatBot().run_all(map(PersonAction, moves))
# print("#" * 76)
# moves = map(str.strip, open("../statemachine/person/person_moves2.txt").readlines())
# ChatBot().run_all(map(PersonAction, moves))
