#Account credentials checker

This package takes care of verifing the credentials serverside.

##Download
You can pip install by
```commandline
pip3 install Credentials-Validator
```

##Usage

You can import the pakage by typing

```python
from Credentials_Validator import UsernameValidator, PasswordValidator
```
\
The general use is:

```python
from Credentials_Validator import UsernameValidator

user = UsernameValidator([4], #length
                         [1], #lower-case chars range
                         [1], #upper-case chars range
                         [1,3], #numbers range
                         [0,0], #symbols range
                         )
```
\
The use of range is:

```python
[2, 5] # minimum 2, maximum 5 characters
[1] # at least one
[0] # not necessary, not denied
[0, 4] # not necessary, maximum 5 characters
[0, 0] # denied
```

###Validation
In order to validate a `text` (Username or password) you have to call the method `Validator.verify(text)`\
It returns two objects:
1. a `boolean` (`True` if the text is valid, `False` if there is one or more errors)
2. a `string`, that can be:
    * `''` empty, if there are no errors
    * `'length'` if the `text` is too short or too long
    * `'lower'` if there are too few or too many lower-case characters
    * `'upper'` if there are too few or too many upper-case characters
    * `'digit'` if there are too few or too many numbers
    * `'symbols'` if there are too few or too many allowed symbols
```python
from Credentials_Validator import UsernameValidator

user = UsernameValidator([4, 10], [1], [2], [0], [1],)

is_valid, error = user.verify('PasswOrd!')
print((is_valid, error))
#returns (True, '')

is_valid, error = user.verify('PasswOrd3')
print((is_valid, error))
#returns (False, 'symbols')

is_valid, error = user.verify('Password!')
print((is_valid, error))
#returns (False, 'upper')

is_valid, error = user.verify('th1sPasswOrdist00long')
print((is_valid, error))
#returns (False, 'length')
```

###Customization
\
The default symbols are: `!"#$%&'()*+,-./:;<=>?@[\]^_{|}~`\
\
You can customize the simbols by adding your custom list (string):

```python
from Credentials_Validator import UsernameValidator

my_symbols = '!?$%&@#'

user = UsernameValidator([4, 10], [1], [1], [0], [1], symbols_list=my_symbols)
```
