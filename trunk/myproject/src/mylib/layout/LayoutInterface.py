class LayoutInterface(object):
    def __init__(self):
        raise NotImplementedError
    def getGraph(self):
        raise NotImplementedError
    def getLayoutName(self):
        raise NotImplementedError