# A State has an operation, and can be moved
# into the next State given an Input:


class State:
    def run(self, first=True):
        assert 0, "run not implemented"

    def next(self, inputs, info=None):
        assert 0, "next not implemented"


class NonInputState:
    def run(self, first=True):
        assert 0, "run not implemented"

    def next(self, info=None):
        assert 0, "next not implemented"
