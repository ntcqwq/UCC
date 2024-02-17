import math
print("""[How to calculate an equation:]

'+' to add         [Example: 1+1 -> 2]
'-' to subtract    [Example: 2-1 -> 1]
'*' to multiply    [Example: 4*4 -> 16]
'/' to divide      [Example: 16/4 -> 4]

'**' for exponents [Example: 3**2 -> 9]
'rt()' for roots   [Example: rt(16) -> 4]
'%' for remainders [Example: 5%2 -> 1]
""")

equation = input(f"[Please input an equation.]\n").replace("rt","math.sqrt")
rounding = int(input(f"[To how many decimal places do you want to round your answer to?]\n"))

print(round(eval(equation),rounding))