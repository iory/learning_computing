#!/usr/bin/env python
# -*- coding:utf-8 -*-

from NFA import *

class Pattern(object):
    def __init__(self):
        super(Pattern, self).__init__()
    def matches(self, string):
        return self.to_nfa_design().accept(string)

class Empty(Pattern):
    def __init__(self):
        super(Empty, self).__init__()
    def to_nfa_design(self):
        start_state = object()
        accept_state = [start_state]
        rulebook = NFARulebook([])
        return NFADesign(start_state, set(accept_state), rulebook)

class Literal(Pattern):
    def __init__(self, character):
        super(Literal, self).__init__()
        self.character = character
    def to_nfa_design(self):
        start_state = object()
        accept_state = object()
        rule = FARule(start_state, self.character, accept_state)
        rulebook = NFARulebook([rule])

        return NFADesign(start_state, set([accept_state]), rulebook)

class Concatenate(Pattern):
    def __init__(self, first, second):
        self.first = first
        self.second = second
    def to_nfa_design(self):
        first_nfa_design = self.first.to_nfa_design()
        second_nfa_design = self.second.to_nfa_design()

        start_state = first_nfa_design.start_state
        accept_states = second_nfa_design.accept_states
        rules = first_nfa_design.rulebook.rules + second_nfa_design.rulebook.rules
        extra_rules = map(lambda state: FARule(state, None, second_nfa_design.start_state),
                          first_nfa_design.accept_states)

        rulebook = NFARulebook(rules + extra_rules)
        return NFADesign(start_state, accept_states, rulebook)

class Choose(Pattern):
    def __init__(self, first, second):
        self.first = first
        self.second = second
    def to_nfa_design(self):
        first_nfa_design = self.first.to_nfa_design()
        second_nfa_design = self.second.to_nfa_design()

        start_state = object()
        accept_states = first_nfa_design.accept_states.union(second_nfa_design.accept_states)
        # print(self.first, self.second)
        # print(first_nfa_design.rulebook.rules, second_nfa_design.rulebook.rules)
        rules = first_nfa_design.rulebook.rules + second_nfa_design.rulebook.rules
        extra_rules = map(lambda nfa_design: FARule(start_state, None, nfa_design.start_state),
                          [first_nfa_design, second_nfa_design])
        rulebook = NFARulebook(rules + extra_rules)
        return NFADesign(start_state, accept_states, rulebook)

class Repeat(Pattern):
    def __init__(self, pattern):
        self.pattern = pattern
    def to_nfa_design(self):
        pattern_nfa_design = self.pattern.to_nfa_design()

        start_state = object()
        accept_states = pattern_nfa_design.accept_states.union(set([start_state]))
        rules = pattern_nfa_design.rulebook.rules
        extra_rules = map(lambda accept_state:
                          FARule(accept_state, None, pattern_nfa_design.start_state),
                          pattern_nfa_design.accept_states)
        extra_rules += [FARule(start_state, None, pattern_nfa_design.start_state)]
        rulebook = NFARulebook(rules + extra_rules)
        return NFADesign(start_state, accept_states, rulebook)

def main():
    nfa_design = Empty().to_nfa_design()
    print(nfa_design.accept("") == True)
    print(nfa_design.accept('a') == False)
    print(nfa_design.accept('b') == False)

    nfa_design = Literal('a').to_nfa_design()
    print(nfa_design.accept('') == False)
    print(nfa_design.accept('a') == True)
    print(nfa_design.accept('b') == False)

    print("\n==== Pattern module test ====")
    print(Empty().matches('a') == False)
    print(Literal('a').matches('a') == True)

    print("\n==== concatenate test ====")
    pattern = Concatenate(Literal('a'), Literal('b'))
    print(pattern.matches('a') == False)
    print(pattern.matches('ab') == True)
    print(pattern.matches('abc') == False)

    pattern = Concatenate(Literal('a'),
                          Concatenate(Literal('b'), Literal('c')))
    print(pattern.matches('a') == False)
    print(pattern.matches('ab') == False)
    print(pattern.matches('abc') == True)

    print("\n==== Chose test ====")
    pattern = Choose(Literal('a'), Literal('b'))
    print(pattern.matches('a') == True)
    print(pattern.matches('b') == True)
    print(pattern.matches('c') == False)

    print("\n==== Repeat test ====")
    pattern = Repeat(Literal('a'))
    print(pattern.matches('a') == True)
    print(pattern.matches('aaaa') == True)
    print(pattern.matches('bbb') == False)

    print("\n==== complex pattern test ====")
    pattern = Repeat(Concatenate(Literal('a'), Choose(Empty(), Literal('b'))))
    import graph_util
    graph_util.make_graph(pattern.to_nfa_design().to_nfa())

    print(pattern.matches('') == True)
    print(pattern.matches('a') == True)
    print(pattern.matches('ab') == True)
    print(pattern.matches('aba') == True)
    print(pattern.matches('abab') == True)
    print(pattern.matches('abaab') == True)
    print(pattern.matches('abba') == False)
if __name__ == "__main__":
    main()
