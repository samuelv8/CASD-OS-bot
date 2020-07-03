from bot_da_os.chatbot.statemachine.person.interpreter.interpreter import person_interpreter
from bot_da_os.chatbot.statemachine.person.person_action import PersonAction
from bot_da_os.chatbot.statemachine.state import State, NonInputState
from bot_da_os.chatbot.statemachine.state_machine import StateMachine
from bot_da_os.storage.storage import *
from random import randint
# import sys

# TODO:
# -need to actually store the information obtained in interpreter
# -need to implement save_synonym


class Waiting(State):
    def run(self, user_id, first=True):
        print("\t[Waiting: Waiting for request]")

    def next(self, user_id, inputs, info=None, original_input=None):
        if inputs == PersonAction.request:
            return ChatBot.receiving_name
        elif inputs == PersonAction.greet or inputs == PersonAction.angry:
            print("-- Oi! Como posso ajudar você?")
        elif inputs == PersonAction.thanks:
            print("-- De nada! #ocasdnaopara")
        elif inputs == PersonAction.unknown:
            print("-- Olá! Gostaria de solicitar um serviço?")
        return ChatBot.waiting


class ReceivingName(State):
    def run(self, user_id, first=True):
        if first:
            print("-- Pode me dizer o seu nome e sobrenome?")
        print("\t[ReceivingName: Receiving name]")

    @staticmethod
    def store(user_id, info):
        # here check if it has all the information
        connect = create_connection('db_orders.db')
        copia = next(info) + ' ' + next(info)
        save_name(copia, int(user_id), connect)
        connect.close()

    def next(self, user_id, inputs, info=None, original_input=None):
        if inputs == PersonAction.name:
            ReceivingName.store(user_id, info)
            return ChatBot.receiving_apartment
        print('-- Não entendi. Tente de novo algo do tipo: "Fulano Silva"')
        return ChatBot.receiving_name


class ReceivingApartment(State):
    def run(self, user_id, first=True):
        if first:
            print("-- Pode me passar qual seu apartamento e sua vaga?")
        print("\t[ReceivingApartment: Receiving Apartment]")

    @staticmethod
    def store(user_id, info):
        # here check if it has all the information
        connect = create_connection('db_orders.db')
        save_ap(info[0]+" "+info[1], int(user_id), connect)
        connect.close()
        print(f'## Ap: "{info[0]} {info[1]}" ##')

    def next(self, user_id, inputs, info=None, original_input=None):
        if inputs == PersonAction.apartment:
            ReceivingApartment.store(user_id, info)
            return ChatBot.receiving_room
        print('-- Não entendi. Tente de novo algo do tipo: "222 D"')
        return ChatBot.receiving_apartment


class ReceivingRoom(State):
    def run(self, user_id, first=True):
        if first:
            print("-- Em qual cômodo/ambiente está o problema?")
        print("\t[ReceivingRoom: Receiving Room]")

    @staticmethod
    def store(user_id, info):
        # here check if it has all the information
        connect = create_connection('db_orders.db')
        save_proom(info, int(user_id), connect)
        connect.close()
        print(f'## Cômodo/ambiente: "{info}" ##')

    def next(self, user_id, inputs, info=None, original_input=None):
        if inputs == PersonAction.problem_room:
            if inputs.sure:
                ReceivingRoom.store(user_id, info)
                return ChatBot.receiving_problem_type
            print(f'-- Você quis dizer {info}?')
            t, i = person_interpreter(PersonAction(input()), self.__class__.__name__)
            connect = create_connection('db_orders.db')
            if t == PersonAction.no:
                save_synonym(original_input, info, False, connect)
                connect.close()
            else:
                save_synonym(original_input, info, True, connect)
                connect.close()
                ReceivingRoom.store(user_id, info)
                return ChatBot.receiving_problem_type
        print('-- Não entendi. Tente de novo algo do tipo: "Cozinha" ou "Hall do B"')
        return ChatBot.receiving_room


class ReceivingProblemType(State):
    def run(self, user_id, first=True):
        if first:
            print("-- Qual o tipo do problema?")
        print("\t[ReceivingProblemType: Receiving Problem Type]")

    @staticmethod
    def store(user_id, info):
        # here check if it has all the information
        connect = create_connection('db_orders.db')
        save_ptype(info, int(user_id), connect)
        connect.close()
        print(f'## Tipo: "{info}" ##')

    def next(self, user_id, inputs, info=None, original_input=None):
        if inputs == PersonAction.problem_type:
            if inputs.sure:
                ReceivingProblemType.store(user_id, info)
                return ChatBot.receiving_description
            print(f'-- Você quis dizer {info}?')
            t, i = person_interpreter(PersonAction(input()), self.__class__.__name__)
            connect = create_connection('db_orders.db')
            if t == PersonAction.no:
                save_synonym(original_input, info, False, connect)
                connect.close()
            else:
                save_synonym(original_input, info, False, connect)
                connect.close()
                ReceivingProblemType.store(user_id, info)
                return ChatBot.receiving_description
        print('-- Não entendi. Tente de novo algo do tipo: "Elétrica" ou "Vazamento"')
        return ChatBot.receiving_problem_type


class ReceivingDescription(State):
    def run(self, user_id, first=True):
        if first:
            print("-- Por favor, descreva brevemente o problema.")
        print("\t[Receiving Description: Receiving description]")

    @staticmethod
    def store(user_id, info):
        # here check if it has all the information
        connect = create_connection('db_orders.db')
        save_pdescription(info, int(user_id), connect)
        connect.close()
        print(f'## Descr.: "{info}" ##')

    def next(self, user_id, inputs, info=None, original_input=None):
        if inputs == PersonAction.problem_description:
            ReceivingDescription.store(user_id, info)
            return ChatBot.tracking
        return ChatBot.receiving_description


class Tracking(State):
    def run(self, user_id, first=True):
        if first:
            print("-- Ok, sua ordem foi recebida. Quando quiser saber sobre o andamento dela, me avise! ;)")
        print("\t[Tracking: Order sent, following it]")

    def next(self, user_id, inputs, info=None, original_input=None):
        if inputs == PersonAction.status or inputs == PersonAction.angry:
            return ChatBot.verifying
        return ChatBot.tracking


class Verifying(NonInputState):
    def run(self, user_id, first=True):
        print("\t[Verifying: Checking the database]")

    @staticmethod
    def status():
        # here communicates with the db
        n = randint(0, 2)
        return n

    def next(self, user_id, info=None):
        n = Verifying.status()
        if n <= 0:
            print("-- Serviço pronto!")
            return ChatBot.finishing
        else:
            print(f'Sua ordem está na posição {n} da lista. Em breve estará pronta. :)')
            return ChatBot.tracking


class Finishing(NonInputState):
    def run(self, user_id, first=True):
        print("-- Você pode preencher esse forms rápido para nos dar um feedback? <link>")
        print("\t[Finishing: service done, requesting feedback]")

    def next(self, user_id, info=None):
        return ChatBot.waiting


class ChatBot(StateMachine):
    def __init__(self, user_id):
        # Initial state
        StateMachine.__init__(self, user_id, ChatBot.waiting)


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
