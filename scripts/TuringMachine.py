#!/usr/bin/env python
# -*- coding:utf-8 -*-

class Tape(object):
    def __init__(self, left, middle, right, blank):
        self.left = left
        self.middle = middle
        self.right = right
        self.blank = blank
    def __str__(self):
        return "#<Tape {}({}){}>".format("".join(self.left), self.middle, "".join(self.right))
    def write(self, character):
        return Tape(self.left, character, self.right, self.blank)
    def move_head_left(self):
        try:
            return Tape(self.left[0:-1], self.left[-1], [self.middle] + self.right, self.blank)
        except IndexError:
            return Tape(self.left[0:-1], self.blank, [self.middle] + self.right, self.blank)
    def move_head_right(self):
        try:
            return Tape(self.left + [self.middle], self.right[0], self.right[1:], self.blank)
        except IndexError:
            return Tape(self.left + [self.middle], self.blank, [], self.blank)

class TMConfiguration(object):
    def __init__(self, state, tape):
        self.state = state
        self.tape = tape
    def __str__(self):
        return '#<struct {0.__class__.__name__} state={0.state}, tape={0.tape}>'.format(self)
    def __repr__(self):
        return self.__str__()

class TMRule(object):
    def __init__(self, state, character, next_state, write_character, direction):
        self.state = state
        self.character = character
        self.next_state = next_state
        self.write_character = write_character
        self.direction = direction
    def __str__(self):
        return '''#<struct {0.__class__.__name__}
        state={0.state},
        chracter="{0.character}",
        next_state={0.next_state},
        write_character="{0.write_character}",
        direction={0.direction}>'''.format(self)
    def __repr__(self):
        return self.__str__()
    def applies_to(self, configuration):
        return self.state == configuration.state and self.character == configuration.tape.middle
    def follow(self, configuration):
        return TMConfiguration(self.next_state, self.next_tape(configuration))
    def next_tape(self, configuration):
        written_tape = configuration.tape.write(self.write_character)
        if self.direction == 'right':
            return written_tape.move_head_right()
        elif self.direction == 'left':
            return written_tape.move_head_left()
        else:
            raise Exception("direction error")

class DTMRulebook(object):
    def __init__(self, rules):
        self.rules = rules
    def __str__(self):
        return "#<struct {0.__class__.__name__}, rules={0.rules}".format(self)
    def next_configuration(self, configuration):
        next_rule = self.rule_for(configuration)
        if next_rule:
            return next_rule.follow(configuration)
        else:
            return configuration
        # return self.rule_for(configuration).follow(configuration)
    def rule_for(self, configuration):
        for rule in self.rules:
            if rule.applies_to(configuration):
                return rule
        return None
    def applies_to(self, configuration):
        return not self.rule_for(configuration)

class DTM(object):
    def __init__(self, current_configuration, accept_states, rulebook):
        self.current_configuration = current_configuration
        self.accept_states = accept_states
        self.rulebook = rulebook
    def accepting(self):
        return self.current_configuration.state in self.accept_states
    def stuck(self):
        # print(self.rulebook.applies_to(self.current_configuration))
        return not self.accepting() and not self.rulebook.applies_to(self.current_configuration)
    def step(self):
        self.current_configuration = self.rulebook.next_configuration(self.current_configuration)
    def run(self):
        print(self.current_configuration)
        while not self.accepting() and self.stuck():
            print(self.current_configuration)
            self.step()

def main():
    tape = Tape(['1', '0', '1'], '1', [], '_')
    print(tape)

    print(tape.move_head_left().move_head_left().move_head_left())
    print(tape.write('0'))
    print(tape.move_head_right())

    rule = TMRule(1, '0', 2, '1', "right")
    print(rule)

    print(rule.follow(TMConfiguration(1, Tape([], '0', [], '_'))))

    rulebook = DTMRulebook([
        TMRule(1, '0', 2, '1', 'right'),
        TMRule(1, '1', 1, '0', 'left'),
        TMRule(1, '_', 2, '1', 'right'),
        TMRule(2, '0', 2, '0', 'right'),
        TMRule(2, '1', 2, '1', 'right'),
        TMRule(2, '_', 3, '_', 'left')
    ])

    dtm = DTM(TMConfiguration(1, tape), set([3]), rulebook)
    dtm.run()

    tape = Tape(['1', '2', '1'], '1', [], '_')
    dtm = DTM(TMConfiguration(1, tape), set([3]), rulebook)
    dtm.run()
    print(dtm.current_configuration)
    print(dtm.accepting())
    print(dtm.stuck())

    rulebook = DTMRulebook([
        TMRule(1, 'x', 1, 'x', 'right'),
        TMRule(1, 'a', 2, 'x', 'right'),
        TMRule(1, "_", 6, '_', 'left'),

        TMRule(2, 'a', 2, 'a', 'right'),
        TMRule(2, 'x', 2, 'x', 'right'),
        TMRule(2, 'b', 3, 'x', 'right'),

        TMRule(3, 'b', 3, 'b', 'right'),
        TMRule(3, 'x', 3, 'x', 'right'),
        TMRule(3, 'c', 4, 'x', 'right'),

        TMRule(4, 'c', 4, 'c', 'right'),
        TMRule(4, '_', 5, '_', 'left'),

        TMRule(5, 'a', 5, 'a', 'left'),
        TMRule(5, 'b', 5, 'b', 'left'),
        TMRule(5, 'c', 5, 'c', 'left'),
        TMRule(5, 'x', 5, 'x', 'left'),
        TMRule(5, '_', 1, '_', 'right')
    ])

    tape = Tape([], 'a', ['a', 'a', 'b', 'b', 'b', 'c', 'c', 'c'], '_')
    print(tape)
    dtm = DTM(TMConfiguration(1, tape), set([6]), rulebook)
    [dtm.step() for i in range(10)]
    print(dtm.current_configuration)
    [dtm.step() for i in range(25)]
    print(dtm.current_configuration)
    dtm.run()
    print(dtm.current_configuration)

if __name__ == "__main__":
    main()
