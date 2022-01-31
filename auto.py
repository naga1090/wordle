from solver import *
from wordle import *

# print("Welcome to wordle!\n")
the_guess = "irate"
the_result = ""
for i in range(12):
    the_result = play_guess(the_guess)
    the_guess = solve_guess(the_result)