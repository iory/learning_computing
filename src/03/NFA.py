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

class NFARulebook(object):
    def __init__(self, rules):
        self.rules = rules
    def next_states(self, states, character):
        ret = []
        for state in states:
            if isinstance(state, list):
                ret += self.next_states(state, character)
            else:
                ret += self.follow_rules_for(state, character)
        return set(ret)

    def follow_rules_for(self, state, character):
        return map(lambda x: x.follow(), self.rules_for(state, character))
    def rules_for(self, state, character):
        return [r for r in self.rules if r.applies_to(state, character)]

class NFA(object):
    def __init__(self, current_states, accept_states, rulebook):
        self.current_states = current_states
        self.accept_states = accept_states
        self.rulebook = rulebook
    def accepting(self):
        return any(self.current_states & self.accept_states)
    def read_character(self, character):
        self.current_states = self.rulebook.next_states(self.current_states, character)
    def read_string(self, string):
        for s in string:
            self.read_character(s)

def main():
    rulebook = NFARulebook([
        FARule(1, 'a', 1), FARule(1, 'b', 1), FARule(1, 'b', 2),
        FARule(2, 'a', 3), FARule(2, 'b', 3),
        FARule(3, 'a', 4), FARule(3, 'b', 4)])
    print(rulebook.next_states(set([1]), 'b'))
    print(rulebook.next_states(set([1, 2]), 'a'))
    print(rulebook.next_states(set([1, 3]), 'b'))

    print("\n==== NFA ====")
    print(NFA(set([1]), set([4]), rulebook).accepting())
    print(NFA(set([1, 2, 4]), set([4]), rulebook).accepting())

    nfa = NFA(set([1]), set([4]), rulebook)
    print(nfa.accepting())
    nfa.read_character('b')
    print(nfa.accepting())
    nfa.read_character('a')
    print(nfa.accepting())
    nfa.read_character('b')
    nfa = NFA(set([1]), set([4]), rulebook)
    print(nfa.accepting())
    nfa.read_string('bbbbb')
    print(nfa.accepting())

if __name__ == "__main__":
    main()
