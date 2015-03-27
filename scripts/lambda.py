#!/usr/bin/env python
# -*- coding:utf-8 -*-

# definition of Numbers
ZERO = lambda f: lambda x: x
ONE  = lambda f: lambda x: f(x)
TWO  = lambda f: lambda x: f(f(x))
THREE= lambda f: lambda x: f(f(f(x)))

to_integer = lambda f: f(lambda x: x + 1)(0)

def main():
    print(to_integer(ZERO))
    print(to_integer(ONE))
    print(to_integer(TWO))
    print(to_integer(THREE))

if __name__ == "__main__":
    main()
