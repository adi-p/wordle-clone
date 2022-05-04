from wordle import Wordle, Correct_Code
import random


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
		