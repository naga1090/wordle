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

for game in range(6):
    valid_guess = False
    guess = ""
    while not valid_guess:
        guess = input("Guess a valid 5 letter word: ").lower()
        if len(guess) != 5:
            print("Not a valid word, try again!")
            continue
        if guess not in master_word_list:
            print("Not a valid word, try again!")
            continue
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
    # print(letters_guessed_already)
    # print(yellow_letters)
    # print(green_letters)
