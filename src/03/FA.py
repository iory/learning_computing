#!/usr/bin/env python
# -*- coding:utf-8 -*-

class FARule(object):
    def __init__(self, state, character, next_state):
        self.state = state
        self.character = character
        self.next_state = next_state
    def follow(self):
        return self.next_state
    def applies_to(self, state, character):
        return self.state == state and self.character == character

class DFARulebook(object):
    def __init__(self, rules):
        self.rules = rules
    def next_state(self, state, character):
        return self.rule_for(state, character).follow()
    def rule_for(self, state, character):
        # bad code
        for rule in self.rules:
            if rule.applies_to(state, character):
                return rule

class DFA(object):
    def __init__(self, current_state, accept_states, rulebook):
        self.current_state = current_state
        self.accept_states = accept_states
        self.rulebook = rulebook
    def accepting(self):
        return self.current_state in self.accept_states
    def read_character(self, character):
        self.current_state = self.rulebook.next_state(self.current_state, character)
    def read_string(self, string):
        for s in string:
            self.read_character(s)

class DFADesign(object):
    def __init__(self, start_state, accept_states, rulebook):
        self.start_state = start_state
        self.accept_states = accept_states
        self.rulebook = rulebook
    def to_dfa(self):
        return DFA(self.start_state, self.accept_states, self.rulebook)
    def accept(self, string):
        dfa = self.to_dfa()
        dfa.read_string(string)
        return dfa.accepting()

if __name__ == '__main__':
    rulebook = DFARulebook([
        FARule(1, 'a', 2), FARule(1, 'b', 1),
        FARule(2, 'a', 2), FARule(2, 'b', 3),
        FARule(3, 'a', 3), FARule(3, 'b', 3)])
    print(rulebook.next_state(1, 'a'))
    print(rulebook.next_state(1, 'b'))
    print(rulebook.next_state(2, 'b'))

    print(DFA(1, [1, 3], rulebook).accepting())
    print(DFA(1, [3], rulebook).accepting())

    dfa = DFA(1, [3], rulebook)
    print(dfa.accepting())
    dfa.read_string('baaab')
    print(dfa.accepting())

    print("\n==== dfa_design ====")
    dfa_design = DFADesign(1, [3], rulebook)
    print(dfa_design.accept('a'))
    print(dfa_design.accept("baa"))
    print(dfa_design.accept('baba'))
