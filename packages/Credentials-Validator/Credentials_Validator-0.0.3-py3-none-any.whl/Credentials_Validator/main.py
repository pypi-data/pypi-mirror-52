from Validators import PasswordValidator

user = PasswordValidator([4, 10], [1], [2], [0], [1], username='PasswOrd!')

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
