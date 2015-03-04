#!/usr/bin/env python
# -*- coding:utf-8 -*-

class Number(object):
    def __init__(self, value):
        self.value = value
    def __str__(self):
        return "{}".format(self.value)
    def __add__(self, other):
        return self.value + other.value
    def __mul__(self, other):
        return self.value * other.value
    def reducible(self):
        return False

class Add(object):
    def __init__(self, left, right):
        self.left = left
        self.right = right
    def __str__(self):
        return "{} + {}".format(self.left, self.right)
    def reducible(self):
        return True
    def reduce(self):
        if self.left.reducible():
            return Add(self.left.reduce(), self.right)
        elif self.right.reducible():
            return Add(self.left, self.right.reduce())
        else:
            return Number(self.left + self.right)

class Multiply(object):
    def __init__(self, left, right):
        self.left = left
        self.right = right
    def __str__(self):
        return "{} * {}".format(self.left, self.right)
    def reducible(self):
        return True
    def reduce(self):
        if self.left.reducible():
           return Multiply(self.left.reduce(), self.right)
        elif self.right.reducible():
            return Multiply(self.left, self.right.reduce())
        else:
            return Number(self.left * self.right)

class Boolean(object):
    def __init__(self, value):
        self.value = value
    def __str__(self):
        return "{}".format(self.value)
    def __lt__(self, other):
        return self.left.value < self.right.value
    def __gt__(self, other):
        return self.left.value > self.right.value
    def reducible(self):
        return False

class LessThan(object):
    def __init__(self, left, right):
        self.left = left
        self.right = right
    def __str__(self):
        return "{} < {}".format(self.left, self.right)
    def reducible(self):
        return True
    def reduce(self):
        if self.left.reducible():
            return LessThan(self.left.reduce(), self.right)
        elif self.right.reducible():
            return LessThan(self.left, self.right.reduce())
        else:
            return Boolean(self.left.value < self.right.value)

class Machine(object):
    def __init__(self, expression):
        self.expression = expression
    def step(self):
        self.expression = self.expression.reduce()
    def run(self):
        while self.expression.reducible():
            print(self.expression)
            self.step()
        print(self.expression)

# def reducible(expression):
#     if isinstance(expression, Number):
#         return False
#     elif isinstance(expression, Add) or isinstance(expression, Multiply):
#         return True

print(Add( Multiply( Number(1), Number(2)),
           Multiply( Number(3), Number(4))))

expression = Add( Multiply(Number(1), Number(2)),
                  Multiply(Number(3), Number(4)))

m = Machine(expression)
m.run()

print("Boolean Test")
Machine(LessThan(Number(5), Add(Number(2), Number(2)))).run()
