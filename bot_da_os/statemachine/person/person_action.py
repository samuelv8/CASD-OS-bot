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
PersonAction.greet = PersonAction("greet")
PersonAction.request = PersonAction("request")
PersonAction.name = PersonAction("name")
PersonAction.apartment = PersonAction("apartment")
PersonAction.problem_type = PersonAction("ptype")
PersonAction.problem_room = PersonAction("proom")
PersonAction.problem_description = PersonAction("pdescr")
PersonAction.status = PersonAction("status")
PersonAction.feedback = PersonAction("feedback")
PersonAction.thanks = PersonAction("thanks")
PersonAction.angry = PersonAction("angry")
PersonAction.unknown = PersonAction("unknown")
