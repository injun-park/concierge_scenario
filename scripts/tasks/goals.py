
class Goal :
    def __init__(self, **kwargs):
        self.kwargs = kwargs

        self.name = self.getKeyValue('name')
        self.intent = self.getKeyValue('intent')
        self.entities = self.getKeyValue('entity')
        self.parameters = self.getKeyValue('parameters')

    def getKeyValue(self, keyname):
        value = ''
        try :
            value = self.kwargs[keyname]
        except KeyError as e :
            value = ''

        return value

class Goals :
    def __init__(self):
        self.goalTaskMap = {}
