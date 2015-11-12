
class Event(object):
    id = ''
    name = ''
    description = ''
    creator = ''
    assistants = []

    def __init__(self, id, name, description, creator):
        self.id = id
        self.name = name
        self.description = description
        self.creator = creator
        self.assistants.append(creator)

class User(object):
    id = ''
    name = ''
    lastname = ''
    age = 0

    def __init__(self, id, name, lastname, age):
        self.id = id
        self.name = name
        self.lastname = lastname
        self.age = age
