import statistics

loops: int = 7
numbers = []

def isFloat(n):
    try:
        float(n)
        return True
    except ValueError:
        return False

for i in range(loops):
    num = input(f"[What is number {i+1}?] ")
    while not isFloat(num):
        print("[Please enter a number.]")
        num = input(f"[What is number {i+1}?] ")
    numbers.append(float(num))
    print(numbers[i])
avg = statistics.mean(numbers)
print(f'[The average of the {loops} numbers is {avg}.]')