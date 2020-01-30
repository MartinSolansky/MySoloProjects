import random
import time


def main():
    global name
    global guess_number
    global TIME
    print("WELCOME TO BULLS AND COWS GAME!!!")
    name = input("Please enter your name: ")
    print(
f"""Hi {name}!
I've generated a random 4 digit number for you.
Let's play a bulls and cows game.""")
    TEMPLATE = generate_number()
    print(TEMPLATE)
    start_time = time.time()
    user_guess = guess()
    guess_number = 1
    while guess_number:
        result = game_cycle(TEMPLATE, user_guess)
        if result == 4:
            end_time = time.time()
            TIME = time_taken(start_time, end_time)
            print(f"\nCorrect, you've guessed the right number in {guess_number} guesses with time {TIME} !")
            print(f"That's {valuation(guess_number)}!")
            single_attempt = create_single_attempt()
            result_recording(str(guess_number), single_attempt)
            print("You have been placed in {}. rank.\n".format(get_rank(create_single_attempt())))
            break
        else:
            user_guess = guess()
            guess_number += 1

    chart_plotting = input("Do you want to see TOP 10 chart?\nYes/No\n")
    while True:
        if chart_plotting.lower() == "yes":
            print_chart()
            break
        elif chart_plotting.lower() == "no":
            print("Thats all!\nI hope you have fun!")
            break
        else:
            print(f"Are you sure? '{chart_plotting}' is no valid option!")


def generate_number():
    number = ""
    for i in range(4):
        repeat = True
        while repeat:
            digit = str(random.randint(1,9))
            if digit in number:
                repeat = True
            else:
                number += digit
                repeat = False
    return number


def guess():
    print("Enter a number")
    wrong_guess = True
    while wrong_guess:
        guess_number = input()
        if len(guess_number) == 4:
            return guess_number
        else:
            print("Wrong guess! \nPlease guess again.")


def game_cycle(template: str, user_guess: str):
    bulls = 0
    cows = 0
    for i_guess, digit in enumerate(user_guess):
        if digit in template and i_guess == template.index(digit):
            bulls += 1
        elif  digit in template:
            cows += 1
    print(f"{bulls} bulls, {cows} cows")
    return bulls

def valuation(guess_number):
    valuation_possibilities = {"amazing": range(1, 5),
                               "quite good": range(5, 15),
                               "not so good": range(15, 25),
                               "really bad": range(150000)}
    for valuation_rank in valuation_possibilities:
        if guess_number in valuation_possibilities[valuation_rank]:
            return valuation_rank

def create_single_attempt():
    attempt = {"name": name, "attempts": guess_number, "time": TIME, "valuation": valuation(guess_number)}
    return attempt

def result_recording(attempts: str, single_attempt: dict):
    with open("bull_and_cow_records.txt",
              "r+") as file:
        records_dictionary = file.read()
        if not records_dictionary:
            records_dictionary = {}
        else:
            records_dictionary = eval(records_dictionary)

        if attempts not in records_dictionary.keys():
            records_dictionary[f"{attempts}"] = single_attempt
        else:
            to_merge = records_dictionary.get(f"{attempts}")
            if type(to_merge) == dict:
                to_merge = (to_merge, single_attempt)
                records_dictionary[f"{attempts}"] = to_merge
            elif type(to_merge) == list:
                to_merge.append(single_attempt)
        file.seek(0)
        file.write(f"{records_dictionary}")
        print("Your game has been recorded to local ranking......")


def time_taken(start_time, end_time):
    timer = end_time - start_time
    minutes, seconds = divmod(timer, 60)
    return "{}:{:} ".format(int(minutes), int(seconds))


def print_chart():
    with open("bull_and_cow_records.txt",
              "r") as file:
        text = eval(file.read())
        order = sorted(list(text.keys()))
        rank = 1
        header = "{}|{:^10}|{:^10}|{:^10}|{:^11}|\n".format("RANK", "NAME", "ATTEMPTS", "TIME", "VALUATION")
        print(header + ("-" * (len(header) - 2)))
        while rank < 10:
            for attempts in order:
                user_attempt = text.get(attempts)
                if type(user_attempt) == tuple:
                    for real_attempt in user_attempt:
                        user_attempt = real_attempt
                        row = "{:>3}.|{name:^10.8}|{attempts:^10}|{time:^10}|{valuation:>11}|".format(rank, **user_attempt)
                        rank += 1
                        print(row)
                else:
                    row = "{:>3}.|{name:^10.8}|{attempts:^10}|{time:^10}|{valuation:>11}|".format(rank, **user_attempt)
                    rank += 1
                    print(row)
            return


def get_rank(attempt: dict):
    with open("bull_and_cow_records.txt",
              "r") as file:
        text = eval(file.read())
        order = sorted(list(text.keys()))
        rank = 0
        for attempts in order:
            user_attempt = text.get(attempts)
            if type(user_attempt) == tuple:
                for real_attempt in user_attempt:
                    user_attempt = real_attempt
                    rank += 1
            else:
                rank += 1
            if user_attempt == attempt:
                return rank
            else:
                return rank

main()