import json
import random

letters_guessed_already = []
yellow_letters = []
green_letters = []


def load_word_list(file_name):
    f = open(file_name)
    wl = json.load(f)["word_list"]
    f.close()
    return wl


master_word_list = load_word_list("word_list.json")
word = random.choice(master_word_list)


def play():

    global letters_guessed_already
    global yellow_letters
    global green_letters
    global word

    for game in range(6):
        valid_guess = False
        guess = ""
        while not valid_guess:
            guess = input("Guess a valid 5 letter word: ").lower()
            if len(guess) != 5:
                print("Not a valid word, try again!")
                continue
            elif guess not in master_word_list:
                print("Not a valid word, try again!")
                continue
            elif guess == word:
                valid_guess = True
                break
            else:
                valid_guess = True
                break

        result = []
        str_rep = ""
        for i, letter in enumerate(guess):
            if letter != word[i] and letter not in word:
                result.append('b')
                str_rep += letter + ' ' + 'b' + ' '
                if letter not in letters_guessed_already:
                    letters_guessed_already.append(letter)
            elif letter != word[i] and letter in word:
                result.append('y')
                str_rep += letter + ' ' + 'y' + ' '
                if letter not in yellow_letters:
                    yellow_letters.append(letter)
            if letter == word[i]:
                result.append('g')
                str_rep += letter + ' ' + 'g' + ' '
                if letter in yellow_letters:
                    yellow_letters.remove(letter)
                if letter not in green_letters:
                    green_letters.append(letter)

        str_rep = str_rep[:-1]
        # print(list(guess))
        # print(result)
        print(str_rep)
        if word == guess:
            print()
            print("Game Won! Congratulations!!!!!!")
            exit(0)
        # print(letters_guessed_already)
        # print(yellow_letters)
        # print(green_letters)


total_turns = 0
result_total = ""


def play_guess(guess="irate"):
    global total_turns
    global result_total

    valid_guess = False
    total_turns += 1
    while not valid_guess:
        # if guess == "irate":
        #     guess = input("Guess a valid 5 letter word: ").lower()
        if len(guess) != 5:
            print("Not a valid word, try again!")
            continue
        elif guess not in master_word_list:
            print("Not a valid word, try again!")
            continue
        elif guess == word:
            valid_guess = True
            break
        else:
            valid_guess = True
            break

    result = []
    str_rep = ""
    for i, letter in enumerate(guess):
        if letter != word[i] and letter not in word:
            result.append('b')
            str_rep += letter + ' ' + 'b' + ' '
            if letter not in letters_guessed_already:
                letters_guessed_already.append(letter)
        elif letter != word[i] and letter in word:
            result.append('y')
            str_rep += letter + ' ' + 'y' + ' '
            if letter not in yellow_letters:
                yellow_letters.append(letter)
        if letter == word[i]:
            result.append('g')
            str_rep += letter + ' ' + 'g' + ' '
            if letter in yellow_letters:
                yellow_letters.remove(letter)
            if letter not in green_letters:
                green_letters.append(letter)

    str_rep = str_rep[:-1]
    result_total += str_rep + ', '
    # print(str_rep)
    if word == guess:
        # print()
        # print("word: " + word)
        # print("Game Won! Congratulations!!!!!!")
        result_total = result_total[:-2]
        result_total = str(total_turns) + ", " + result_total
        print(result_total)
        exit(0)
    # elif total_turns == 6:
    #     result_total = result_total[:-2]
    #     result_total = "-1, " + result_total
    #     print(result_total)
    #     exit(1)
    return str_rep
