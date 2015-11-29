from turing import turing_machine_from_file
from turing import tape_from_file


def main():
    busy_beaver3 = turing_machine_from_file('examples/bb3.txt')
    busy_beaver3.compute(
        input_tape=tape_from_file('examples/bb3_input.txt'), print_results=False
    )

    busy_beaver4 = turing_machine_from_file('examples/bb4.txt')
    busy_beaver4.compute(
        input_tape=tape_from_file('examples/bb4_input.txt'), print_results=False
    )

    copy_machine = turing_machine_from_file('examples/copy.txt')
    copy_machine.compute(
        input_tape=tape_from_file('examples/copy_input.txt'),
        print_results=False
    )
    copy_machine.compute(
        input_tape=tape_from_file('examples/copy_input2.txt'),
        print_results=False
    )

    subtractor = turing_machine_from_file('examples/subtract.txt')
    subtractor.compute(
        input_tape=tape_from_file('examples/subtract_3_2.txt'),
        print_results=False
    )
    subtractor.compute(input_tape=tape_from_file('examples/subtract9_5.txt'),
                       print_results=False)

    counter = turing_machine_from_file('examples/counter.txt')
    counter.compute(input_tape=tape_from_file('examples/count_to_16.txt'),
                    print_results=False)

    adder = turing_machine_from_file('examples/add.txt')
    adder.compute(input_tape=tape_from_file('examples/add2_2.txt'),
                  print_results=False)

    wolfram23 = turing_machine_from_file('examples/wolfram2_3.txt')
    wolfram23.compute(
        input_tape=tape_from_file('examples/wolfram2_3_input.txt'),
        print_results=True,
        max_iter=100
    )
main()
