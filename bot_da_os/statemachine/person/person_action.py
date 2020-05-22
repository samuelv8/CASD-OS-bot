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
PersonAction.name = PersonAction("person tells his/her name")
PersonAction.apartment = PersonAction("person tells his/her apartment and spot")
PersonAction.problem_type = PersonAction("person classifies his/her problem")
PersonAction.problem_room = PersonAction("person tells problem room")
PersonAction.problem_description = PersonAction("person describes his/her problem")
PersonAction.status = PersonAction("person wants to know the status of his/her order")
PersonAction.feedback = PersonAction("person gives his/her feedback")
PersonAction.thanks = PersonAction("person thanks")
PersonAction.angry = PersonAction("person is pissed off")
PersonAction.undefined = PersonAction("person does something else")
