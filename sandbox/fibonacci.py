#!/usr/bin/env python
# -*- coding:utf-8 -*-

# oneliner: fibonacci
def main():
    print('fibonacci number')
    fibo = lambda n: reduce(lambda x, i: x + [x[i] + x[i+1]], range(n-2), [1, 1])
    for i in range(2, 10):
        print(fibo(i))

if __name__ == "__main__":
    main()
