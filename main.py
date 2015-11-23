from turing import turing_machine_from_file
from turing import blank_tape
from turing import Tape
from turing import TransitionFunction
from turing import TuringMachine
from turing import tape_from_file


def main():
    #
    # bb4_transition_fn = TransitionFunction(
    #     {0: {0: (1, 'r', 1),
    #          2: (0, 'l', -1),
    #          1: (1, 'l', 1)},
    #      1: {0: (1, 'l', 0),
    #          2: (0, 'l', -1),
    #          1: (0, 'l', 2)},
    #      2: {0: (1, 'r', 'HALT'),
    #          2: (0, 'l', -1),
    #          1: (1, 'l', 3)},
    #      3: {0: (1, 'r', 3),
    #          2: (0, 'l', -1),
    #          1: (0, 'r', 0)},
    #      -1: {0: (0, 'r', 0),
    #           2: (2, 'r', 0),
    #           1: (1, 'r', 0)}})
    # bb4_tm = TuringMachine(states={0, 1, 2, 3, 'HALT'},
    #                        alphabet={0, 1, 2},
    #                        blank=0,
    #                        input_alphabet={1, 2},
    #                        initial_state=0,
    #                        final_states={'HALT'},
    #                        transition_function=bb4_transition_fn)
    # bb4_result = bb4_tm.compute(input_tape=blank_tape(0, length=14,
    #                                                   start_index=10),
    #                             print_results=True)
    turing_machine_from_file('examples/bb3.txt').compute(
        input_tape=tape_from_file('examples/bb3_input.txt'), print_results=True
    )
main()
