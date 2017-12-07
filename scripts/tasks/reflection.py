from pydoc import locate
class Reflection :
    def __init__(self): pass
    
    @staticmethod
    def forName(modulepath):
        obj = locate(modulepath)
        return obj
