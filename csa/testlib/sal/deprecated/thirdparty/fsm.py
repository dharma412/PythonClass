#!/usr/bin/env python
# -*- Mode: Python; tab-width: 4 -*-
# vim:ts=4:sw=4:expandtab:softtabstop=4:smarttab
#
# From code by Noah Spurrier 
#
'''This module implements a Finite State Machine (FSM) with one stack.
The FSM is fairly simple. It is useful for small parsing tasks.
The addition of a stack makes it much simpler to build tiny parsers.

The FSM is an association of
    (input_symbol, current_state) --> (action, next_state)
When the FSM matches the pair (input_symbol, current_state)
it will call the associated action and then set the next state.
The action will be passed input_symbol, current state, and a stack.
'''
#: Reference Symbols: fsm

# $Id: //prod/main/sarf_centos/testlib/sal/deprecated/thirdparty/fsm.py#1 $
__revision = '$Revision: #1 $'

import re


class ANY:
    '''This is a meta key. This is a class, but you use it like a value.
    Example: x = ANY
    Example: f.add_transition (ANY, 'SOMESTATE', None, 'OTHERSTATE')
    '''
    pass


class FSM:
    '''This class is a Finite State Machine (FSM) with one stack.
    You set up a state transition table which is
    The FSM is an association of
        (input_symbol, current_state) --> (action, next_state)
    When the FSM matches a pair (current_state, input_symbol)
    it will call the associated action
    The action is a function reference defined with a signature like this:
            def a (input_symbol, fsm):
    and pass as parameters the current state, the input symbold, and a stack.
    As an additional aid a stack is given.
    The stack is really just a list.
    The action function may produce output and update the stack.
    '''

    def __init__(self, initial_state=None):
        self.state_transitions = {}  # Map (input_symbol, state) to (action, next_state).
        self.default_transition = None
        self.initial_state = initial_state
        self.current_state = self.initial_state
        self.stack = []

    def push(self, v):
        '''This pushes a value onto the stack.'''
        self.stack.append(v)

    def pop(self):
        '''This pops a value off the stack and returns the value.'''
        return self.stack.pop()

    def reset(self):
        '''This clears the stack and resets the current_state to the initial_state.
        '''
        self.current_state = self.initial_state
        self.stack = []

    def add_default_transition(self, action, next_state):
        '''This sets the default transition.
        If the FSM cannot match the pair (input_symbol, current_state)
        in the transition table then this is the transition that 
        will be returned. This is useful for catching errors and undefined states.
        The default transition can be removed by calling
        add_default_transition (None, None)
        If the default is not set and the FSM cannot match
        the input_symbol and current_state then it will 
        raise an exception (see process()).
        '''
        if action == None and next_state == None:
            self.default_transition = None
        else:
            self.default_transition = (action, next_state)

    def add_transition(self, input_symbol, state, action, next_state):
        '''This adds an association between inputs and outputs.
                (input_symbol, current_state) --> (action, next_state)
           The action may be set to None.
           The input_symbol may be set to None.
        '''
        self.state_transitions[(input_symbol, state)] = (action, next_state)

    def add_transition_list(self, list_input_symbols, state, action, next_state):
        '''This adds lots of the same transitions for different input symbols.
        You can pass a list or a string. Don't forget that it is handy to use
        string.digits, string.letters, etc. to add transitions that match 
        those character classes.
        '''
        for input_symbol in list_input_symbols:
            self.add_transition(input_symbol, state, action, next_state)

    # XXX
    def add_transition_re(self, regex, state, action, next_state):
        self.state_transitions[(re.compile(regex), state)] = (action, next_state)

    def get_transition(self, input_symbol, state):
        '''This tells what the next state and action would be 
        given the current state and the input_symbol.
        This returns (action, new state).
        This does not update the current state
        nor does it trigger the output action.
        If the transition is not defined and the default state is defined
        then that will be used; otherwise, this throws an exception.
        '''
        if self.state_transitions.has_key((input_symbol, self.current_state)):
            return self.state_transitions[(input_symbol, self.current_state)]
        elif self.state_transitions.has_key((ANY, self.current_state)):
            return self.state_transitions[(ANY, self.current_state)]
        elif self.default_transition != None:
            return self.default_transition
        else:
            raise Exception('Transition is undefined.')

    def process(self, input_symbol):
        '''This causes the fsm to change state and call an action.
        (input_symbol, current_state) --> (action, next_state)
        If the action is None then the action is not called and
        only the current state is changed.
        '''
        (action, next_state) = self.get_transition(input_symbol, self.current_state)
        if action != None:
            apply(action, (input_symbol, self))
        self.current_state = next_state

    def process_string(self, s):
        for c in s:
            self.process(c)


if __name__ == '__main__':
    import os

    os.system("iafunittest test_fsm")
