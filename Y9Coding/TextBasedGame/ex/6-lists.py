from audioop import findfactor
from tkinter import Y


everything = {
    'name': ['Noah', 'SSnipro', 'iss', 'KnightNoah', 'Tairan', 'n_t_c'],
    'bday': '3/13',
    'friends': [],
    'ilike': {
        'sports': ['Soccer', 'Basketball', 'Tennis', 'Swimming', 'Ping Pong'],
        'food': ['Sushi', 'Rice', 'Lobsters', 'Crabs', 'Soup', 'Noodles'],
        'games': ['Minecraft', 'Genshin Impact', 'RoK', 'CoC', 'Clash Royale', '3D-Aim trainer'],
        'places': ['Beijing', 'Shanghai', 'ZJG', 'YJ', 'Montreal', 'Toronto', 'Hong Kong', 'Sydney'],
        'hobbies': ['Coding', 'Math', 'Drumming', 'Soccer'], 
        'numbers': range(6970)
    }
}

everything['friends'].extend(['none :)', 'everyone :)'])
print(f"Davis has {everything['ilike']['numbers'][-1]} girlfriends and I have {everything['friends'][0]}")
everything['friends'].remove('none :)')