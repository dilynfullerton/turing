# turing
A tool for simulating arbitrary Turing Machines written in Python 3.

### About this codes
---
Currently, the design is such that it is best used for educational
purposes. Arbitrary Turing Machines and their inputs can be specified
by their seven parameters via text files in conjunction with the
examples included. Turing Machines and their inputs can also be
created and computed via Python codes, such that if one wanted to
design a program to use the TuringMachine definition, one could do so
without too much difficulty.

A \*.txt file can be written to specify the seven parameters that
define a Turing machine. Then it can be created using the
```turing_machine_from_file()``` function.

### Turing machine definition format
---
A Turing machine is defined by seven parameters:

1. _**States**_: The set of states that the Turing machine may be in.
2. _**Initial state**_: The states that the Turing machine starts in.
3. _**Halting states**_: The subset of _States_ that represent halting
(final) states
4. _**Alphabet**_: The set of "characters" that can be written on the
tape.
5. _**Blank**_: The "character" in the alphabet that represents a
blank tape square.
6. _**Input alphabet**_: The subset of _Alphabet_ (minus the _Blank_)
that are acceptable inputs.
7. _**Transition function**_: A partial function that specifies a
_write character_, _move direction_, and _next state_ for each
combination of the set of non-halting states and the set of
alphabet characters.

In my program, these are represented by the following in order in a
\*.txt file.

1. _**States**_:
   ```python
   # States
   {State0, State1, ..., (:, ):}
   ```

States are represented by a single line contained in braces, with
named state strings separated by commas.

2. _**Initial state**_:
   ```python
   # Initial state
   State0
   ```

The initial state must be one of the named states in the states set.

3. _**Final states**_:
   ```python
   # Final states
   {(:, ):, ...}
   ```

The final states are written in the same format as the states, and all
of the final states must be contained in the states set. I typically
use ```(:``` for a successful completion and ```):``` for an
unsuccessful completion.

4. _**Alphabet**_:
   ```python
   # Alphabet
   {B, 0, 1, ...}
   ```

The alphabet is provided in the same format as the states. I typically
use single-character strings for nice print display, but this is not
necessary.

5. _**Blank**_: 
   ```python
   # Blank
   B
   ```

The blank is a single string that is also contained in the alphabet.

6. _**Input alphabet**_: 
   ```python
   # Input alphabet
   {1, ...}
   ```

The input alphabet is provided in the same format as the alphabet, and
all strings in the input alphabet must be in the alphabet. The blank
may not be included as part of the input alphabet.

7. _**Transition function**_: 

   ```python
   <State0, B, 0, r, ):>
   <State0, 0, 0, r, ):>
   <State0, 1, 0, r, ):>
   ...

   <State1, B, 0, r, ):>
   <State1, 0, 0, r, ):>
   <State1, 1, 0, r, ):>
   ...

   ...
   ```

The transition function is provided as a series of 5-tuples, contained
in angle brackets and separated by commas. These are

   ```python
   < current state, read value, write value, move direction, next state >
   ```

A line reads as follows: if the machine is in ```current state``` and
reads ```read value```, then it replaces that with ```write value```,
moves one square in ```move direction```, and enters ```next state```.

Every single combination of the states minus the final states and
the possible read values (i.e. the whole alphabet) must be provided
a write value, move direction, and next state.

### Examples
---
The following are example Turing machine algorithms that I wrote.

* ```binary_copy.txt```: Copies a binary number
* ```collatz.txt```: Performs the algorithm of the Collatz Conjecture
and creates a recording of the actions performed. 
* ```factorial.txt```: Performs the factorial of the given nubmer.
* ```infinite_print.txt```: Infinite printer, to demonstrate a
non-halting Turing maching.
* ```is_prime.txt```: Tests if the given number is prime.
* ```nand.txt```: Fundamental logic gate.
* ```negator.txt```: Negator, as part of the proof sketch that a
Universal Turing Machine that solves the halting problem cannot exist.
* ```quicksort.txt```: Sorts a series of integers in place.

### About Turing Machines
---
```turing.pptx``` is a PowerPoint I presented in class for a
"How Things Work" series.

### See also
---
* http://plato.stanford.edu/entries/turing-machine/
* http://plato.stanford.edu/entries/church-turing/
* http://plato.stanford.edu/entries/goedel-incompleteness/
* https://math.stanford.edu/~feferman/papers/deciding.pdf
* http://www.philocomp.net/home/hilbert.htm
* http://www.philocomp.net/home/turing.htm
* http://www.dna.caltech.edu/courses/cs129/caltech_restricted/Turing_1936_IBID.pdf
* https://www.youtube.com/channel/UC9-y-6csu5WGm29I7JiwpnA
* https://youtu.be/GP21wU6R0-o?list=PLslgisHe5tBM8UTCt1f66oMkpmjCblzkt
