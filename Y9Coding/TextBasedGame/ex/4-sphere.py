import math

def isFloat(n):
    try:
        float(n)
        return True
    except ValueError:
        return False

rad = input(f"[Please enter the radius of the sphere.]\n")
while not isFloat(rad):
    print("[Please enter a number.]\n")
    rad = float(input(f"[Please enter the radius of the sphere.]\n"))
print(f"The volume is {round(math.pi*(4/3)*float(rad)**3, 3)} cubic units")