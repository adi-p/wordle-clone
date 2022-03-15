
import sys
from enum import Enum
from functools import reduce
import random


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
			raise Exception("Chosen word is not in the word list")

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

		return tries


	def make_guess(self, prev_result = None, prev_guess = None):
		if prev_result and prev_guess:
			greens = {}
			yellows = {}
			greys = {}

			for idx, corr_code in enumerate(prev_result):
				if corr_code == Correct_Code.GREEN:
					greens[idx] = prev_guess[idx]
				elif corr_code == Correct_Code.YELLOW:
					yellows[idx] = prev_guess[idx]
				elif corr_code == Correct_Code.GREY:
					greys[idx] = prev_guess[idx]

			def filter_guess(guess):
				if guess == prev_guess:
					return False

				for idx, el in greens.items():
					if guess[idx] != prev_guess[idx]:
						return False

				for idx, el in yellows.items():
					# this doesn't deal with two yellows for the same letter. As long as the letter appears once, the word will not be filtered.
					if not prev_guess[idx] in guess:
						return False

				for idx, el in greys.items():
					if guess[idx] == prev_guess[idx]:
						return False 

					if (not prev_guess[idx] in yellows.values() and not prev_guess[idx] in greens.values()) and prev_guess[idx] in guess:
						return False
				
				return True

		
			self.allowed_guesses = list(filter(filter_guess, self.allowed_guesses))

		return random.choice(self.allowed_guesses)


def human_solve(wordle):
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

def main():

	allowed_guesses = load_words("words.txt")
	answer_words = load_words("answers.txt")

	wordle = Wordle(answer_words, allowed_guesses)
	solver = Wordle_Solver(wordle, allowed_guesses)

	results = []
	for word in answer_words:
		try_count = solver.solve(word)
		results.append({ "word": word, "count": try_count})
		solver.reset()

	average = sum(map(lambda el: el["count"], results)) / len(answer_words)

	max_el = reduce(lambda el, max_el: max_el if max_el["count"] > el["count"] else el, results)
	min_el = reduce(lambda el, min_el: min_el if min_el["count"] < el["count"] else el, results)
	print(f"Average try count { average }")
	print(f"Max try {max_el['count']} for word {max_el['word']}")
	print(f"Min try {min_el['count']} for word {min_el['word']}")
	
if __name__ == "__main__":
    main()