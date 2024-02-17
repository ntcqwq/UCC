# imports: 
#  * h_pct - external file, html-to-python character translator (original)
#  * random - python package
#  * curses - python package, allows windows to be created
#  * time - python package, timeit: timer extension
#  * textColor - external file, color data storage
#  * playsound - allows mp3 files to be played
#  * config - external file, json
#  * profanity - profanity filter
#  * sys - system, used for typewriter effect

from utility.hctp import pct
import random
import curses
import time
from timeit import default_timer as timer
from utility.textColor import textColors
from playsound import playsound
import utility.config as config
from better_profanity import profanity
import sys
import rich 

# var hs: json file where all the leaderboard user data is stored.
# var score: score of the user (refreshes after each attempt)
# var timeElapsed: time elapsed since start of the questions section
# var q: current question, if q = 100 -> question part = false

hs = config.CONFIG['leaderboard']
score = 0
timeElapsed = 0
q = 100

# func type: used for typewriter effect
def type(string):
    for char in string:
        time.sleep(0.02)
        sys.stdout.write(char)
        sys.stdout.flush()

def fasttype(string, speed):
    for char in string:
        time.sleep(speed)
        sys.stdout.write(char)
        sys.stdout.flush()

# func clear_page: used to clear terminal page
def clear_page():
    print("\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n")

# dict data: where all essential data to run the game is stored. Could potentially be separated into a .json file.
data = {
    # array cs: Correct sound effect random options 
    "cs": ["ding","nice"],
    # array ws: Wrong sound effect random options 
    "ws": ["cry","grrrrr","heheheha"],
    # array dialogue: Dialogue line data, each object in list is by line
    "dialogue": [
        [f'''"{textColors.LightBlue}{textColors.Bold}I'm jumping off the diving board today{textColors.ResetAll}{textColors.White}," Jabari told his dad.''', '''"Really?" said his dad.'''],
        [f'''The diving board is a bit scary, but Jabari had finished his {textColors.LightBlue}{textColors.Bold}swimming lessons and passed his swim test{textColors.ResetAll}{textColors.White}, and now he was ready to jump.''','''"I'm a great jumper," said Jabari, "so I'm not scared at all."'''],
        [f'''Jabari watched the other kids climb the long ladder. They walked all the way out to the end of the board, as big as tiny bugs. Then they stood on the edge. They spread their arms and bent their knees. And sprang up! up! up! And then they dove down, down, down.''', '''SPLASH!''', f'''{textColors.LightBlue}{textColors.Bold}"Looks easy," Jabari said.''', f'''But when his dad squeezed his hand. Jabari squeezed back.{textColors.ResetAll}{textColors.White}'''],
        ['''Jabari stood at the bottom of the ladder.''', '''"You can go before me if you want," he told the kid behind him.''', '''"I need to think about what kind of special jump I'm going to do."''', '''Jabari thought and thought.'''],
        ['''Jabari started to climb. Up and up. This ladder is very tall, he thought.''', '''"Are you okay?" called his dad.''', '''"I'm just a little tired," said Jabari.''', '''"Maybe you should climb down and take a tiny rest," said his dad.''', '''A tiny rest sounded like a good idea.'''],
        [f'''When he got to the bottom, Jabari remembered something. "{textColors.LightBlue}{textColors.Bold}I forgot to do my stretches!{textColors.ResetAll}{textColors.White}" he said to his dad.''', '''"Stretching is very important," said his dad.''', '''"I think tomorrow might be a better day for jumping," Jabari said.''', '''They looked up at the diving board together.'''],
        [f'''{textColors.LightBlue}{textColors.Bold}"It's okay to feel a little scared" said his dad. "Sometimes, if I feel a little scared, I take a deep breath and tell myself I am ready. And you know what? Sometimes it stops feeling scary and feels a little like a surprise.{textColors.ResetAll}{textColors.White}"''', '''Jabari loved surprises.'''],
        ['''Jabari took a deep breath and felt it fill his body from the ends of his hair right down to the tips of his toes.''','''Jabari looked up. He began to climb.''', '''Up and up. And up and up.''', '''Until he got to the top. Jabari stood up straight.''', '''He walked all the way to the end of the board.'''],
        ['''His toes curled around the rough edge.'''],
        ['''Jabari looked out, as far as he could see. He felt like he was ready.''', '''"I love surprises," he whispered.'''],
        ['''He took a deep breath and spread his arms and bent his knees.''', '''Then he sprang up!''', '''Up off the board!''', '''Flying!'''],
        ['''Jabari hit the water with a SPLASH!'''],
        ['''Down,''','''down,''','''down he went.''','''And then back up!''','''WHOOSH'''],
        ['''"Jabari! You did it!" said his dad.''','''"I did it!" said Jabari. "I'm a great jumper! And you know what?"''', '''"What?" said his dad.'''],
        ['''"Surprise double backflip is next!"''']
    ],
    # array questions: Question part data
    "questions": [
        "Looking at the cover, who is the author of the book?", 
        "What is the setting of the story?", 
        "What will Jabari be doing?",
        "What does Jabari think about jumping down the diving board initially, and why was he confident?", 
        "Who is Jabari with?",
        "Just as Jabari was about to jump off the diving board, he forgets to do something. What did Jabari forget to do?",
        "Who encourages Jabari?",
        "What is the advice Jabari's dad give Jabari?",
        "In this book, what qualities does Jabari show?",
        "How does Jabari's perspective of jumping off the diving board change?",
        "Find at least 2 signs of Jabari being nervous.",
        """Here are the 17 UN goals. Which of the 17 UN goals connect most to this book?"""
        ],
    # array type: Type data stored in format: [Question type (optional image), question value]
    "type": [
        ["Multiple Choice image_question_1.html",100], 
        ["Multiple Choice",100], 
        ["Multiple Choice",100],
        ["Short Answer",300],
        ["Multiple Choice",100],
        ["Multiple Choice",100],
        ["Multiple Choice",100],
        ["Multiple Choice,",200],
        ["Short Answer",400],
        ["Short Answer",500],
        ["Short Answer",300],
        ["UN", 1000]
        ],
    # array answers: If question type multiple choice, stored format [a,b,c], if empty -> not multiple choice
    "answers": [
        ["Jabari","Gaia Cornwall","David Shannon"],
        ["A park", "Jabari's home", "A swimming pool"],
        ["Playing with his sister", "Swimming with his dad", "Jumping off a diving board"],
        [],
        ["His dad and his sister","His dad","His dad and his mother"],
        ["He forgets to stretch","He forgets to hug his sister","He forgets how to jump"],
        ["His mother", "His dad", "His sister"],
        ['''"Sometimes, if I feel a little scared, I take a deep breath and tell myself I am ready. And you know what? Sometimes it stops feeling scary and feels a little like a surprise."''','''"Stretching is very important,"''','''"Are you okay?"'''],
        [],
        [],
        [],
        [],
        ],
    # array answer: Correct answer list
    "answer": ["b","c","c",["test", "lesson","easy"],"a","a","b","a",["bravery", "courage", "risk", "confiden"],["nervous", "scared","confiden","encourage", "dad"],["front","excuse","behind","squeeze","rest","think"],["6","9","4"]],
    # array result: Stored user input result 
    "result": []
}


def welcome():
    # Welcome to the game ASCII art
    fasttype(pct("hctp_images/welcome.html"),0.000005)
    # Conditional input value skip
    skip = input(f"{textColors.Bold}                                                       Press S to skip walkthrough | Press anything else to start the story walkthrough{textColors.ResetAll}     ")
    if skip.lower() == "s":
        questions()
    else:
       walkthrough()


def walkthrough():
    # Dialogue function
    def dialogue():
        for lines in range(len(data["dialogue"])):
            clear_page()
            for line in data["dialogue"][lines]:
                # Each page
                type(line)
                print("\n")
                time.sleep(2)
            try:
                # Image corresponding to each page (if there is an image, if error -> pass)
                print("\n\n")
                print(pct(f"hctp_images/walkthrough/{lines+1}.html"))
                time.sleep(5)
            except:
                pass

    type(f"{textColors.White}\n\n\n\n\nHere is a brief walkthrough of Jabari Jumps! (Tip: Pay attention to the {textColors.LightBlue}{textColors.Bold}BLUE{textColors.ResetAll}{textColors.White} text!)")
    time.sleep(1)
    # Cover page
    print("\n")
    fasttype(pct("hctp_images/walkthrough/cover.html"),0.000005)
    time.sleep(5)
    dialogue()
    clear_page()
    # After walkthrough ends, question part commences
    print(pct("hctp_images/q.html"))
    time.sleep(5)
    questions()
    


def questions():
    # Timer starts
    start = timer()
    clear_page()
    # Cover page w/ author name, again
    fasttype(pct("hctp_images/q1.html"),0.00001)
    time.sleep(5)
    # global vars, they will be used for tracking in this section
    global q
    global score
    global timeElapsed
    # var firstTry: The player will get bonus points if they got the correct answer first try. Will refresh every single q.
    # var wrongCounter: The player will reduce points for each answer they get wrong for every single q. (Formula: question value / wrongCounter + 1)
    firstTry = True
    wrongCounter = 0
    # Python curses Window created, along with 4 color pairs with background color, since textColor.py cannot be used while using curses.
    stdscr = curses.initscr()
    curses.start_color()
    curses.init_pair(1, curses.COLOR_WHITE, curses.COLOR_BLACK)
    curses.init_pair(2, curses.COLOR_GREEN, curses.COLOR_BLACK)
    curses.init_pair(3, curses.COLOR_RED, curses.COLOR_BLACK)
    curses.init_pair(4, curses.COLOR_MAGENTA, curses.COLOR_BLACK)
    stdscr.bkgd(' ', curses.color_pair(1))
    # q = 0, questions begin
    q = 0
    # win title_win: Window that will display the title as well as the answer options (if Multiple Choice), resizes conditionally using ternary operation
    title_win = curses.newwin(25 if "UN" in data['type'][q][0] else 12, 260, 2, 5)
    # while loop until questions end
    while q < len(data["questions"]):
        # win input_win: Window that will display user input (responses), resizes conditionally using ternary operation
        input_win = curses.newwin(3 if "Multiple Choice" in data['type'][q][0] or "UN" in data['type'][q][0] else 5, 18 if "Multiple Choice" in data['type'][q][0] or "UN" in data['type'][q][0] else 180, 20 if "UN" in data['type'][q][0] else 10, 3)
        # func incorrectFlash(): text-based flash if user gets an incorrect answer 
        def incorrectFlash():
            global firstTry
            firstTry = False
            try_again = """████████╗██████╗ ██╗   ██╗     █████╗  ██████╗  █████╗ ██╗███╗   ██╗██╗
╚══██╔══╝██╔══██╗╚██╗ ██╔╝    ██╔══██╗██╔════╝ ██╔══██╗██║████╗  ██║██║
   ██║   ██████╔╝ ╚████╔╝     ███████║██║  ███╗███████║██║██╔██╗ ██║██║
   ██║   ██╔══██╗  ╚██╔╝      ██╔══██║██║   ██║██╔══██║██║██║╚██╗██║╚═╝
   ██║   ██║  ██║   ██║       ██║  ██║╚██████╔╝██║  ██║██║██║ ╚████║██╗
   ╚═╝   ╚═╝  ╚═╝   ╚═╝       ╚═╝  ╚═╝ ╚═════╝ ╚═╝  ╚═╝╚═╝╚═╝  ╚═══╝╚═╝"""
            title_win.addstr(0,0, try_again, curses.color_pair(3))
            title_win.refresh()
            time.sleep(0.1)
            title_win.addstr(0,0, try_again, curses.color_pair(4))
            title_win.refresh()
            time.sleep(0.1)
            title_win.addstr(0,0, try_again, curses.A_BLINK)
            title_win.refresh()
            time.sleep(0.1)
            title_win.addstr(0,0, try_again, curses.color_pair(3))
            title_win.refresh()
            time.sleep(0.1)
            title_win.addstr(0,0, try_again, curses.color_pair(4))
            title_win.refresh()
            time.sleep(0.1)
            title_win.addstr(0,0, try_again, curses.color_pair(3))
            title_win.refresh()
            # This line is added because python curses is very sensitive, even when the windows end it will still count user input, therefore this line prevents this from happening when the game ends.
            if q != 100:
                playsound(f'mp3/Wrong Sounds/{random.choice(data["ws"])}.mp3')
            
        # func correctFlash(): text-based flash if user gets an correct answer 
        def correctFlash():
            title_win.addstr(0, 0, """████████╗██╗  ██╗ █████╗ ████████╗███████╗    ██████╗ ██╗ ██████╗ ██╗  ██╗████████╗██╗
╚══██╔══╝██║  ██║██╔══██╗╚══██╔══╝██╔════╝    ██╔══██╗██║██╔════╝ ██║  ██║╚══██╔══╝██║
   ██║   ███████║███████║   ██║   ███████╗    ██████╔╝██║██║  ███╗███████║   ██║   ██║
   ██║   ██╔══██║██╔══██║   ██║   ╚════██║    ██╔══██╗██║██║   ██║██╔══██║   ██║   ╚═╝
   ██║   ██║  ██║██║  ██║   ██║   ███████║    ██║  ██║██║╚██████╔╝██║  ██║   ██║   ██╗
   ╚═╝   ╚═╝  ╚═╝╚═╝  ╚═╝   ╚═╝   ╚══════╝    ╚═╝  ╚═╝╚═╝ ╚═════╝ ╚═╝  ╚═╝   ╚═╝   ╚═╝""", curses.color_pair(2))
            title_win.refresh()
            playsound(f'mp3/Correct Sounds/{random.choice(data["cs"])}.mp3')

        # Re-add the border of the windows
        stdscr.border()
        input_win.border()

        # var pointGrammar: this variable is not really used anymore, since all my question values are now above 100, but I would still like to keep it since it is not completely a waste.
        pointGrammar = "point" if data['type'][q][1] == 1 else "points"
        # title_win adds question, question value and description.
        title_win.addstr(1, 0, f"{q+1}. {data['questions'][q]} ({data['type'][q][1]} {pointGrammar})", curses.A_BOLD)
        if "Multiple Choice" in data['type'][q][0]:
            title_win.addstr(3, 0, f"A. {data['answers'][q][0]}\nB. {data['answers'][q][1]}\nC. {data['answers'][q][2]}")
        elif "Short Answer" in data['type'][q][0]:
            pass
        elif "UN" in data['type'][q][0]:    
            title_win.addstr(3, 0, f"GOAL 1: No Poverty\nGOAL 3: Good Health and Well-being\nGOAL 5: Gender Equality\nGOAL 7: Affordable and Clean Energy\nGOAL 9: Industry, Innovation and Infrastructure\nGOAL 11: Sustainable Cities and Communities\nGOAL 13: Climate Action\nGOAL 15: Life on Land\nGOAL 17: Partnerships to achieve the Goal")
            array = ["GOAL 2: Zero Hunger","GOAL 4: Quality Education","GOAL 6: Clean Water and Sanitation","GOAL 8: Decent Work and Economic Growth","GOAL 10: Reduced Inequality","GOAL 12: Responsible Consumption and Production","GOAL 14: Life Below Water","GOAL 16: Peace and Justice Strong Institutions"]
            for i in range(8):
                title_win.addstr(i+3, 50, array[i])
        # refreshing the window
        stdscr.refresh()
        title_win.refresh()

        # If statements, depending on the type of question, the code will react differently.
        if "Multiple Choice" in data['type'][q][0]:
            input_win.addstr(1, 1, "Your answer: ", curses.A_BOLD)
            answer = input_win.getkey()
            input_win.addstr(1, 17, answer)
            # If the user trolls
            while not answer.lower() in ["a","b","c"]: 
                input_win.clear()
                input_win.border()
                input_win.addstr(1, 1, "Your answer: ", curses.A_BOLD)
                answer = input_win.getkey()
                input_win.refresh()
            stdscr.clear()
            stdscr.refresh()
            # If the user gets an incorrect answer
            if answer.lower() != data['answer'][q]:
                incorrectFlash()
                wrongCounter += 1
            # If the user gets a correct answer
            elif answer.lower() == data['answer'][q]:
                correctFlash()
                if firstTry == True and wrongCounter == 0:
                    # result storage system
                    data["result"].append("1!")
                else: 
                    data["result"].append(f"{wrongCounter}")
                # resets vars, next question
                firstTry = True
                wrongCounter = 0
                q += 1
        elif "Short Answer" in data['type'][q][0]:
            # var goodCounter: the amount of keywords the user got right
            goodCounter = 0
            input_win.addstr(1, 1, "Your answer: ", curses.A_BOLD)
            input_win.refresh()
            # when the user types enter, user input ends, since input() cannot be used in curses.
            answer = input_win.getstr(1, 14, 175)
            stdscr.clear()
            stdscr.refresh()
            # counting goodCounter
            for each in range(len(data['answer'][q])):
                if data['answer'][q][each] in str(answer.lower().decode("utf-8")):
                    goodCounter += 1
            # if user got at least one right, counted as correct
            if goodCounter >= 1:
                correctFlash()
                if firstTry == True and wrongCounter == 0:
                    # goodCounter acts as a multiplier to the score for this q
                    data["result"].append(f"1!,{goodCounter}")
                else: 
                    data["result"].append(f"{wrongCounter},{goodCounter}")
                firstTry = True
                wrongCounter = 0
                q += 1
            elif goodCounter == 0:
                incorrectFlash()
                wrongCounter += 1
                time.sleep(1)
        elif "UN" in data['type'][q][0]:
            input_win.addstr(1, 1, "Your answer: ", curses.A_BOLD)
            input_win.refresh()
            answer = input_win.getstr(1, 14, 175)
            stdscr.clear()
            stdscr.refresh()
            # Since UN is a special type of question, and there are only one type of questions like this, we can be less flexible for the code.
            if str(answer.lower().decode("utf-8")) in ["6","9","4"]:
                correctFlash()
                if firstTry == True and wrongCounter == 0:
                    data["result"].append(f"1!")
                else: 
                    data["result"].append(f"{wrongCounter}")
                firstTry = True
                wrongCounter = 0
                q += 1
            else:
                incorrectFlash()
                wrongCounter += 1
                time.sleep(1)
    if q == len(data["questions"]):
        # Timer ends, counts time
        end = timer()
        timeElapsed = round(end-start,2)
        stdscr.clear()
        stdscr.refresh()
        title_win.addstr(0,0, "Your results:", curses.A_BOLD)
        title_win.refresh()
        playsound("mp3/Other/drumroll.mp3") 
        # Calculations of score percentage
        maxscore = 0
        for i in data["type"]:
            maxscore += float(i[1])
        for i in range(len(data["result"])):
            if "1!" in data["result"][i]:
                if "," in data["result"][i]:
                    score += float(100 * int(data["result"][i].split(",")[1]))
                else:
                    score += data["type"][i][1]
            else: 
                if "," in data["result"][i]:
                    score += round(float(data["type"][i][1]/(float(int(data["result"][i].split(",")[0])+1))) * int(data["result"][i].split(",")[0]), 2)
                else:
                    score += round(float(data["type"][i][1]/float((int(data["result"][i])))), 2)
        # Obtaining the score, and sends the user back the results.
        score = round(score,2)
        title_win.addstr(2,0, f"{score} / {maxscore} ({round((score/maxscore) * 100, 2)}%!) in {timeElapsed} seconds! 👑\n\n")
        title_win.refresh()
        # Questions part end, curses window terminated
        q = 100
        playsound("mp3/Other/clap.mp3")
        curses.endwin()
        # next section, leaderboards
        highscoreSystem()

def highscoreSystem():
    print(f"{textColors.White}{textColors.Bold}")
    clear_page()
    # Profanity censor to censor out any "naughty" names
    name = profanity.censor(input("What is your name?\n"))
    type(f"Hi {name}!\n")
    time.sleep(1)
    type("Your high score will be recorded, as long as the json file does not get deleted!\n\n")
    hs.append([name,score,timeElapsed])
    # load json config
    config.CONFIG['leaderboard'] = hs 
    config.save_config()
    time.sleep(1)
    type("Current Leaderboards:\n")
    time.sleep(0.5)
    # Sort the rankings of the players by score then time
    def sort_key1(h):
        return h[2]
    def sort_key2(h):
        return h[1]
    hs.sort(key=sort_key1, reverse=False)
    hs.sort(key=sort_key2, reverse=True)
    # print out the leaderboards
    for s in range(len(hs)):
        color = textColors.Yellow if s == 0 else textColors.LightGreen if s == 1 else textColors.LightBlue if s == 2 else textColors.White
        print(f"{color}{s+1}. {hs[s][0]}: {hs[s][1]} points (⏱ {hs[s][2]}s)")
        time.sleep(0.25)
    time.sleep(3)
    print(f"{textColors.White}{textColors.Bold}{clear_page()}")
    clear_page()
    # end, thanks for playing!


welcome()
print(pct('hctp_images/thanks.html'))
rich.print("""[link=https://docs.google.com/forms/d/e/1FAIpQLSf05T93PRvFXamRgehGHw15VKl8rcHIGyI68dcbOlvHci26ew/viewform?usp=sf_link]Feedback form[/link]!""")