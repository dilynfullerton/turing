from collections import Iterable
from collections import namedtuple
from enum import Enum


class TuringMachine:
    """A Turing Machine, implemented to reflect the formal definition on
    https://en.wikipedia.org/wiki/Turing_machine
    """

    def __init__(self, states: Iterable, initial_state, final_states: Iterable,
                 alphabet: Iterable, blank, input_alphabet: Iterable,
                 transition_function: TransitionFunction):
        """Initializes the TuringMachine object

        :param states: a finite iterable containing all of the  states the
        Turing Machine can theoretically take; must contain at least one state;
        states must be hashable
        :param initial_state: a string representation of the state that the
        Turing Machine begins in; this must be contained in states
        :param final_states: the set of states that will cause the Turing
        Machine to halt; must be a subset of states.
        :param alphabet: a finite iterable containing all of the items the
        Turing machine should recognize; must contain at least one item; items
        must be hashable
        :param blank: the item in the alphabet that is to be interpreted as a
        blank section on the tape; must also be contained in the alphabet
        :param input_alphabet: the set of items that the Turing Machine
        should interpret as input; the must be a subset of the alphabet set
        minus the blank term
        :param transition_function: the transition function which, based on the
        current state and read value, specifies how to proceed; must contain a
        mapping for each pair (q, r) -> (w, m, qn), where
           q is in the space of all non-final states,
           r is in the alphabet,
           w is in the alphabet,
           m is either left or right, and
          qn is in the space of all states.
        """
        self._states = frozenset(states)
        self._state0 = initial_state
        self._final_states = frozenset(final_states)
        self._alphabet = frozenset(alphabet)
        self._input_alphabet = frozenset(input_alphabet)
        self._blank = blank
        self._tf = transition_function

    def compute(self, input_tape: Tape, print_results: bool=False):
        """Computes the input in accordance with the Turing Machine's properties

        :param input_tape: the tape to process; must be initialized only with
        elements that are either blank or are in the input alphabet
        :param print_results: if true, prints out a string representation of the
        tape for each step
        :return: the tape, as it is after being operated on
        """
        current_tape = input_tape
        current_state = self._state0
        while True:
            if print_results:
                print(current_tape)
            if current_state in self._final_states:
                break
            current_value = current_tape.read()
            if current_value not in self._alphabet:
                raise InvalidInputForTuringMachineException(
                    'Turing machine given invalid input '
                    '{0}'.format(current_value)
                )
            transition = self._tf.transition(current_state, current_value)
            current_tape.write(transition.write)
            current_tape.move(transition.move)
            current_state = transition.next_state
        if print_results:
            print(current_tape)
        return current_tape


class Tape:
    def __init__(self, blank, initial_tape: list=list(), start_index: int=0):
        """Creates a tape object for use with a Turing Machine

        :param blank: the item to be interpreted as a blank
        :param initial_tape: a list representing the input tape
        :param start_index: the index of the tape on which to start the Turing
        Machine; must be a valid index given the length of the list
        """
        self._tape = initial_tape
        self._blank = blank
        self._index = start_index

    def move(self, direction: MoveDirection):
        """Moves the head of the turing machine one space in the given direction

        :param direction: the direction to move the head or the Turing Machine
        """
        if direction is MoveDirection.left:
            if self._index == 0:
                self._tape.insert(0, self._blank)
            else:
                self._index -= 1
        elif direction is MoveDirection.right:
            if self._index == len(self._tape) - 1:
                self._tape.append(self._blank)
            self._index += 1

    def read(self):
        """Returns the value at the current location of the head of the Turing
        Machine
        """
        return self._tape[self._index]

    def write(self, item):
        """Writes the given item into the current location of the head of the
        Turing Machine

        :param item: the item to write; must be in the alphabet
        """
        self._tape[self._index] = item

    def __str__(self):
        s = '['
        for item in self._tape:
            if item is self._blank:
                s += ' , '
            else:
                s += '{0}, '.format(str(item))
        s = s[:-2] + ']'
        return s

    def __repr__(self):
        return repr(self._tape)


def blank_tape(blank, length: int, start_index: int=0):
    """Returns a blank Turing Machine tape with the specified blank item, length
    and starting index

    :param blank: the item to add (represents a blank)
    :param length: the length of the tape to produce; note that the Turing
    Machine may extend the tape arbitrarily in either direction (this length is
    not in any way binding)
    :param start_index: the index of the tape at which to place the head of the
    Turing Machine during computation
    :return: a blank Tape with the specified blank, length, and starting index
    """
    tape_values = [blank for x in range(length)]
    return Tape(blank, tape_values, start_index)

Transition = namedtuple('Transition', ['write', 'move', 'next_state'])


class TransitionFunction:
    """Represents the mapping (q, r) -> (w, m, qn), where
           q is in the space of all non-final states,
           r is in the alphabet,
           w is in the alphabet,
           m is either left or right, and
          qn is in the space of all states.
       This mapping is an inherent state of the machine, and so it is never
       mutated.
    """
    def __init__(self, transitions_map: dict):
        """Initializes the transition function from a map of the form
                {s0: {r0: (w00, d00, ns00),
                      r1: (w01, d01, ns01),
                      ...,
                      rN: (w0N, d0N, ns0N)},
                 s1: {r0: (w10, d10, ns10),
                      ...,
                      rN: (w1N, d1N, ns1N)},
                 ...,
                 sM: {r0: (wM0, dM0, nsM0),
                      ...,
                      rN: (wMN, dMN, nsMN)}}
        where
          si = ith state
          rj = jth possible read value
          wij = write value associated with the ith state and jth read value
          dij = direction string 'l' or 'r' associated with the ith state and
                jth read value
          nsij = the next state associated with the ith state and jth read value

        :param transitions_map: a dictionary of the form specified above, which
        is to be converted into a transition function
        """
        self._function = dict()
        for state in transitions_map.keys():
            read_map = transitions_map[state]
            next_read_map = dict()
            for read_value in read_map.keys():
                transition_tuple = read_map[read_value]
                write, move_str, next_state = transition_tuple
                move_char = move_str.lower()[0]
                if move_char == 'l':
                    move = MoveDirection.left
                elif move_char == 'r':
                    move = MoveDirection.right
                else:
                    raise InvalidTransitionsMapException()
                next_read_map[read_value] = Transition(write, move, next_state)
            self._function[state] = next_read_map

    def transition(self, current_state, current_read):
        """Returns the named 3-tuple associated with the current state and
        current read value in accordance with the transition function

        :param current_state: the current state of the Turing machine
        :param current_read: the value at the current location of the head
        :return: the 3-tuple associated with the next transition
        """
        return self._function[current_state][current_read]


class InvalidTransitionsMapException(Exception):
    pass


class InvalidInputForTuringMachineException(Exception):
    pass


class MoveDirection(Enum):
    """Represents the possible move directions of the head of the turing machine
    """
    left = 0
    right = 1
