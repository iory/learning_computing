#!/usr/bin/env python
# -*- coding:utf-8 -*-

class Stack(object):
    def __init__(self, contents):
        self.contents = contents
    def __str__(self):
        return "#<Stack ({}){}>".format(self.top(), ''.join(self.drop(1)))
    def __eq__(self, other):
        return self.contents == other.contents
    def __ne__(self, other):
        return not self.__eq__(other)
    def __hash__(self):
        return sum(map(hash, self.contents))
    def push(self, character):
        self.contents.insert(0, character)
        return self
    def pop(self):
        self.contents = self.drop(1)
        return self
    def top(self):
        return self.contents[0]
    def drop(self, n):
        return self.contents[n:]

def main():
    print("==== Stack test ====")
    stack  = Stack(['a', 'b', 'c', 'd', 'e'])
    print(stack.top())
    stack.pop()
    stack.pop()
    print(stack.top())
    stack.push('x')
    stack.push('y')
    print(stack.top())
    stack.push('x')
    stack.push('y')
    stack.pop()
    print(stack.top())
    print(stack)

    copy_stack = Stack(['x', 'y', 'x', 'c', 'd', 'e'])
    print(copy_stack)
    print(stack == copy_stack)

if __name__ == "__main__":
    main()
