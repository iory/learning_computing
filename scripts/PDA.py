#!/usr/bin/env python
# -*- coding:utf-8 -*-

from stack import Stack

class PDAConfiguration(object):
    def __init__(self, state, stack):
        self.state = state
        self.stack = stack

class PDARule(object):
    def __init__(self, state, character, next_state,
                 pop_character, push_characters):
        self.state = state
        self.character = character
        self.next_state = next_state
        self.pop_character = pop_character
        self.push_characters = push_characters
    def applies_to(self, configuration, character):
        return self.state == configuration.state and self.pop_character == configuration.stack.top() and self.character == character
    def __str__(self):
        return '''#<struct PDARule
        state={0.state},
        chracter="{0.character}",
        next_state={0.next_state},
        pop_character="{0.pop_character}",
        push_characters={0.push_characters}>'''.format(self)

def main():
    print("==== PDA test ====")
    rule = PDARule(1, '(', 2, '$', ['b', '$'])
    print(rule)

    configuration = PDAConfiguration(1, Stack(['$']))
    print(rule.applies_to(configuration, '('))
if __name__ == "__main__":
    main()
