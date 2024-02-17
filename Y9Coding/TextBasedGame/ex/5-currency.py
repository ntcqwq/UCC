import math
currency = ["United States Dollar", "Chinese Yuan", "Vietnamese Dong", "Turkish Lira", "Euro", "Brazilian Real", "Pound Sterling", "Japanese Yen", "Canadian Dollar"]
converter = [0.75, 5.27, 17782.65, 13.74, 0.75, 3.97, 0.66, 107.75, 1]
for type in range(len(currency)):
    print(f"{type+1}. {currency[type]}")
amount = input(f"[Please enter the amount of Canadian Dollars you want to convert.]\n")
second = input(f"[Please enter the number of the second currency.]\n")
print(f"{float(amount)} Canadian Dollars is {round(1*float(amount)*float(converter[int(second)-1]), 2)} {currency[int(second)-1]}")