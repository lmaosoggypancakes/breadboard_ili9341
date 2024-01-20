from ili9341 import color565

class Pos(object):
    def __init__(self, x, y):
        self.x = x
        self.y = y

class Color(object):
    def __init__(self, r, g, b):
        self.r = r
        self.g = g
        self.b = b
        self.color565 = color565(self.r, self.g, self.b)
        
    def to_color565(self):
        return self.color565
    
    def darker(self):
        return Color(int(self.r * 0.5), int(self.g * 0.5), int(self.b * 0.5))
