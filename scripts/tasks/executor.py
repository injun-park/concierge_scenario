import transition

class Executor :
    def __init__(self): pass
    def loop(self):
        t = transition.Transition()
        shutdown = False
        while shutdown is not True :
            task = t.getTask()
            task.execute()

