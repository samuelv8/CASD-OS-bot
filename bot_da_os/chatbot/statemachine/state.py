# A State has an operation, and can be moved
# into the next State given an Input:


class State:
    def run(self, user_id, first=True):
        assert 0, "run not implemented"

    def next(self, user_id, inputs, info=None, original_input=None):
        assert 0, "next not implemented"


class NonInputState:
    def run(self, user_id, first=True):
        assert 0, "run not implemented"

    def next(self, user_id, info=None):
        assert 0, "next not implemented"
