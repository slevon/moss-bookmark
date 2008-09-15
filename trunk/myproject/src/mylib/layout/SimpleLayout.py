from LayoutInterface import LayoutInterface
class SimpleLayout(LayoutInterface):
    def __init__(self):
        print "Hell"
    def getGraph(self):
        pass
    def getLayoutName(self):
        pass
if __name__ == "__main__":
    a = SimpleLayout()
    print type(a)
    print isinstance(a, LayoutInterface)