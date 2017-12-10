import unittest
from jinja2 import  Environment, PackageLoader, select_autoescape, FileSystemLoader

class TestStringMethods(unittest.TestCase):
    def test_value(self):
        import os
        path, filename = os.path.split("./test1.html")
        env = Environment(
            loader=FileSystemLoader(path),
            autoescape=select_autoescape(['html', 'xml'])
        )

        context = {
            'user' : 'peek'
        }

        template = env.get_template(filename)
        merged = template.render(context)

        print merged

    def test_object(self):

        import os
        path, filename = os.path.split("./robot_div.html")
        env = Environment(
            loader=FileSystemLoader(path),
            autoescape=select_autoescape(['html', 'xml'])
        )

        class User :
            def __init__(self, age, name):
                self.age = age
                self.name = name

        users = [
            User(1, 'first'),
            User(2, 'second'),
            User(3, 'third'),
            User(4, 'fourth')
        ]

        context = {
            'my_string' : 'this is my string',
            'my_intent' : 'my_intent',
            'users' : users
        }

        template = env.get_template(filename)
        print template.render(context)


    def test_array(self):
        a = [1, 2, 3]
        if 1 in a : self.assertTrue(True)
        else : self.assertTrue(False)

        a = ['a', 'abc', 'def']
        if 'abc' in a :
            self.assertTrue(True)

        if 'adbdefg' in a :
            self.assertTrue(False)

if __name__ == '__main__':
    unittest.main()