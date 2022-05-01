
import sys
from enum import Enum
from functools import reduce
import random
import argparse
# import numpy as np
# import pandas as pd

## TODO ##
# - Consider using pandas (maybe numpy) for this
# - Consider saving some type of data to make solving faster (solver_2)
# 	In general make solver_2 more efficient
# - Consider splitting program into multiple files as it is getting larger.
# - Add a verbose flag and print all guesses made for a word

class Correct_Code(Enum):
	GREEN = 1
	YELLOW = 0
	GREY = -1

	def __str__(self):
		return self.name

	def __repr__(self):
		return self.name


class Wordle:

	def __init__(self, words, allowed_guesses):
		self.words = words
		self.allowed_guesses = { guess : 1 for guess in allowed_guesses }
		self.goal = None

	def set_goal_word(self, word):
		if word in self.words:
			self.goal = word
		else:
			raise Exception(f"Chosen word: {word} is not in the word list")

	def choose_goal_word(self):
		self.goal = random.choice(self.words)

	def is_allowed_guess(self, guess):
		return guess in self.allowed_guesses

	# Assumes the guess is allowed
	def get_guess_results(self, guess):
		guess_letters = list(guess)
		goal_letters = list(self.goal)

		result = [ Correct_Code.GREY for i in range(5) ]

		for idx, letter in enumerate(guess_letters):
			if letter == goal_letters[idx]:
				result[idx] = Correct_Code.GREEN
				goal_letters[idx] = None # Remove letter so it won't be considered for YELLOW correctness
				guess_letters[idx] = None

		for idx, letter in enumerate(guess_letters):
			if letter != None and letter in goal_letters:
				result[idx] = Correct_Code.YELLOW
				goal_idx = next(i for i, l in enumerate(goal_letters) if l == letter)
				goal_letters[goal_idx] = None # Remove letter so it won't be considered for future YELLOW correctness

		return result



# Naive solution
class Wordle_Solver:

	def __init__(self, wordle, allowed_guesses):
		self.wordle = wordle
		self.allowed_guesses = allowed_guesses
		self.allowed_guesses_original = allowed_guesses

	def reset(self):
		self.allowed_guesses = self.allowed_guesses_original

	def solve(self, goal_word = None):
		if goal_word:
			self.wordle.set_goal_word(goal_word)
		else:
			self.wordle.choose_goal_word()
		
		result = None
		prev_word = None
		CORRECT_RESULT = [ Correct_Code.GREEN for i in range(5) ]
		tries = 0

		while not result == CORRECT_RESULT:
			word = self.make_guess(result, prev_word)
			tries += 1

			result = self.wordle.get_guess_results(word)
			prev_word = word

		self.reset()

		return tries


	def filter_words(results, guess, word_list):
			greens = {}
			yellows = {}
			greys = {}

			for idx, corr_code in enumerate(results):
				if corr_code == Correct_Code.GREEN:
					greens[idx] = guess[idx]
				elif corr_code == Correct_Code.YELLOW:
					yellows[idx] = guess[idx]
				elif corr_code == Correct_Code.GREY:
					greys[idx] = guess[idx]

			def filter_guess(word):
				if word == guess:
					return False

				for idx, el in greens.items():
					if word[idx] != guess[idx]:
						return False

				for idx, el in yellows.items():
					# TODO this doesn't deal with two yellows for the same letter. As long as the letter appears once, the word will not be filtered.
					if not guess[idx] in word:
						return False

				for idx, el in greys.items():
					if word[idx] == guess[idx]:
						return False 

					if (not guess[idx] in yellows.values() and not guess[idx] in greens.values()) and guess[idx] in word:
						return False
				
				return True

			return list(filter(filter_guess, word_list))


	def make_guess(self, prev_result = None, prev_guess = None):
		if prev_result and prev_guess:
			self.allowed_guesses = Wordle_Solver.filter_words(prev_result, prev_guess, self.allowed_guesses)

		return random.choice(self.allowed_guesses)


class Wordle_Solver_2:

	def __init__(self, wordle, allowed_guesses):
		self.wordle = wordle
		self.allowed_guesses = allowed_guesses
		self.allowed_final_guesses = allowed_guesses
		self.allowed_guesses_original = allowed_guesses
		# do I do set up here?
		# What do I set up?
		# rank words by entropy
		#		- given a word, how much does the list reduce by on average over any kind of result it gives

	def train(self):

		# TODO: add more possible results
		possible_results = [ 
			[ Correct_Code.GREY for i in range(5) ], 
			[ Correct_Code.GREEN for i in range(5) ], 
			[ Correct_Code.YELLOW for i in range(5) ] 
		] # TODO: every permutation of a result

		word_scores = []

		# TODO: see if it is possible to choose words from outside allowed_guesses that help reduce search space
		# Along the same vein see if the filtering for words is done as smartly as it can be.
		for word in self.allowed_guesses:

			total_remaining = 0

			for result in possible_results:
				filtered_word_list = Wordle_Solver.filter_words(result, word, self.allowed_guesses)
				total_remaining += len(filtered_word_list)
			
			word_scores.append((word, total_remaining))


		word_scores.sort(key=(lambda el: el[1]))

		self.allowed_guesses = list(map(lambda el: el[0], word_scores))

	def reset(self):
		self.allowed_guesses = self.allowed_guesses_original


	# NOTE: this is just a duplicate of the solve() func on Wordle_Solver, maybe think about how to remove this duplication
	def solve(self, goal_word = None):
		if goal_word:
			self.wordle.set_goal_word(goal_word)
		else:
			self.wordle.choose_goal_word()
		
		result = None
		prev_word = None
		CORRECT_RESULT = [ Correct_Code.GREEN for i in range(5) ]
		tries = 0

		while not result == CORRECT_RESULT:
			word = self.make_guess(result, prev_word)
			tries += 1

			result = self.wordle.get_guess_results(word)
			prev_word = word

		self.reset()

		return tries


	def make_guess(self, prev_result = None, prev_guess = None):
		if prev_result and prev_guess:
			self.allowed_guesses = Wordle_Solver.filter_words(prev_result, prev_guess, self.allowed_guesses)

		self.train()

		return self.allowed_guesses[0]
		

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
		print(word, result)

	print(f"You won, the word was {wordle.goal}")
	print(f"You took {guess_count} tries")


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
	parser.add_argument("--sample-word-count", type=int, help="choose the size of the sample list of words to run the solver with")

	return parser

def main():

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