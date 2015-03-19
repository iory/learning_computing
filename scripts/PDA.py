#!/usr/bin/env python
# -*- coding:utf-8 -*-

from stack import Stack
import copy

class PDAConfiguration(object):
    def __init__(self, state, stack):
        self.state = state
        self.stack = stack
    def __str__(self):
        return '#<struct {0.__class__.__name__} state={0.state}, stack={0.stack}>'.format(self)
    def __repr__(self):
        return self.__str__()

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
        return '''#<struct {0.__class__.__name__}
        state={0.state},
        chracter="{0.character}",
        next_state={0.next_state},
        pop_character="{0.pop_character}",
        push_characters={0.push_characters}>'''.format(self)
    def __repr__(self):
        return self.__str__()

    def follow(self, configuration):
        return PDAConfiguration(self.next_state, self.next_stack(copy.deepcopy(configuration)))
    def next_stack(self, configuration):
        popped_stack = configuration.stack.pop()

        # for character in reversed(self.push_characters):
        #     popped_stack.push(character)
        # return popped_stack

        # following code means comment outed code above
        return reduce(lambda popped_stack, character: popped_stack.push(character), reversed(self.push_characters), popped_stack)

class DPDARulebook(object):
    def __init__(self, rules):
        self.rules = rules
    def __str__(self):
        return "#<struct {0.__class__.__name__}, rules={0.rules}".format(self)
    def next_configuration(self, configuration, character):
        return self.rule_for(configuration, character).follow(configuration)
    def rule_for(self, configuration, character):
        for rule in self.rules:
            if rule.applies_to(configuration, character):
                return rule
        return None
    def applies_to(self, configuration, character):
        return not self.rule_for(configuration, character) == None
    def follow_free_moves(self, configuration):
        if self.applies_to(configuration, None):
            return self.follow_free_moves(self.next_configuration(configuration, None))
        else:
            return configuration

class DPDA(object):
    def __init__(self, current_configuration, accept_states, rulebook):
        self.current_configuration = current_configuration
        self.accept_states = accept_states
        self.rulebook = rulebook
    def accepting(self):
        print(self.current_configuration.state, self.accept_states)
        return self.current_configuration.state in self.accept_states
    def read_character(self, character):
        self.current_configuration = self.rulebook.next_configuration(self.current_configuration, character)
        self.update()
    def read_string(self, string):
        for character in string:
            self.read_character(character)
    def update(self):
        self.current_configuration = self.rulebook.follow_free_moves(self.current_configuration)

class DPDADesign(object):
    def __init__(self, start_state, bottom_character, accept_states, rulebook):
        self.start_state = start_state
        self.bottom_character = bottom_character
        self.accept_states = accept_states
        self.rulebook = rulebook
    def accept(self, string):
        dpda = self.to_dpda()
        dpda.read_string(string)
        return dpda.accepting()
    def to_dpda(self):
        start_stack = Stack([self.bottom_character])
        start_configuration = PDAConfiguration(self.start_state, start_stack)
        return DPDA(start_configuration, self.accept_states, self.rulebook)

def main():
    print("==== PDA test ====")
    rule = PDARule(1, '(', 2, '$', ['b', '$'])
    print(rule)

    configuration = PDAConfiguration(1, Stack(['$']))
    print(rule.applies_to(configuration, '('))

    stack = Stack(['$']).push('x').push('y').push('z')
    print(stack)
    stack = stack.pop()
    print(stack)
    stack = stack.pop()
    print(stack)
    print(rule.follow(configuration))

    print("==== DPDA ====")
    rulebook = DPDARulebook([
        PDARule(1, '(', 2, '$', ['b', '$']),
        PDARule(2, '(', 2, 'b', ['b', 'b']),
        PDARule(2, ')', 2, 'b', []),
        PDARule(2, None, 1, '$', ['$'])
    ])
    print(rulebook)
    configuration = rulebook.next_configuration(configuration, '(')
    print(configuration)
    configuration = rulebook.next_configuration(configuration, '(')
    print(configuration)
    configuration = rulebook.next_configuration(configuration, ')')
    print(configuration)

    dpda = DPDA(PDAConfiguration(1, Stack(['$'])), set([1]), rulebook)
    print(dpda.accepting())
    dpda.read_string('(()')
    print(dpda.accepting())
    print(dpda.current_configuration)

    print("=== DPDA free move ====")
    configuration = PDAConfiguration(2, Stack(['$']))
    print(configuration)
    print(rulebook.follow_free_moves(configuration))

    dpda = DPDA(PDAConfiguration(1, Stack(['$'])), set([1]), rulebook)
    dpda.read_string('(()(')
    print(dpda.accepting())
    print(dpda.current_configuration)
    dpda.read_string('))()')
    print(dpda.accepting())
    print(dpda.current_configuration)

    print('==== DPDADesign test ====')
    dpda_design = DPDADesign(1, '$', set([1]), rulebook)
    print(dpda_design.accept('((((((((((()))))))))))'))
    print(dpda_design.accept('((((((((()))))))))()'))

if __name__ == "__main__":
    main()
