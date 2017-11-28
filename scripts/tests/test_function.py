import unittest

class TestFunction(unittest.TestCase) :
    def test_uppper(self):
        self.assertEqual('foo'.upper(), 'FOO')


    def test_lambda(self):
        function = lambda x, y : (x + y)

    def callback_test(self):
        def function(arg) :
            print arg
        f = lambda : function("abc")
        f()
