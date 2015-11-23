from turing import turing_machine_from_file
from turing import blank_tape
from turing import Tape
from turing import TransitionFunction
from turing import TuringMachine
from turing import tape_from_file


def main():
    busy_beaver3 = turing_machine_from_file('examples/bb3.txt')
    busy_beaver3.compute(
        input_tape=tape_from_file('examples/bb3_input.txt'), print_results=False
    )

    busy_beaver4 = turing_machine_from_file('examples/bb4.txt')
    busy_beaver4.compute(
        input_tape=tape_from_file('examples/bb4_input.txt'), print_results=True
    )
main()
