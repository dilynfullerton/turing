from collections import Iterable
from collections import namedtuple
from collections import deque
from enum import Enum

DEFAULT_FILE_INPUT_DELIMITER = ','
DEFAULT_TAPE_DELIMITER = '|'
DEFAULT_MAX_ITER = None
DEFAULT_CURRENT_INDEX_COLOR = '\033[93m'
END_COLOR = '\033[0m'


class Transition(namedtuple('Transition', ['write', 'move', 'next_state'])):
    __slots__ = ()

    def __str__(self):
        return '(write {w}, move {m}, next {n})'.format(w=self.write,
                                                        m=self.move,
                                                        n=self.next_state)


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
                jth read value or a direction left or right of type 
                MoveDirection
          nsij = the next state associated with the ith state and jth read 
                 value

        :param transitions_map: a dictionary of the form specified above, which
        is to be converted into a transition function
        """
        self._function = dict()
        for state in transitions_map.keys():
            read_map = transitions_map[state]
            next_read_map = dict()
            for read_value in read_map.keys():
                transition_tuple = read_map[read_value]
                write, move, next_state = transition_tuple
                if isinstance(move, str):
                    move_char = move.lower()[0]
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
        try:
            return self._function[current_state][current_read]
        except KeyError:
            raise InvalidTuringMachineDefinitionException(
                '\nTransition function is incomplete: ' +
                'No transition available for state {} with read {}.'.format(
                    current_state, current_read
                )
            )


class InvalidTransitionsMapException(Exception):
    pass


class InvalidInputForTuringMachineException(Exception):
    pass


class MoveDirection(Enum):
    """Represents the possible move directions of the turing machine head
    """
    left = 0
    right = 1

    def __str__(self):
        if self == MoveDirection.left:
            return chr(10229)
        elif self == MoveDirection.right:
            return chr(10230)


class Tape:
    def __init__(self, initial_tape: list, start_index: int=0, blank=None,
                 tape_delim: str=DEFAULT_TAPE_DELIMITER,
                 current_index_color: str=DEFAULT_CURRENT_INDEX_COLOR,
                 end_color: str=END_COLOR):
        """Creates a tape object for use with a Turing Machine

        :param initial_tape: a list representing the input tape
        :param start_index: the index of the tape on which to start the Turing
        Machine; must be a valid index given the length of the list
        :param blank: the item to be interpreted as a blank and outputted as an
        empty space; this parameter is not necessary and not providing it will
        simply result in the blank being outputted just as it is provided (i.e.
        if blank is 'b', then 'b' would be outputted instead of ' ')
        """
        self._tape = initial_tape
        self._index = start_index

        self._blank = blank
        self._delim = tape_delim
        self._current_color = current_index_color
        self._end_color = end_color

    def move(self, direction: MoveDirection, blank):
        """Moves the turing machine head one space in the given direction

        :param direction: the direction to move the head or the Turing Machine
        :param blank: the character that will be initialized in added sections
        when the Turing Machine head goes beyond the end of the tape list
        """
        if direction is MoveDirection.left:
            if self._index == 0:
                self._tape.insert(0, blank)
            else:
                self._index -= 1
        elif direction is MoveDirection.right:
            if self._index == len(self._tape) - 1:
                self._tape.append(blank)
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
        for item, index in zip(self._tape, range(len(self._tape))):
            if item is self._blank:
                add_str = '{d} '.format(d=self._delim)
            else:
                add_str = '{d}{0}'.format(str(item), d=self._delim)
            if index == self._index:
                    add_str = self._current_color + add_str + self._end_color
            s += add_str
        s += '|]'
        return s

    def __repr__(self):
        return repr(self._tape)


def tape_from_file(filename: str, delim=DEFAULT_TAPE_DELIMITER):
    with open(filename) as f:
        lines_list = f.readlines()
    informative_lines = filter(lambda line: _is_acceptable_line(line),
                               lines_list)
    cured_lines = deque(map(lambda line: line.strip(' \n\r\t{}[]<>' + delim),
                            informative_lines))
    start_index = 0
    if len(cured_lines) == 2:
        start_index = int(cured_lines.pop())
    elif len(cured_lines) != 1:
        raise InvalidTapeFromFileException('A single line of tape and starting '
                                           'index was expected')
    input_tape_str = cured_lines.popleft()
    input_items = map(lambda s: s.strip(' \n\r\t{}[]<>'),
                      input_tape_str.split(delim))
    input_tape = list(input_items)
    return Tape(input_tape, start_index)


class InvalidTapeFromFileException(Exception):
    pass


class InvalidInputTapeException(Exception):
    pass


def blank_tape(blank, length: int, start_index: int=0):
    """Returns a blank Turing Machine tape with the specified blank item, 
    length and starting index

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

        self._is_consistent_turing_machine_definition()

    def compute(self, input_tape,
                max_iter=DEFAULT_MAX_ITER,
                print_results: bool=False,
                display_blank_as_empty=True):
        """Computes the input in accordance with the Turing Machine properties

        :param max_iter: the maximum number of iterations to allow
        :param input_tape: the tape to process (either a Tape object or a
        filename from which to generate the tape); must be initialized only with
        elements that are either blank or are in the input alphabet
        :param print_results: if true, prints out a string representation of
        the tape for each step
        :param display_blank_as_empty: if True, outputs blank characters as an
        empty space, if False, prints the string representation of the blanks
        :return: the tape as it is after being operated on
        """
        if isinstance(input_tape, Tape):
            current_tape = input_tape
        elif isinstance(input_tape, str):
            current_tape = tape_from_file(input_tape)
        else:
            raise InvalidInputTapeException('Tape input should either be a '
                                            'Tape or a filename from which to'
                                            'generate a Tape')
        if print_results and display_blank_as_empty:
            current_tape._blank = self._blank
        current_state = self._state0

        # Accumulators
        num_iter = 0
        all_tapes = list([str(current_tape)])
        all_states = list([str(current_state)])
        all_transitions = list()

        while True:
            if max_iter is not None and num_iter >= max_iter:
                break

            if current_state in self._final_states:
                break

            current_value = current_tape.read()
            if current_value not in self._alphabet:
                raise InvalidInputForTuringMachineException(
                    'Turing machine given invalid input '
                    '{0}'.format(current_value)
                )

            transition = self._tf.transition(current_state, current_value)

            # Turing Machine operations
            current_tape.write(transition.write)
            current_tape.move(transition.move, self._blank)
            current_state = transition.next_state

            # Update accumulators
            num_iter += 1
            all_tapes.append(str(current_tape))
            all_states.append(current_state)
            all_transitions.append(transition)

        all_transitions.append(None)

        if print_results:
            print()
            w_step = len(str(num_iter))
            w_state = max(map(lambda s: len(str(s)), all_states))
            w_tape = max(map(lambda t: len(str(t)), all_tapes))
            for step, state, tape, transition in zip(range(num_iter + 1),
                                                     all_states,
                                                     all_tapes,
                                                     all_transitions):
                print(('Step= {i:' + str(w_step) + '} \t' +
                       'State= {s:' + str(w_state) + '} \t' +
                       'Tape= {t:' + str(w_tape) + '} \t' +
                       'Transition= {n}').format(i=step, s=state, t=tape,
                                                 n=transition))

        return current_tape

    def _is_consistent_turing_machine_definition(self):
        """Checks whether the given Turing Machine definition is consistent and
        complete, based on its 7 parameter definition

        :return: True if the definition is consistent and complete, 
        False otherwise
        """
        if self._state0 not in self._states:
            raise InvalidTuringMachineDefinitionException(
                'Initial state {} not in allowed states.'.format(self._state0)
            )
        if not self._final_states.issubset(self._states):
            raise InvalidTuringMachineDefinitionException(
                'Final states set is not a subset of allowed states.'
            )
        if self._blank not in self._alphabet:
            raise InvalidTuringMachineDefinitionException(
                'Blank character {} not in alphabet.'.format(self._blank)
            )
        if not self._input_alphabet.issubset(self._alphabet):
            raise InvalidTuringMachineDefinitionException(
                'Input alphabet is not a subset of alphabet.'
            )
        try:
            self._is_valid_transition_function()
        except InvalidTuringMachineDefinitionException:
            raise
        return True

    def _is_valid_transition_function(self):
        """Tests whether the given transition function definition is valid by
        ensuring that
          + each state in states has a set of associated transitions for each
            value in the alphabet
          + each transition tuple contains a write value, a move direction, 
            and a next state
          + each write value is contained in the alphabet
          + each move value is either 'l' or 'r'
          + each next state is contained in the set of states

        :return: True if the transition function is consistent and complete 
        with respect to the Turing Machine parameters and False otherwise
        """
        for state in self._states - self._final_states:
            for value in self._alphabet:
                trans = self._tf.transition(state, value)
                try:
                    self._is_valid_transition_tuple(state, value, trans)
                except InvalidTuringMachineDefinitionException:
                    raise
            else:
                continue
        else:
            return True

    def _is_valid_transition_tuple(self, state, value, t: Transition):
        if state not in self._states - self._final_states:
            raise InvalidTuringMachineDefinitionException(
                '\nInvalid transition tuple for state {} reading {}:'.format(
                    state, value
                ) +
                'State {} is not in states - final states.'.format(state)
            )
        if value not in self._alphabet:
            raise InvalidTuringMachineDefinitionException(
                '\nInvalid transition tuple for state {} reading {}:'.format(
                    state, value
                ) +
                'Key {} is not in alphabet.'.format(value)
            )
        if t.write not in self._alphabet:
            raise InvalidTuringMachineDefinitionException(
                '\nInvalid transition tuple for state {} reading {}:'.format(
                    state, value
                ) +
                'Write value {} is not in alphabet.'.format(t.write)
            )
        if t.move not in MoveDirection:
            raise InvalidTuringMachineDefinitionException(
                '\nInvalid transition tuple for state {} reading {}:'.format(
                    state, value
                ) +
                '{} is not a valid move direction.'.format(t.move)
            )
        if t.next_state not in self._states:
            raise InvalidTuringMachineDefinitionException(
                '\nInvalid transition tuple for state {} reading {}:'.format(
                    state, value
                ) +
                'Next state {} not in states.'.format(t.next_state)
            )
        return True


class InvalidTuringMachineDefinitionException(Exception):
    pass


def turing_machine_from_file(filename: str,
                             delim: str=DEFAULT_FILE_INPUT_DELIMITER):
    """Produces a Turing Machine object from a file. The file should follow
    the following grammar

    <file> ::= <empty> <states> <empty> <initial state> <empty> <final states>
               <empty> <alphabet> <empty> <blank> <empty> <input alphabet>
               <empty> <transition function> <empty>
    <empty> ::= # <string> | <whitespace>
    <string> ::= <character>*
    <whitespace> ::= <whitespace char>* | <nothing>
    <whitespace char> ::= \n | \r | \t | <space>
    <states> ::= <set of states>
    <set of states> ::= {<state> <whitespace>, * }
    <state> ::= <string>
    <initial state> ::= <state>
    <final states> ::= <set of states>
    <alphabet> ::= <set of string>
    <set of string> ::= {<string> <whitespace>, * }
    <blank> ::= <string>
    <input alphabet> ::= <set of string>
    <transition function ::= <transition tuple> <empty> *
    <transition tuple> ::= < <state> <whitespace>, <value> <whitespace>,
                             <transition> <whitespace> >
    <value> ::= <string>
    <transition> ::= <write> <whitespace>, <move> <whitespace>, <state>
                     <whitespace>
    <write> ::= <string>
    <move> ::= l | left | r | right

    :param delim:
    :param filename: the file from which to produce the Turing Machine
    :return: the Turing Machine object produced from the file's specifications
    """
    with open(filename) as f:
        lines_list = f.readlines()
    informative_lines = filter(lambda line: _is_acceptable_line(line),
                               lines_list)
    cured_lines = deque(map(lambda line: line.strip(' \n\r\t<>[]{}'),
                            informative_lines))
    # Get states
    states_str = cured_lines.popleft()
    tm_states = frozenset(_set_parse(states_str, delim))

    # Get initial state
    tm_initial_state = str(cured_lines.popleft())

    # Get final states
    final_states_str = cured_lines.popleft()
    tm_final_states = frozenset(_set_parse(final_states_str, delim))

    # Get alphabet
    alphabet_str = cured_lines.popleft()
    tm_alphabet = frozenset(_set_parse(alphabet_str, delim))

    # Get blank
    tm_blank = str(cured_lines.popleft())

    # Get input alphabet
    in_alphabet_str = cured_lines.popleft()
    tm_input_alphabet = frozenset(_set_parse(in_alphabet_str, delim))

    # Get transition function
    tm_transition_function = _transition_function_from_lines(cured_lines,
                                                             delim)

    return TuringMachine(states=tm_states,
                         initial_state=tm_initial_state,
                         final_states=tm_final_states,
                         alphabet=tm_alphabet,
                         blank=tm_blank,
                         input_alphabet=tm_input_alphabet,
                         transition_function=tm_transition_function)


def _transition_function_from_lines(lines: Iterable, delim: str):
    tf = dict()
    for line_str in lines:
        state, value, write, move_str, next_state = _set_parse(line_str, delim)
        move = move_str.lower()[0]
        transition = Transition(write, move, next_state)
        if state not in tf.keys():
            tf[state] = dict()
        tf[state][value] = transition
    return TransitionFunction(tf)


def _move_from_move_str(move_str: str):
    move_char = move_str.lower()[0]
    if move_char == 'l':
        return MoveDirection.left
    elif move_char == 'r':
        return MoveDirection.right
    else:
        raise InvalidTuringMachineFileDefinitionException(
                '"{ms}" was not understood as a move direction; please '
                'enter "left" ("l") or '
                '"right" ("r").'.format(ms=move_str)
            )


def _is_acceptable_line(line: str):
    return line[0] != '#' and len(line.strip(' \n\t\r')) > 0


def _set_parse(set_str: str, delim):
    trimmed_set = set_str.strip(' \n\t\r{}[]<>')
    elements = trimmed_set.split(delim)
    return map(lambda s: s.strip(), elements)


class InvalidTuringMachineFileDefinitionException(Exception):
    pass
