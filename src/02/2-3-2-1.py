#!/usr/bin/env python
# -*- coding:utf-8 -*-

class Number(object):
    def __init__(self, value):
        self.value = value
    def __str__(self):
        return "{}".format(self.value)
    def __repr__(self):
        return self.__str__()
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
            return Number(self.left.value * self.right.value)

class Boolean(object):
    def __init__(self, value):
        self.value = value
    def __str__(self):
        return "{}".format(self.value)
    def __repr__(self):
        return self.__str__()
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
            return Boolean(self.left.value < self.right.value)

class Variable(object):
    def __init__(self, name):
        self.name = name
    def __str__(self):
        return "{}".format(self.name)
    def reducible(self):
        return True
    def reduce(self, environment):
        return environment[self.name]


class DoNothing(object):
    def __init__(self):
        print("do-nothing-init")
    def __str__(self):
        return "do-nothing"
    def __eq__(self, other):
        return isinstance(self.other, DoNothing)
    def reducible(self):
        return False

class Assign(object):
    def __init__(self, name, expression):
        self.name = name
        self.expression = expression
    def __str__(self):
        # return "<<{} = {}>>".format(self.name, self.expression)
        return "{0.name} = {0.expression}".format(self)
    def reducible(self):
        return True
    def reduce(self, environment):
        if self.expression.reducible():
            return [Assign(self.name, self.expression.reduce(environment)),
                    environment]
        else:
            environment[self.name] = self.expression
            return [DoNothing(), environment]

class If(object):
    def __init__(self, condition, consequence, alternative):
        self.condition = condition
        self.consequence = consequence
        self.alternative = alternative
    def __str__(self):
        return "if ({}) {{{}}} else {{{}}}".format(self.condition, self.consequence, self.alternative)
    def reducible(self):
        return True
    def reduce(self, env):
        # print(self.__class__.__name__)
        if self.condition.reducible():
            return [If(self.condition.reduce(env), self.consequence, self.alternative), env]
        else:
            if self.condition.value:
                return [self.consequence, env]
            else:
                return [self.alternative, env]

class Sequence(object):
    def __init__(self, first, second):
        self.first = first
        self.second = second
    def __str__(self):
        return "{}, {}".format(self.first, self.second)
    def reducible(self):
        return True
    def reduce(self, env):
        if isinstance(self.first, DoNothing):
            return [self.second, env]
        else:
            reduced_first, reduced_env = self.first.reduce(env)
            return Sequence(reduced_first, self.second), reduced_env

class While(object):
    def __init__(self, condition, body):
        self.condition = condition
        self.body = body
    def __str__(self):
        return "while ({}) {{{}}}".format(self.condition, self.body)
    def reducible(self):
        return True
    def reduce(self, env):
        print(self.__class__.__name__)
        return [If(self.condition, Sequence(self.body, While(self.condition, self.body)), DoNothing()), env]

class Machine(object):
    def __init__(self, statement, env):
        self.statement = statement
        self.env = env
    def step(self):
        self.statement, self.env = self.statement.reduce(self.env)
    def run(self):
        while self.statement.reducible():
            print("{}, {}".format(self.statement, self.env))
            self.step()
        print("{}, {}".format(self.statement, self.env))

if __name__ == "__main__":
    # statement = Assign('x', Add(Variable('x'), Number(1)))
    # print(statement)
    # environment = {'x': Number(2)}
    # print(statement.reducible())
    # statement, environment = statement.reduce(environment)
    # statement, environment = statement.reduce(environment)
    # statement, environment = statement.reduce(environment)
    # print(statement.reducible())

    Machine(Assign('x', Add(Variable('x'), Number(1))),
            {'x': Number(2)}).run()

    print("\n==== if ====")
    Machine(If(Variable('x'),
               Assign('y', Number(1)),
               Assign('y', Number(2))),
               {'x': Boolean(True)}).run()

    print("\n==== sequence ====")
    Machine(Sequence(
        Assign('x', Add(Number(1), Number(1))),
        Assign('y', Add(Variable('x'), Number(3)))),
            {}).run()

    print("\n==== while ====")
    Machine(While(LessThan(Variable('x'), Number(5)),
                  Assign('x', Multiply(Variable('x'), Number(3)))),
            {'x': Number(1)}).run()
