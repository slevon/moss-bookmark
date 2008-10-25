class JeremyQueue(list):
    __slots__ = ('back',)
    def __init__(self):
        self.back = []
    def enqueue(self, elt):
        self.back.append(elt)
    def dequeue(self):
        if self:
            return self.pop()
        else:
            self.back.reverse()
            self[:] = self.back
            self.back = []
            return self.pop()