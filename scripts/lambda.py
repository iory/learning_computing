#!/usr/bin/env python
# -*- coding:utf-8 -*-

# definition of Numbers
ZERO = lambda f: lambda x: x
ONE  = lambda f: lambda x: f(x)
TWO  = lambda f: lambda x: f(f(x))
THREE= lambda f: lambda x: f(f(f(x)))

to_integer = lambda f: f(lambda x: x + 1)(0)

TRUE = lambda x: lambda y: x
FALSE= lambda x: lambda y: y

# to_boolean = lambda f: f(True)(False)
IF = lambda f: lambda x: lambda y: f(x)(y)
IF = lambda f: f
to_boolean = lambda f: IF(f)(TRUE)(FALSE)

IS_ZERO = lambda n: n(lambda x: FALSE)(TRUE)

def main():
    print(to_integer(ZERO))
    print(to_integer(ONE))
    print(to_integer(TWO))
    print(to_integer(THREE))

    print(to_boolean(TRUE))
    print(to_boolean(FALSE))

    print(IF(TRUE)("happy")("sad"))
    print(IF(FALSE)("happy")("sad"))

    print(to_boolean(IS_ZERO(ZERO)))

if __name__ == "__main__":
    main()
