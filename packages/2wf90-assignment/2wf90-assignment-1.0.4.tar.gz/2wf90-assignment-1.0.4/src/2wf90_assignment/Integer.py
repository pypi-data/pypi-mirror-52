# Use like this: "from classes import Integer".

class Integer:
    """
    Class used to store large integers. Detailed documentation is given below,
    so here are some common use cases:

        from Integer import *

        i = Integer('6A', 16, False)
        i.digits   -> [6, 10]
        i.radix     -> 16
        i.positive -> False

        i.digits[0] = 1
        print(i) -> '-1A'
        repr(i)  -> '-[1, 10] (radix 16)'

        i = -i
        print(i) -> '1A'

        len(i) -> 2
        i = i.pad(6)
        repr(i) -> +[0, 0, 0, 0, 1, 10] (radix 16)
        len(i) -> 6

        j = Integer([1, 10, 2, 13], 16)
        print(j) -> '1A2D'
    """
    def __init__(self, digits, radix = 10, positive = True):
        """
        Arguments:
            digits:
                A list of numbers - they should all be lower than the radix.
                The most significant numbers are at the beginning of this list.
                A string can be used as well, e.g. '13AF'.
            radix:
                radix of the number. Decimal by default.
            positive:
                True if the number has a positive sign, False if negative.
                Positive by default.

        Examples:
            Integer([1, 0, 14, 2], 16, False)  -> -10E2   (radix 16)
            Integer('-100101', 2)              -> -100101 (radix 2)
            Integer([1, 2, 3])                 -> +123    (radix 10)
        """

        if radix > 16:
            raise ValueError(f'radix is {radix}. radixs beyond 16 are not supported.')

        if radix < 1:
            raise ValueError(f'radix is {radix}. radix must be positive.')

        if len(digits) == 0:
            raise ValueError('Digit list cannot be empty.')

        # Sanity checks when digits are given as a list.
        if type(digits) is list:
            for digit in digits:
                if digit >= radix:
                    raise ValueError(f'Digit {digit} is not allowed in radix {radix}.')

                if (digit < 0):
                    raise ValueError(f'Digit {digit} may not be negative.')

        # Sanity checks when digits are given as a string.
        # Also transforms string into its list representation.
        if type(digits) is str:
            if digits[0] == '-':
                positive = False
                digits = digits[1:]

            new_digits = []

            for digit in digits:
                num = char_to_number(digit)
                if num >= radix:
                    raise ValueError(f'Digit {digit} is not allowed in radix {radix}.')
                new_digits.append(num)

            digits = new_digits

        self.digits = digits
        self.radix = radix
        self.positive = positive

        # We could remove leading zeroes here using self.strip(), but for
        # assignment 1 that shouldn't be neccesary.

    def __len__(self):
        """
        Useful shortcut. Example:

            i = new Integer([1, 2, 3], 8)
            len(i) -> 3
            len(i) == len(i.digits) -> True
        """
        return len(self.digits)

    def __neg__(self):
        """
        Negation operator. Example:

            i = new Integer('ABC', 16)
            i -> +[10, 11, 12] (radix 16)
            -i -> -[10, 11, 12] (radix 16)
        """
        new_int = self.copy()
        new_int.positive = not new_int.positive
        return new_int

    def __str__(self):
        """
        Represent integer as a string. The radix is not given, and a minus sign
        is added if negative. This is the same as notation found in input.

        Examples:
            str(Integer('6A', 16, False)) -> -6A
        """
        return ('' if self.positive else '-') + f'{self.get_digit_string()}'

    def __repr__(self):
        """
        Represent as string, but with more information. Useful for debugging.
        The digit list is always printed, along with the sign and radix.

        Examples:
            repr(Integer('6A', 16, False)) -> -[6, 10] (radix 16)
        """
        return ('+' if self.positive else '-') + f'{self.digits} (radix {self.radix})'

    def __abs__(self):
        if self.positive:
            return self.copy()
        else:
            return -self

    def pad(self, size):
        """
        Add leading zeroes to the digit list to ensure it becomes a certain size.
        Returns a new copy of the Integer, so that the original one isn't modified.

        Example:
            i = Integer([1])
            i = i.pad(4)
            i.digits -> [0, 0, 0, 1]
        """
        original_size = len(self.digits)

        if size < original_size:
            raise ValueError(f'New size {size} is below original size {original_size}')

        new_int = self.copy()
        new_int.digits = [0] * (size - original_size) + new_int.digits
        return new_int

    def strip(self):
        """
        Remove trailing zeroes from the digit list. Undoes Integer.pad().
        Also called in the constructor.
        """
        new_int = self.copy()
        while new_int.digits[0] == 0 and len(new_int.digits) > 1:
            new_int.digits = new_int.digits[1:]
        return new_int

    def get_digit_string(self):
        """
        Returns the integer's digits as a string, not a list. It converts digits
        above 9 to the hexadecimal counterparts.

        Used by the class internally. Don't call it directly, but use print(i)
        instead.
        """
        s = ''
        for digit in self.digits:
            s = s + number_to_char(digit)
        return s

    def copy(self):
        """
        Returns a distinct copy of itself.
        """
        digits_copy = self.digits.copy()
        return Integer(digits_copy, self.radix, self.positive)

def char_to_number(character):
    character = character.upper()
    index = '0123456789ABCDEF'.find(character)

    if index == -1:
        raise ValueError('Character must be hexadecimal notation.')

    return index

def number_to_char(number):
    return '0123456789abcdef'[number] # ;)
