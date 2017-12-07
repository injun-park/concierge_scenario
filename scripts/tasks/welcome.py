import task
import TTS

class Welcome(task.Task) :
    def __init__(self): pass
    def execute(self, intent, entities, params):
        tts = TTS.TTS()
        tts.speak()

