from turing import TuringMachine, TransitionFunction, blank_tape


def main():
    bb3_transition_fn = TransitionFunction({'A': {0: (1, 'r', 'B'),
                                                  1: (1, 'l', 'C')},
                                            'B': {0: (1, 'l', 'A'),
                                                  1: (1, 'r', 'B')},
                                            'C': {0: (1, 'l', 'B'),
                                                  1: (1, 'r', 'HALT')}})
    bb3_tm = TuringMachine(states={'A', 'B', 'C', 'HALT'},
                           alphabet={0, 1},
                           blank=0,
                           input_alphabet={1},
                           initial_state='A',
                           final_states={'HALT'},
                           transition_function=bb3_transition_fn)
    bb3_result = bb3_tm.compute(input_tape=blank_tape(0, 1),
                                print_results=False)

    bb4_transition_fn = TransitionFunction(
        {0: {0: (1, 'r', 1),
             2: (0, 'l', -1),
             1: (1, 'l', 1)},
         1: {0: (1, 'l', 0),
             2: (0, 'l', -1),
             1: (0, 'l', 2)},
         2: {0: (1, 'r', 'HALT'),
             2: (0, 'l', -1),
             1: (1, 'l', 3)},
         3: {0: (1, 'r', 3),
             2: (0, 'l', -1),
             1: (0, 'r', 0)},
         -1: {0: (0, 'r', 0),
              2: (2, 'r', 0),
              1: (1, 'r', 0)}})
    bb4_tm = TuringMachine(states={0, 1, 2, 3, 'HALT'},
                           alphabet={0, 1, 2},
                           blank=0,
                           input_alphabet={1, 2},
                           initial_state=0,
                           final_states={'HALT'},
                           transition_function=bb4_transition_fn)
    bb4_result = bb4_tm.compute(input_tape=blank_tape(0, length=14,
                                                      start_index=10),
                                print_results=True)

main()
