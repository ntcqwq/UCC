import math
currency = ["Adult Ticket", "Elderly Ticket", "Kids Ticket"]
converter = [10,5,5]
for type in range(len(currency)):
    print(f"{type+1}. {currency[type]}")
amount = int(input(f"[Please enter the number of the ticket you want to buy.]\n"))
second = int(input(f"[Please enter the number of the that ticket you want to buy.]\n"))
print(f"{second*converter[amount-1]}")