class Validator:

    def __init__(self, length, chars, Chars, nums, symbols, **kwargs):

        self.text = ''  # will be the .verify() input
        self.length = length
        if len(self.length) < 2:
            self.length.append(float('inf'))  # set length second element to infinity if not present
        self.chars = chars  # lower-case
        self.Chars = Chars  # upper-case
        self.nums = nums
        self.symbols = symbols
        self.symbols_list = [s for s in kwargs.get('symbols_list',
                                                   '!"#$%&\'()*+,-./:;<=>?@[\\]^_{|}~')]
        # list the symbols (default or argument)

    @staticmethod
    def __safe_get(l, index, default):  # get from list with default value
        try:
            return l[index]
        except IndexError:
            return default

    def __check(self, func, limit):  # check if a type of character is present enough times
        if limit:
            chars = 0
            for char in self.text:
                chars += 1 if func(char) else 0  # count
            return not limit[0] <= chars <= self.__safe_get(limit, 1, self.length[1])  # check if in bounds
        return False

    def extra_validation(self, text):  # need to be overwritten
        raise NotImplementedError('Extra validation not implemented')

    def verify(self, text: str):
        self.text = text

        extra = self.extra_validation(self.text)  # call extra_validation
        if extra:  # if response is not None
            return extra  # return error

        if not self.length[0] <= len(self.text) <= self.length[1]:  # check for length
            return False, 'length'

        if self.__check(lambda c: c.islower(), self.chars):  # check for lower-case
            return False, 'lower'

        if self.__check(lambda c: c.isupper(), self.Chars):  # check for upper-case
            return False, 'upper'

        if self.__check(lambda c: c.isdigit(), self.nums):  # check for digits
            return False, 'digit'

        if self.__check(lambda c: c in self.symbols_list, self.symbols):  # check for symbols
            return False, 'symbols'

        return True, ''  # if all verifications passed


class UsernameValidator(Validator):
    def __init__(self, length, chars, Chars, nums, symbols, **kwargs):
        super().__init__(length, chars, Chars, nums, symbols, **kwargs)
        self.django = kwargs.get('django_model', None)  # add django argument

    def extra_validation(self, text):
        model = self.django
        if model:
            if model.objects.filter(username=text):  # check in the database
                return False, 'existing'
        return None


class PasswordValidator(Validator):
    def __init__(self, length, chars, Chars, nums, symbols, **kwargs):
        super().__init__(length, chars, Chars, nums, symbols, **kwargs)
        self.username = kwargs.get('username', None)  # add username argument

    def extra_validation(self, text):
        if text == self.username:  # check if is equal
            return False, 'equal'
        return None
