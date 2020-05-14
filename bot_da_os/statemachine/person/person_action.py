from operator import eq


class PersonAction:
    def __init__(self, action):
        self.action = action

    def __str__(self): return self.action

    def __eq__(self, other):
        return eq(self.action, other.action)

    # Necessary when __cmp__ or __eq__ is defined
    # in order to make this class usable as a
    # dictionary key:
    def __hash__(self):
        return hash(self.action)


# Static fields; an enumeration of instances:
PersonAction.greet = PersonAction("person greets")
PersonAction.request = PersonAction("person makes a request")
PersonAction.informing = PersonAction("person gives personal information")
PersonAction.briefing = PersonAction("person explains the problem")
PersonAction.query = PersonAction("person wants to know about his/her order")
PersonAction.angry = PersonAction("person is pissed off")
PersonAction.thanks = PersonAction("person thanks")
