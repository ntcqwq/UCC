name = input("[What's your name?] ")
while name.replace(" ", "").replace("   ", "") == "":
    name = input("[What's your name? Please don't enter the status of your father that went to get milk and never came back!] ")
age: int = -1
print(f'Nice to meet you {name}!')
year: int = input("[What year were you born?] ")
while age == -1:
    try: 
        if 2022 - int(year) <= 0:
            year: int = input("[You can't be 0 years old or born in the future!] ")
        elif 2022 - int(year) >= 200:
            year: int = input("[Either you have broken a world record for oldest person alive or you're trolling!] ")
        else:
            age = 2022 - int(year)  
    except: 
        year: int = input("[What year were you born you clown? You think you're so funny? Enter a number!] ")
print(f'[You are {str(age)} years old, {name}!]')