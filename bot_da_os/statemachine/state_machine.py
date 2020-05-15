# Takes a list of Inputs to move from State to
# State using a template method.
from .person.interpreter.interpreter import person_interpreter


class StateMachine:
    def __init__(self, initial_state):
        self.current_state = initial_state
        self.current_state.run()

    # Template method:
    def run_all(self, inputs):
        for i in inputs:
            print(i)
            t, info = person_interpreter(i)  # 't' is the type, 'info' is useful information (can be None)
            first = True
            new = self.current_state.next(t, info)
            if new == self.current_state:
                first = False
            self.current_state = new
            self.current_state.run(first)
