import math
import utils.isfloat
rad = input(f"[Please enter the radius of the circle.]\n")
while not utils.isfloat.isFloat(rad):
    print("[Please enter a number.]\n")
    rad = input(f"[Please enter the radius of the circle.] ")
print(f"The area is {round(math.pi*int(rad)**2, 2)}")