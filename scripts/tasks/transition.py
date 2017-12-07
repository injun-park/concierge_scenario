import reflection
import welcome
import shutdown
import guide

class Transition :
    def __init__(self):
        self.oldTask = self.curTask = welcome.Welcome()
        self.model = {}

    def setCondition(self, name, value):
        pass
    def getTask(self):
        self.oldTask = self.currentTask

