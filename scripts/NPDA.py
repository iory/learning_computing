#!/usr/bin/env python
# -*- coding:utf-8 -*-

from PDA import *
from stack import *

class NPDARulebook(object):
    def __init__(self, rules):
        self.rules = rules
    def next_configurations(self, configurations, character):
        next_conf = []
        for configuration in configurations:
            if isinstance(configuration, list):
                next_conf += self.next_configurations(configuration, character)
            else:
                next_conf += self.follow_rules_for(configuration, character)
        return set(next_conf)
    def follow_rules_for(self, configuration, character):
        return map(lambda rule: rule.follow(configuration), self.rules_for(configuration, character))
    def rules_for(self, configuration, character):
        return [r for r in self.rules if r.applies_to(configuration, character)]

    def follow_free_moves(self, configations):
        more_configurations = self.next_configurations(configurations, None)
        if more_configurations.issubset(configurations):
            return configurations
        else:
            return self.follow_free_moves(configurations + more_configurations)

class NPDA(object):
    def __init__(self, current_configurations, accept_states, rulebook):
        self.current_configurations = current_configurations
        self.accept_states = accept_states
        self.rulebook = rulebook
    def accepting(self):
        return any([config.state in self.accept_states for config in self.current_configurations])
    def read_character(self, character):
        self.current_configurations = self.rulebook.next_configurations(self.current_configurations, character)
        self.update_current_configuration()
    def read_string(self, string):
        for char in string:
            self.read_character(char)
    def update_current_configuration(self):
        self.current_configurations = self.rulebook.follow_free_moves(self.current_configurations)

def main():
    print("==== NPDA test ====")
    rulebook = NPDARulebook([
        PDARule(1, 'a', 1, '$', ['a', '$']),
        PDARule(1, 'a', 1, 'a', ['a', 'a']),
        PDARule(1, 'a', 1, 'b', ['a', 'b']),
        PDARule(1, 'b', 1, '$', ['b', '$']),
        PDARule(1, 'b', 1, 'a', ['b', 'a']),
        PDARule(1, 'b', 1, 'b', ['b', 'b']),
        PDARule(1, None, 2, '$', ['$']),
        PDARule(1, None, 2, 'a', ['a']),
        PDARule(1, None, 2, 'b', ['b']),
        PDARule(2, 'a', 2, 'a', []),
        PDARule(2, 'b', 2, 'b', []),
        PDARule(2, None, 3, '$', ['$'])
    ])

    configuration = PDAConfiguration(1, Stack(['$']))
    npda = NPDA(set([configuration]), set([3]), rulebook)
    print(npda.accepting())



if __name__ == "__main__":
    main()
