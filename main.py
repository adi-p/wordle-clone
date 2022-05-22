
import sys
import argparse
from functools import reduce
import random
from colorama import init, Fore

# import numpy as np
# import pandas as pd

from solver import Wordle_Solver, Wordle_Solver_2
from wordle import Wordle, Correct_Code

#####################################
## TODO ##
#####################################
# - Consider using pandas (maybe numpy) for this
# - Consider saving some type of data to make solving faster (solver_2)
# 	In general make solver_2 more efficient
# - Add a verbose flag and print all guesses made for a word
# - Add regression tests, unit tests?
#####################################

#####################################

### Human ###

def human_solve(wordle):
	# TODO: make human solving nicer
	# - Add ability to stop and see the goal word
	# - Add a looping mechanism to play several times. (Maybe in `main`)
	# - Show already used letters (Like keyboard in real wordle)

	result = None
	prev_word = None
	CORRECT_RESULT = [ Correct_Code.GREEN for i in range(5) ]
	guess_count = 0

	while not result == CORRECT_RESULT:
		word = input("Guess a 5 letter word: ").lower()

		if(not len(word) == 5):
			print("The word must be 5 letters.")
			continue
		elif not wordle.is_allowed_guess(word):
			print("This guess is not allowed")
			continue 

		guess_count += 1

		result = wordle.get_guess_results(word)
		prev_word = word
		color_print_result(word, result)

	print(f"You won, the word was {wordle.goal}")
	print(f"You took {guess_count} tries")


### Utilities ###

def color_print_result(word, result):

	def code_to_colour(code):
		if code == Correct_Code.GREEN:
			return Fore.GREEN
		elif code == Correct_Code.YELLOW:
			return Fore.YELLOW
		return Fore.WHITE

	colour_result = list(map(code_to_colour, result))

	for colour, letter in zip(colour_result, list(word)):
		print(colour + letter, end='')
	print(' [ ', end='')

	for colour, code in zip(colour_result, result):
		print(colour + str(code), end=' ')
	print(']')



def load_words(file):
	words = []
	with open(file) as f:
		words = f.readlines()
	words = [ word.strip() for word in words ]
	return words

def init_parser():
	parser = argparse.ArgumentParser()

	# Play
	parser.add_argument("-p", "--play", action="store_true", default=False, help="play Wordle on the command line")

	# Solve
	parser.add_argument("-s", "--solve", nargs="?", type=int, choices=[1, 2], const=1, default=1, help="choose a solver level. Default = 1")

	# Sample word count
	parser.add_argument("--sample-word-count", "-w", type=int, help="choose the size of the sample list of words to run the solver with")

	return parser

def main():

	# init colored 
	init(autoreset=True)

	parser = init_parser()
	args = parser.parse_args()

	allowed_guesses = load_words("words.txt")
	answer_words = load_words("answers.txt")

	wordle = Wordle(answer_words, allowed_guesses)

	# Playing Worlde
	if args.play:
		# TODO: maybe loop if user wants to play again
		wordle.choose_goal_word()
		human_solve(wordle)
		return
	
	# Choosing a Solver
	if args.solve == 1:
		solver = Wordle_Solver(wordle, allowed_guesses)
	elif args.solve == 2:
		# solver = Wordle_Solver_2(wordle, allowed_guesses)
		solver = Wordle_Solver_2(wordle, answer_words) # use answer_words instead of allowed guesses to have a smaller list for now
	else:
		raise SystemExit("NO SOLVER CHOOSEN - please choose a solver")

	# Choosing a sample size
	if args.sample_word_count:
		test_words = random.sample(answer_words, args.sample_word_count)
	else:
		test_words = answer_words


	results = []
	for word in test_words:
		try_count = solver.solve(word)
		# print(word, try_count)
		results.append({ "word": word, "count": try_count})

	average = sum(map(lambda el: el["count"], results)) / len(test_words)

	max_el = reduce(lambda el, max_el: max_el if max_el["count"] > el["count"] else el, results)
	min_el = reduce(lambda el, min_el: min_el if min_el["count"] < el["count"] else el, results)
	print(f"Average try count { average }")
	print(f"Max try {max_el['count']} for word {max_el['word']}")
	print(f"Min try {min_el['count']} for word {min_el['word']}")
	
if __name__ == "__main__":
    main()