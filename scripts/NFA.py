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
        ns = []
        for state in states:
            if isinstance(state, list):
                ns += self.next_states(state, character)
            else:
                ns += self.follow_rules_for(state, character)
        return set(ns)

    def follow_rules_for(self, state, character):
        return map(lambda x: x.follow(), self.rules_for(state, character))
    def rules_for(self, state, character):
        return [r for r in self.rules if r.applies_to(state, character)]

    def follow_free_moves(self, states):
        more_states = self.next_states(states, None)

        if more_states.issubset(states):
            return states
        else:
            return self.follow_free_moves(states.union(more_states))

class NFA(object):
    def __init__(self, current_states, accept_states, rulebook):
        self.current_states = current_states
        self.accept_states = accept_states
        self.rulebook = rulebook
    def accepting(self):
        return any(self.current_states & self.accept_states)
    def read_character(self, character):
        self.current_states = self.rulebook.follow_free_moves(self.current_states)
        self.current_states = self.rulebook.next_states(self.current_states, character)
    def read_string(self, string):
        for s in string:
            self.read_character(s)

class NFADesign(object):
    def __init__(self, start_state, accept_states, rulebook):
        self.start_state = start_state
        self.accept_states = accept_states
        self.rulebook = rulebook
    def to_nfa(self):
        return  NFA(set([self.start_state]), self.accept_states, self.rulebook)
    def accept(self, string):
        nfa = self.to_nfa()
        nfa.read_string(string)
        return nfa.accepting()

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
    import graph_util
    graph_util.make_graph(nfa)

    print(nfa.accepting())
    nfa.read_string('bbbbb')
    print(nfa.accepting())

    print("\n==== NFA free moving test =====")
    rulebook = NFARulebook([
        FARule(1, None, 2), FARule(1, None, 4),
        FARule(2, 'a', 3),
        FARule(3, 'a', 2),
        FARule(4, 'a', 5),
        FARule(5, 'a', 6),
        FARule(6, 'a', 4)
    ])
    print(rulebook.next_states(set([1]), None))
    print(rulebook.follow_free_moves(set([1])))

    nfa_design = NFADesign(1, set([2, 4]), rulebook)
    graph_util.make_graph(nfa_design.to_nfa())
    print(nfa_design.accept('aa'))
    print(nfa_design.accept('aaa'))
    print(nfa_design.accept('aaaaa'))
    print(nfa_design.accept('aaaaaa'))


if __name__ == "__main__":
    main()
