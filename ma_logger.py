'''
Logger for debugging info on server functionality
'''
import datetime
import io

class Singleton(object):
  _instance = None
  def __new__(class_, *args, **kwargs):
    if not isinstance(class_._instance, class_):
        class_._instance = object.__new__(class_, *args, **kwargs)
    return class_._instance

class Logger(Singleton):
    mode = ""
    action_history = []

    # change modes
    def __init__(self, mode="DEFAULT"):
        self.mode = mode

    # registers an action to action history
    def registerNewAction(self, action):
        current_time = datetime.datetime.now().strftime("%I:%M%p - %B %d, %Y")
        self.action_history.append("[" + current_time + "]" + " New action on server: " + action)

    # Must be called at the end of action registration to write all files to memory
    def log(self):
        with io.open('meetapp.logs', 'a') as file:
            for action in self.action_history:
                file.write(unicode(action + "\n"))
