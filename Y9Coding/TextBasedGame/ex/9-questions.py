data = {
    "questions": ["What is your favorite color in the above", "What is your favorite fruit", "What is your favorite chess opening"],
    "type": ["Multiple Choice", "Short Answer", "Multiple Choice"],
    "answers": [["Blue","Red","Green"],"",["Halloween Gambit", "eq", "eafga"]],
    "answer": ["Blue",False,"Halloween Gambit"]
}

for i in range(len(data["questions"])):
    if data["type"][i] == "Multiple Choice":
        for each in data["answers"][i]:
            print(each)
        answer = input(f'{data["questions"][i]}?\n')
        if answer == data["answer"][i]:
            print("Correct!\n========")
    elif data["type"][i] == "Short Answer":
        answer = input(f'{data["questions"][i]}?\n')
        if data["answer"][i] == False:
            print("Great answer!")


