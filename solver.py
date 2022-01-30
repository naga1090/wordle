import json
import math


def load_word_list(file_name):
    f = open(file_name)
    wl = json.load(f)["word_list"]
    f.close()
    return wl


def create_ltw_dict(word_list):
    ltw = {}
    for word in word_list:
        for letter in set(word):  # set to remove duplicate letters in words to avoid duplicate entries
            if letter in ltw:
                ltw[letter].append(word)
            else:
                ltw[letter] = [word]
    return ltw


def create_freq_dicts(word_list):
    ltw = {}
    total = 0
    for word in word_list:
        for letter in word:  # set to remove duplicate letters in words to avoid duplicate entries
            total += 1
            if letter in ltw:
                ltw[letter] = ltw[letter] + 1
            else:
                ltw[letter] = 1
    ltwp = {k: math.ceil((v / total) * 10000) / 100 for k, v in ltw.items()}
    return ltw, ltwp


def print_top_x_dict(dict_to_print, x=5):
    x = 4 if x > 26 or x < 0 else x - 1
    for key in sorted(dict_to_print, key=dict_to_print.get, reverse=True):
        print(key, dict_to_print[key])
        if x <= 0:
            break
        x -= 1


def create_top_words_dict(word_list, letter_freq):
    wtaf = {}
    for word in word_list:
        letters = list(word)
        freq_total = 0
        for letter in letters:
            freq_total += letter_freq[letter]
        freq_total /= 5
        wtaf[word] = freq_total
    return wtaf


def wtaf_adjust(words_to_avg_freq):
    wtafa = {}
    for k, v in words_to_avg_freq.items():
        if len(set(k)) == 5:
            wtafa[k] = v
    return wtafa


def make_guess():
    print("Enter guessed letter and result (black=b,yellow=y,green=g)")
    print("If need help with the initial guess try one of these: IRATE, LATER, ADIEU, AEROS")
    print("space between. Ex: DOILT --> d y o g i b l g t b")
    print("or q to quit")
    init_inp = (input("Enter: ")).lower()
    return init_inp


def validate_guess(init_inp):
    if init_inp == "q":
        exit(0)
    split_inp = init_inp.split(" ")
    if len(split_inp) != 10:
        print("ERROR IN INPUT, TRY AGAIN!!!!")
        exit(1)
    if split_inp[1] == 'g' and split_inp[3] == 'g' and split_inp[5] == 'g' and split_inp[7] == 'g' and split_inp[
        9] == 'g':
        print("\nGame Won! Congratulations!!!!!!")
        exit(0)
    guess = []
    for k in range(0, 9, 2):
        guess.append([split_inp[k], split_inp[k + 1]])
    return guess


def filter_guess(guess):
    global yellow_tracker
    global green_tracker
    global next_not_letter
    global yellow
    global green

    next_pos_letter = []

    for i, gl in enumerate(guess):
        letter_guessed = gl[0]
        guess_result = gl[1]

        if guess_result == "g":
            if letter_guessed not in next_pos_letter:
                next_pos_letter.append(letter_guessed)
                green = True
            green_tracker[i] = letter_guessed
        elif guess_result == "y":
            if letter_guessed not in next_pos_letter:
                next_pos_letter.append(letter_guessed)
                yellow = True
            if letter_guessed not in yellow_tracker[i]:
                yellow_tracker[i].append(letter_guessed)
        else:
            if letter_guessed not in next_not_letter:
                next_not_letter.append(letter_guessed)

    return next_pos_letter


def add_search_letters(next_pos_letter, letter_freq):
    global num_letters_to_search_with
    global next_not_letter
    if len(next_pos_letter) < num_letters_to_search_with:
        for key in sorted(letter_freq, key=letter_freq.get, reverse=True):
            if len(next_pos_letter) == num_letters_to_search_with:
                break
            elif key not in next_pos_letter and key not in next_not_letter:
                next_pos_letter.append(key)
    return next_pos_letter


def initial_next_guess_words(next_pos_letter, letter_to_word):
    global num_letters_to_search_with
    next_guess_words = letter_to_word[next_pos_letter[0]]
    for i in range(1, num_letters_to_search_with):
        current_letter = next_pos_letter[i]
        current_letter_words = letter_to_word[current_letter]

        for word in current_letter_words:
            if word not in next_guess_words:
                next_guess_words.append(word)
    return next_guess_words


def green_filter(next_guess_words):
    global green_tracker
    next_guess_words_2 = []
    for word in next_guess_words:
        ok = True
        for i, state in enumerate(green_tracker):
            if state != 0:
                if word[i] != state:
                    ok = False
                    break
        if ok:
            next_guess_words_2.append(word)
    return next_guess_words_2


def yellow_filter(next_guess_words):
    global yellow_tracker
    next_guess_words_2 = []
    for word in next_guess_words:
        ok = True
        for i, state in enumerate(yellow_tracker):
            if state:
                for letter in state:
                    if word[i] == letter or letter not in word:
                        ok = False
                        break
                if not ok:
                    break
        if ok:
            next_guess_words_2.append(word)
    return next_guess_words_2


def black_filter(next_guess_words):
    global next_not_letter
    next_guess_words_2 = []
    for word in next_guess_words:
        ok = True
        for let in next_not_letter:
            if let in word:
                ok = False
                break
        if ok:
            next_guess_words_2.append(word)
    return next_guess_words_2


def get_guess(next_guess_words, words_to_avg_freq):
    guess_ranked = []
    for guess in next_guess_words:
        unique_let = len(set(guess))
        freq = words_to_avg_freq[guess]
        inp = [unique_let, freq, guess]
        guess_ranked.append(inp)
    guess_ranked.sort()
    guess_ranked.sort(reverse=True)
    return guess_ranked


master_word_list = load_word_list("word_list.json")
letter_to_words = create_ltw_dict(master_word_list)
letter_to_freq, letter_freq_perct = create_freq_dicts(master_word_list)
words_to_average_freq = create_top_words_dict(master_word_list, letter_to_freq)
words_to_avg_freq_adjusted = wtaf_adjust(words_to_average_freq)

yellow_tracker = [[], [], [], [], []]
green_tracker = [0, 0, 0, 0, 0]
yellow = False
green = False
num_letters_to_search_with = 4
next_not_letter = []

for game in range(6):
    raw_guess = make_guess()
    valid_guess = validate_guess(raw_guess)
    filtered_guess = filter_guess(valid_guess)
    next_possible_letters = add_search_letters(filtered_guess, letter_to_freq)
    next_guess_words_list = initial_next_guess_words(next_possible_letters, letter_to_words)
    if green:
        next_guess_words_list = green_filter(next_guess_words_list)
    if yellow:
        next_guess_words_list = yellow_filter(next_guess_words_list)
    next_guess_words_list = black_filter(next_guess_words_list)
    print(get_guess(next_guess_words_list, words_to_average_freq))
    print()
