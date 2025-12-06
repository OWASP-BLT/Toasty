class Add:
    def __init__(self, c):
        self.c = c
    def forward(self, a, b):
        c = a+b
        return c

class test:
    def __init__(self):
        self.add = Add(0)
    def forward(self, a, b):
        c = self.add.forward(a, b)
        return c

t = test()
print(t.forward(10, 12))