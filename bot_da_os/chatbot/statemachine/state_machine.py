# Takes a list of Inputs to move from State to
# State using a template method.
from .person.interpreter.interpreter import person_interpreter
from .person.person_action import PersonAction
from .state import NonInputState
import threading


class StateMachine(threading.Thread):
    def __init__(self, user_id, initial_state):
        threading.Thread.__init__(self)
        self.user_id = user_id
        self.current_state = initial_state
        self.current_state.run(user_id)

    def run(self):
        while True:
            try:
                i = PersonAction(input())
            except EOFError:
                print("bye bye")
                break
            s = self.current_state.__class__.__name__
            t, info = person_interpreter(i, s)  # 't' is the type, 'info' is useful information (can ben None)
            first = True
            new = self.current_state.next(self.user_id, t, info)
            if new == self.current_state:
                first = False
            self.current_state = new
            self.current_state.run(self.user_id, first)
            while issubclass(self.current_state.__class__, NonInputState):  # runs the loop again without inputs
                self.current_state = self.current_state.next(self.user_id, )
                self.current_state.run(self.user_id, False)
