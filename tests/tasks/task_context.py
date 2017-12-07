import unittest

class IntentionMap :
    def __init__(self): pass
    def tests(self): return -1

class TaskContext :
    def __init__(self): pass


class TestMethod(unittest.TestCase) :
    def test_dynamic_load(self):

        from pydoc import locate
        my_class = locate('scripts.stt.SpeechRecognizer')
        my_class.recognize()

if __name__ == "__main__" :
    unittest.main()