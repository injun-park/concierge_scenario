import unittest

class State :
    def __init__(self): pass
    def handle(self): pass


class InitState(State) :
    def __init__(self): pass
    def handle(self):
        print "Init"

class WelcomeState(State) :
    def __init__(self): pass
    def handle(self):
        '''
        speak welcome speech
        send welcome ui

        read google voice
        read aibril response

        return aibril_response
        '''

        pass

class ChoolseLocationState(State):
    def __init__(self): pass
    def handle(self):
        '''
        send helping sentence to UI
        speak above sentence

        read google voice
        send google voice to aibril and receive result
        :return: above result
        '''
        pass

class InformLocationState(State) :
    def __init__(self): pass
    def handle(self):
        '''

        :return:
        '''
        pass

class ShutdownState(State) :
    def __init__(self): pass
    def handle(self):


        pass

class Transition :
    def __init__(self):
        self.oldState = None
        self.currentState = WelcomeState()

    def calculateNewState(self, **kwargs):
        ui_msg = aibrilResponse = None
        try :
            ui_msg = kwargs['ui_msg']
            aibrilResponse = kwargs['aibrilResponse']

        except KeyError as e :
            pass

        if ui_msg is not None : pass
        elif aibrilResponse is not None :
            '''
            extract intent
            extract entities
            '''
            pass

class TestFunction(unittest.TestCase) :
    def test_a(self):
        transition = Transition()
        initState = transition.calculateNewState()
        shutdown = False
        while shutdown is not True :
            state = transition.calculateNewState()

if __name__ == '__main__':
    unittest.main()