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
PersonAction.status = PersonAction("person wants to know the status of his/her order")
PersonAction.name = PersonAction("person tells his/her name")
PersonAction.apartment = PersonAction("person tells his/her apartment number")
PersonAction.spot = PersonAction("person tells his/her spot letter")
PersonAction.problem_type = PersonAction("person classifies his/her problem")
PersonAction.problem_description = PersonAction("person describes his/her problem")
PersonAction.feedback = PersonAction("person gives his/her feedback")
PersonAction.angry = PersonAction("person is pissed off")
PersonAction.undefined = PersonAction("person does something else")
