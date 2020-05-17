#!/usr/bin/python3
import sys

accounts_database = {"bob": "123", "ann": "pass123", "mike": "password123", "liz": "pass123"}

print("*" * 60,
"""
Hello and welcome to: 
TEXT ANALYZER  Version 1.0.0
""",
"*" * 60)

print("""PRESS ENTER IF YOU ARE REGISTERED USER.
If you wish to register type any key.
If you wish to end program type "No" """)

registration = input("")

if registration in ["No", "no"]:
    print("Program is shutting down.")
    sys.exit()

if registration != "":
    while registration:
        new_name = input("New name: ")
        new_password = input("New password: ")
        if new_name in accounts_database:
            print("This account name is already taken!")
        else:
            accounts_database[new_name] = new_password
            registration = False

# Number of attempts for login
attempts = 3

# Login loop
print("="*60)
print("Please enter your login information")
while attempts:
    user_name = input("Please enter your acc name: ")
    user_password = input("Please enter your password: ")

    if accounts_database.get(user_name) == user_password:
        break
    else:
        attempts -= 1
        print("=" * 60)
        print("ERROR: Your login or password is incorrect, you have", attempts, "attempts remaining.")

# Login execution
if not attempts:
    print("""
You ran out of attempts.
Program is shutting down!
    """)
    sys.exit()
else:
    print("=" * 60)
    print(" ")
    print("Welcome", user_name, "!")

# Text analysis phase
TEXTS = ['''
Situated about 10 miles west of Kemmerer, 
Fossil Butte is a ruggedly impressive 
topographic feature that rises sharply 
some 1000 feet above Twin Creek Valley 
to an elevation of more than 7500 feet 
above sea level. The butte is located just 
north of US 30N and the Union Pacific Railroad, 
which traverse the valley. ''',

'''At the base of Fossil Butte are the bright 
red, purple, yellow and gray beds of the Wasatch 
Formation. Eroded portions of these horizontal 
beds slope gradually upward from the valley floor 
and steepen abruptly. Overlying them and extending 
to the top of the butte are the much steeper 
buff-to-white beds of the Green River Formation, 
which are about 300 feet thick.''',

'''The monument contains 8198 acres and protects 
a portion of the largest deposit of freshwater fish 
fossils in the world. The richest fossil fish deposits 
are found in multiple limestone layers, which lie some 
100 feet below the top of the butte. The fossils 
represent several varieties of perch, as well as 
other freshwater genera and herring similar to those 
in modern oceans. Other fish such as paddlefish, 
garpike and stingray are also present.'''
]

# User choice from TEXTS list
print("We have", len(TEXTS), "texts to be analyzed.")

user_selection = True
while user_selection:
    print("PLEASE TYPE ANY NUMBER FROM RANGE 1 TO", len(TEXTS), "TO SELECT THE TEXT")
    print("If you wish to add additional text press enter.")
    user_selection = input("SELECT: ")
    if user_selection == "No" or user_selection == "no":
        print("Thank you for using TEXT ANALYZER")
        sys.exit()
    elif user_selection == "":
        new_text = input("Paste new text: ")
        TEXTS.append(new_text)
        user_selection = True
    elif int(user_selection) not in range(1, len(TEXTS) + 1):
        print("""Please select from range 1-3!
(if you want to end program type "No")""")
        print("")
    elif int(user_selection) in range(1, len(TEXTS) + 1):
        break

chosen_text = TEXTS[int(user_selection)-1]
print("")
print("Your chosen text is:")
print(chosen_text)

# Conversion of string into compatible list
chosen_text = chosen_text.replace(".", "").replace(",", "").replace("\n", "").strip(" ").split()

# Number of words in total
# Number of words starting with capital letter
# Number of uppercase words
# Number of lowercase words
# Number of numeric-only words (e.q. 100 not 100N)
count_total = len(chosen_text)
count_words = 0
count_titlecased = 0
count_uppercased = 0
count_lowercased = 0
count_numeric = 0
index = 0
summ_of_numbers = 0
# Loop for counting of different words
while index < count_total:
    if chosen_text[index].isupper():
        count_uppercased += 1
        count_titlecased += 1
        index += 1
        count_words += 1

    elif chosen_text[index].istitle():
        count_titlecased += 1
        index += 1
        count_words += 1

    elif chosen_text[index].islower():
        count_lowercased += 1
        index += 1
        count_words += 1

    elif chosen_text[index].isalnum():
        count_numeric += 1
        summ_of_numbers = summ_of_numbers + int(chosen_text[index])
        index += 1
        count_words += 1
    else:
        index += 1


# Print of the text attributes
print("-" * 60)
print("There are", count_words, "words in the selected text")
print("There are", count_titlecased, "titlecase words")
print("There are", count_uppercased, "uppercase words")
print("There are", count_lowercased, "lowercase words")
print("There are", count_numeric, "numeric strings")
print("-" * 60)

# Create a bar chart depicting the frequencies of word lengths in the text. For example:
print("FREQUENCIES OF WORD LENGTH")
length_database = {}
while chosen_text:
    word = chosen_text.pop()
    lenght = len(word)
    if lenght in list(length_database.keys()):
        length_database[lenght].append(word)
    else:
        length_database[lenght] = [word]

sort = sorted(length_database.keys())

while sort:
    key = sort.pop(0)
    length_words = len(length_database[key])
    if len(str(key)) == 1:
        print(key, " " + "□" * len(length_database[key]), len(length_database[key]))
    else:
        print(key, "□" * len(length_database[key]), len(length_database[key]))

# Calculate the sum of all the numeric "words" in the given text. For example the sum for the string below would be 8500
if count_numeric > 0:
    print("-" * 60)
    print("If we summed all the numbers in this text we would get:", summ_of_numbers)
else:
    print("-" * 60)
    print("There are no numbers in provided text. Thus there is no total number calculation.")