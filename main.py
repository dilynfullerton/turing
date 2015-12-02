from turing import turing_machine_from_file
from turing import tape_from_file


def main():
    busy_beaver3 = turing_machine_from_file('examples/bb3.txt')
    busy_beaver3.compute(
        input_tape='examples/bb3_input.txt',
        print_results=False)

    busy_beaver4 = turing_machine_from_file('examples/bb4.txt')
    busy_beaver4.compute(
        input_tape='examples/bb4_input.txt',
        print_results=False)

    copy_machine = turing_machine_from_file('examples/copy.txt')
    copy_machine.compute(
        input_tape='examples/copy_input.txt',
        print_results=False)
    copy_machine.compute(
        input_tape='examples/copy_input2.txt',
        print_results=False)

    subtractor = turing_machine_from_file('examples/subtract.txt')
    subtractor.compute(
        input_tape='examples/subtract_3_2.txt',
        print_results=False)
    subtractor.compute(
        input_tape='examples/subtract9_5.txt',
        print_results=False)

    counter = turing_machine_from_file('examples/counter.txt')
    counter.compute(
        input_tape='examples/count_to_16.txt',
        print_results=False)

    adder = turing_machine_from_file('examples/add.txt')
    adder.compute(
        input_tape='examples/add2_2.txt',
        print_results=False)

    wolfram23 = turing_machine_from_file('examples/wolfram2_3.txt')
    wolfram23.compute(
        input_tape='examples/wolfram2_3_input.txt',
        print_results=False, max_iter=150)

    infinite_printer = turing_machine_from_file('examples/infinite_print.txt')
    infinite_printer.compute(
        input_tape='examples/infinite_print_input.txt',
        print_results=False, max_iter=100)

    copy_machine9000 = turing_machine_from_file('examples/binary_copy.txt')
    copy_machine9000.compute(
        input_tape='examples/binary_copy_input.txt',
        print_results=True)

    negator = turing_machine_from_file('examples/negator.txt')
    negator.compute(
        input_tape='examples/negator_input0.txt',
        print_results=False
    )
    negator.compute(
        input_tape='examples/negator_input1.txt',
        print_results=False,
        max_iter=20
    )

    nand = turing_machine_from_file('examples/nand.txt')
    nand.compute(
        input_tape='examples/nand_input.txt',
        print_results=False
    )
main()
