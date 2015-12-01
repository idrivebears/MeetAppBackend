#User class as per database requirements
class User(object):
    #id = 0; USER ID IS DECIDED BY THE DATABASE ON INSERTION
    IDLocation = 0;
    name = ''
    last_name = ''
    birthdate = ''
    gender = ''
    facebookId = ''
    is_active = ''
    max_interactions_friends = 0
    max_interactions_places = 0

    def __init__(self, name, last_name, birthdate, gender, facebookId, is_active=True, max_interactions_friends= 1, max_interactions_places=1):
        #self.id = id
        self.name = name
        self.last_name = last_name
        self.birthdate = birthdate
        self.gender = gender
        self.facebookId = facebookId
        self.is_active = is_active
        self.max_interactions_friends = max_interactions_friends
        self.max_interactions_places = max_interactions_places

#Event class as per database requirements
class Event(object):
    IDEvent = ""
    IDPlace = ""
    IDUser = ""
    name = ''
    description = ''
    datetime = ''
    visibility = ''

    def __init__(self, IDEvent = "", IDPlace="", IDUser="", name="", description="", datetime="", visibility=""):
        self.IDEvent = IDEvent
        self.IDPlace = IDPlace
        self.IDUser = IDUser
        self.name = name
        self.description = description
        self.datetime = datetime
        self.visibility = visibility

#Place class as per database requiriments
class Place(object):
    #IDPlace = 0 PLACE ID IS DECIDED BY THE DATABASE ON INSERTION
    IDLocation =0
    IDCategory =0
    name = ''
    description =''

    def __init__(self, IDLocation, IDCategory, name, description):
        #self.IDPlace = IDPlace
        self.IDLocation = IDLocation
        self.IDCategory = IDCategory
        self.name = name
        self.description = description

#location as per database requiriments
class Location(object):
    #IDLocation = 0 LOCATION ID IS DECIDED BY THE SERVER
    latitude = -1.0
    longitude = -1.0

    def __init__(self, latitude, longitude):
        #IDLocation = IDLocation
        latitude = latitude
        longitude = longitude

#Comment as per database requiriments
class Comment(object):
    #IDComment = 0 COMENT ID IS DEFINED BY THE SERVER
    IDEvent = 0
    IDUserCreator = 0
    creation_date = ''
    comment_text = ''

    def __init__(self, IDEvent, IDUserCreator, creation_date, comment_text):
        #IDComment = IDComment
        IDEvent = IDEvent
        IDUserCreator = IDUserCreator
        creation_date = creation_date
        comment_text = comment_text

#Category as per database requirements
class Category(object):
    #IDCategory = 0 CATEGORY ID IS DECIDED BY THE DATABASE
    Name = ''

    def __init__(self, Name):
        #IDCategory = IDCategory
        Name = Name

class Recommendation(object):
    IDEvent = 0
    IDUser = 0
    Weight = 0
    def __init__(self, IDEvent, IDUser, Weight):
        self.IDEvent = IDEvent
        self.IDUser = IDUser
        self.Weight = Weight
