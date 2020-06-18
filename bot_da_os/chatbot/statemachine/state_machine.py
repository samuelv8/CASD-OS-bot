# Takes a list of Inputs to move from State to
# State using a template method.
from .person.interpreter.interpreter import person_interpreter
from .person.person_action import PersonAction
from .state import NonInputState


class StateMachine:
    def __init__(self, initial_state):
        self.current_state = initial_state
        self.current_state.run()

    def run_all(self):
        while True:
            i = PersonAction(input())
            s = self.current_state.__class__.__name__
            t, info = person_interpreter(i, s)  # 't' is the type, 'info' is useful information (can ben None)
            first = True
            new = self.current_state.next(t, info)
            if new == self.current_state:
                first = False
            self.current_state = new
            self.current_state.run(first)
            while issubclass(self.current_state.__class__, NonInputState):  # runs the loop again without inputs
                self.current_state = self.current_state.next()
                self.current_state.run(False)
