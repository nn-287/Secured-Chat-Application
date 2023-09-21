from random import *
characters = "AABB09182736CCDD"
print(characters)
password =  "".join(choice(characters) for x in range(randint(8, 16)))
print(password)