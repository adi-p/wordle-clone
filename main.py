
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
			print(self.words[:10])
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

	# wordle.set_goal_word('expel')

	# print(wordle.get_guess_results('lives'))
	# print(wordle.get_guess_results('elves'))
	# print(wordle.get_guess_results('slump'))
	# print(wordle.get_guess_results('yummy'))
	# print(wordle.get_guess_results('uymjy'))

	wordle.choose_goal_word()

	result = []
	CORRECT_RESULT = [ Correct_Code.GREEN for i in range(5) ]
	while not result == CORRECT_RESULT:
		word = input("Guess a 5 letter word: ").lower()

		if(not len(word) == 5):
			print("The word must be 5 letters.")
			continue
		elif not wordle.is_allowed_guess(word):
			print("This guess is not allowed")
			continue 

		result = wordle.get_guess_results(word)
		print(result)

	print(f"You won, the word was {wordle.goal}")



if __name__ == "__main__":
    main()