import re

from Integer import *
from algorithmsCombined import *

class Context():
    """
    """

    def __init__(self):
        self.reset()

    def reset(self):
        self.x = None
        self.y = None
        self.radix = None
        self.op = None
        self.m = None

    def read_line(self, line):
        original_line = line
        line = re.sub('\s', '', line) # Remove all whitespace

        if len(line) == 0:
            if not self.op:
                return '\n'

            if self.op in (addition, subtraction):
                computed = self.op(self.x.digits, self.x.positive, self.y.digits, self.y.positive, self.x.radix)
                answer = Integer(computed[1], self.radix, computed[0])
                self.reset()
                return f'[answer] {answer}\n\n'

            elif self.op in (multiplication, karatsuba):
                computed = self.op(self.x.digits, self.x.positive, self.y.digits, self.y.positive, self.x.radix)
                answer = Integer(computed[1], self.radix, computed[0])
                add = computed[2]
                mul = computed[3]
                self.reset()
                return f'[answer] {answer}\n[count-add] {add}\n[count-mul] {mul}\n\n'

            elif self.op in (modular_reduction, modular_inversion):
                computed = self.op(self.x.digits, self.x.positive, self.m.digits, self.x.radix)
                if isinstance(computed, str):
                    self.reset()
                    return '[answer] inverse does not exist\n\n'
                else:
                    answer = Integer(computed[1], self.radix, computed[0])
                    self.reset()
                    return f'[answer] {answer}\n\n'

            elif self.op in (modular_addition, modular_subtraction, modular_multiplication):
                computed = self.op(self.x.digits, self.x.positive, self.y.digits, self.y.positive, self.m.digits, self.x.radix)
                answer = Integer(computed[1], self.radix, computed[0])
                self.reset()
                return f'[answer] {answer}\n\n'

            elif self.op == euclidean:
                computed = self.op(self.x.digits, self.x.positive, self.y.digits, self.y.positive, self.x.radix)
                d = Integer(computed[0], self.x.radix)
                a = Integer(computed[1][1], self.x.radix, computed[1][0])
                b = Integer(computed[2][1], self.x.radix, computed[2][0])
                self.reset()
                return f'[answ-d] {d}\n[answ-a] {a}\n[answ-b] {b}\n\n'

        if line[0] == '#':
            # Line is a comment, just return it
            return original_line

        bracket_index = line.find(']')
        command = line[1:bracket_index]     # Extract text between brackets
        argument = line[bracket_index + 1:] # Extract argument after command

        if command == 'radix':
            self.radix = int(argument)

        elif command == 'x':
            self.x = Integer(argument, self.radix)

        elif command == 'y':
            self.y = Integer(argument, self.radix)

        elif command == 'm':
            self.m = Integer(argument, self.radix)

            if self.op == addition:
                self.op = modular_addition
            elif self.op == subtraction:
                self.op = modular_subtraction
            elif self.op == multiplication:
                self.op = modular_multiplication

        elif command == 'add':
            if self.m:
                self.op = modular_addition
            else:
                self.op = addition

        elif command == 'subtract':
            if self.m:
                self.op = modular_subtraction
            else:
                self.op = subtraction

        elif command == 'multiply':
            if self.m:
                self.op = modular_multiplication
            else:
                self.op = multiplication

        elif command == 'karatsuba':
            self.op = karatsuba

        elif command == 'reduce':
            self.op = modular_reduction

        elif command == 'inverse':
            self.op = modular_inversion

        elif command == 'euclid':
            self.op = euclidean

        elif command in ('answer', 'count-add', 'count-mul', 'answ-d', 'answ-a', 'answ-b'):
            # Ignore and don't write to output
            return ''

        return original_line
