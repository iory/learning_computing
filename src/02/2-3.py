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
    def reduce(self, env):
        if self.left.reducible():
            return Add(self.left.reduce(env), self.right)
        elif self.right.reducible():
            return Add(self.left, self.right.reduce(env))
        else:
            return Number(self.left.value + self.right.value)

class Multiply(object):
    def __init__(self, left, right):
        self.left = left
        self.right = right
    def __str__(self):
        return "{} * {}".format(self.left, self.right)
    def reducible(self):
        return True
    def reduce(self, env):
        if self.left.reducible():
            return Multiply(self.left.reduce(env), self.right)
        elif self.right.reducible():
            return Multiply(self.left, self.right.reduce(env))
        else:
            return Multiply(self.left.value * self.right.value)

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
    def reduce(self, env):
        if self.left.reducible():
            return LessThan(self.left.reduce(env), self.right)
        elif self.right.reducible():
            return LessThan(self.left, self.right.reduce(env))
        else:
            return LessThan(self.left < self.right)

class Variable(object):
    def __init__(self, name):
        self.name = name
    def __str__(self):
        return "{}".format(self.name)
    def reducible(self):
        return True
    def reduce(self, environment):
        return environment[self.name]


class Machine(object):
    def __init__(self, expression, env):
        self.expression = expression
        self.env = env
    def step(self):
        self.expression = self.expression.reduce(self.env)
    def run(self):
        while self.expression.reducible():
            print(self.expression)
            self.step()
        print(self.expression)

if __name__ == "__main__":
    Machine(
        Add(Variable('x'), Variable('y')),
        {'x': Number(3), 'y': Number(4)}).run()
