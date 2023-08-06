import os
from specialless.specialless import Revertable

my_special_string = ">£#$½¾{()€ª¶[]]}`````''''''$$$$$$"
print(my_special_string)
not_so_special = Revertable.convert(my_special_string)
print(not_so_special)
special_again = Revertable.revert(not_so_special)
print(special_again)


# example use case
print(Revertable.convert(os.path.abspath(os.path.curdir)))
