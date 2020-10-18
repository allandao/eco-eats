# vim: set sw=4 noet ts=4 fileencoding=utf-8:

import pandas as pd
import numpy as np
import os
import logging
import pdb
import nltk
import re
from nltk.corpus import stopwords
set(stopwords.words('english'))

def setup_logger(logging_level, log_file):
	''' Args: logger supports levels DEBUG, INFO, WARNING, ERROR, CRITICAL.
	logger_level should be passed in in the format logging.LEVEL '''

	logging.basicConfig(level = logging_level)
	logger = logging.getLogger(__name__)
	return logger

class Processor():
	'''
	This class will accept data from requests to Amazon for product
	titles and ingredients. It will then process that data and match
	the data to a food and carbon emission from a Kaggle dataset.
	The dataset can be found here:
	https://www.kaggle.com/selfvivek/environment-impact-of-food-production
	With more research into carbon emissions and broader datasets on the
	global impact of farming on climate change, this tool can be expanded
	to match to even more products on Amazon.
	'''

	#XXX: will need to access kaggle data through server eventually??
	def __init__(self, logging_level, data_path):
		# Sample data: {“title”: “SOUR CREAM, 365 WFM, UNFI, 12-16OZ”,
		# “ingredients” : “CULTURED PASTEURIZED GRADE A ORGANIC MILK,
		# PASTEURIZED ORGANIC CREAM, MICROBIAL ENZYMES”}
		#XXX hook up to flask later
		self.request_data = {'title' : 'milk', 'ingredients' : 'dairy milk'}
		#self.data_path = data_path
		self.log = setup_logger(logging_level, './log.log')
		# Dataset from Kaggle
		self.df = self.get_df(data_path)

	# Assumes the file Food_Production.csv is in the working directory
	def get_df(self, data_path):
		'''
		Reads in the csv file for food carbon emissions
		'''
		if os.path.exists(data_path):
			self.log.info(' Reading file %s', data_path)
			df = pd.read_csv(data_path)
		else:
			self.log.critical(' Failed to read data file %s, setting'
				+ ' df = 0', data_path)
			df = 0
		return df

	def match_to_dataset(self, df, request_data):
		'''
		Params:
			df: a pandas dataframe from a csv with foods and
				their cabron emissions
			request_data: a dict containing 'title' for the Amazon food's
				title and 'ingredients' containing the searched-for food's
				ingredients (as strings)
		Returns:
			food_stats: a row from df representing different facts about
				carbon emissions from the production of the searched
				for food

		This function takes the request data from the Amazon search
		and matches it to a corresponding food in the Kaggle dataset.
		It returns the row of carbon emissions corresponding to that food.
		'''
		self.log.debug('df: {}'.format(df))
		# get request data title
		title = request_data['title']
		# kaggle data titles
		foods = df['Food product']
		ingredients = request_data['ingredients']
		self.log.debug('kaggle foods: {}'.format(foods))
		# iterate over kaggle food titles and try to match it
		# Simple way: re expression matching
		# More complex way: NLP processing to match to related foods if
		# exact food is not found
		row_stats = {}
		matches_i = {}

		matches_i = self.match_titles(title, foods, matches_i)

		# if only one match was found between amazon product
		# and dataset
		if len(matches_i) == 1:
			match_i = list(matches_i.values())[0]
			# Integer based row slicing
			row_stats = df.iloc[match_i]

		# To break ties between matches
		elif len(matches_i) > 1:
			# Check ingredients -->
			row_stats = self.match_ingredients(
					df, ingredients, matches_i)

		#XXX what is matches_i is empty???
		# To find matches through ingredients if none came up
		else:
			#XXX won't work b/c foods isn't a dict like matches_i, with
			# it's index as a value in dict
			#self.match_ingredients(df, ingredients, foods)
			self.log.info('No matches found!!')

		self.log.debug('row_stats: {}'.format(row_stats))
		return row_stats

	def match_titles(self, title, foods, matches_i):
		'''
		Loops through kaggle food titles and compare with amazon title.
		Updates matches_i accordingly.
		Ex: title = 'Apple', foods = ['Apples', 'Bananas'], matches_i = {}
		returns matches_i = {'Apples' : 0}
		'''
		# Loop through all kaggle titles
		for i, food_title in enumerate(foods):
			title = title.lower()
			food_title = food_title.lower()
			#if title in food_title or food_title in title:
			if self.check_tokenized_matches(title, food_title):
				matches_i[food_title] = i

		return matches_i

	def check_tokenized_matches(self, title, food_title):
		'''
		Returns whether any words in the Amazon title matched any words in
		a given Kaggle food title
		'''
		match = False
		tokenized_title = self.tokenize([title])
		tokenized_food_title = self.tokenize([food_title])
		for word1 in tokenized_title:
			for word2 in tokenized_food_title:
				if word1 == word2:
					match = True
		return match

#XXX trying to use ingredients if no matches are found with the title
#	def match_unmatched_ingredients(self, ):
#		# Need to compare most frequent?? ingredients to every
#		# word in every food in food_titles, food title
#		# with most matches to ingredient wins
#
#		#most_freq_ingredient = [0:9]
#		# Amazon
#		for ingr in tokenized_ingredients:
#			# Kaggle
#			#freq_lists
#			for food in food_titles:
#				food = self.tokenize(food)
#				#get freq vector of how many times


	def match_ingredients(self, df, ingredients, matches_i):
		'''
		Params:
			df: pandas df of Food_Production.csv
			ingredients: string of ingredients
				Ex: 'milk, flour, sugar'
			matches_i: dictionary with matching food title and
				its corresponding index in df food_titles
				Ex: {'milk' : 3, 'soymilk' : 40}
		Returns:
			row_stats = {'Food product' : 'Milk', 'Land use' : '0.5'...}
		This function uses the ingredients list, turns it into a bag
		of words array sorted by the highest frequency words to lowest.
		It then uses that bag of ingredient frequencies to compare to the
		kaggle food titles. The soonest match found is used to get
		row_stats.
		'''

		row_stats = {}
		# bag of words(ingredients)
		tokenized_ingr = self.tokenize([ingredients])
		matches_titles = list(matches_i.keys())
		tokenized_matches = self.tokenize(matches_titles)
		freq_vector = self.get_ingr_frequency_vector(
				tokenized_matches, tokenized_ingr)
		# highest to lowest frequencies of ingredients words
		# that match titles
		highest_match = max(freq_vector)
		#NOTE: if frequencies are tied, this uses the last i
		# value in tokenized_matches for row_stats. Not great...
		zero_freq_vector = [0 for i in range(len(freq_vector))]
		if (np.array_equal(freq_vector, zero_freq_vector)):
			self.log.info("\nNo ingredient matches were found!!\n")
			row_stats = pd.DataFrame({'empty' : []})
		else :
			self.log.info("\nIngredient match found!\n")
			for i, freq in enumerate(freq_vector):
				if freq == highest_match:
					match_title = tokenized_matches[i]
					match_i = matches_i[match_title]
					row_stats = df.iloc[match_i]
		return row_stats

	# SOURCE: https://www.freecodecamp.org/news/an-introduction-to-bag-of-words-and-how-to-code-it-in-python-for-nlp-282e87a9da04/
	def word_extraction(self, sentence):
		ignore = ['a', "the", "is"]
		words = re.sub("[^\w]", " ", sentence).split()
		cleaned_text = [w.lower() for w in words if w not in ignore]
		return cleaned_text

	def tokenize(self, all_sentences):
		token_words = []
		# Appends cleaned, tokenized words to the array token_words.
		# Represents tokenized words of all sentences passed combined into
		# one array
		for sentence in all_sentences:
			cleaned_words = self.word_extraction(sentence)
			token_words.extend(cleaned_words)
		return token_words

	#NOTE: not used right now because it doesn't guarantee the bag_vector
	# frequencies corresponding to an index in a passed in token
	# words array
	def get_frequency_vector(self, tokenized1, tokenized2):
		longer_text = max(len(tokenized1), len(tokenized2))
		bag_vector = np.zeros(longer_text)
		for word1 in tokenized1:
			for i, word2 in enumerate(tokenized2):
				if word2 == word1:
					bag_vector[i] += 1
		return bag_vector

	def get_ingr_frequency_vector(self, token_matches, token_ingr):
		'''
		Returns vector of number of matches with token_ingr for
		each matched title in token_matches
		Knowing that token_matches was passed first allows us to assume
		bag_vector indices correspond to token_matches indices
		Ex:
		token_matches = ['apple', 'applemilk'], token_ingr = ['applemilk',
		'applemilk', 'sugar']
		bag_vector = [0, 2]
		'''
		bag_vector = np.zeros(len(token_matches))
		for i, word1 in enumerate(token_matches):
			for word2 in token_ingr:
				if word2 == word1:
					bag_vector[i] += 1
					self.log.debug("bag_vector: ".format(bag_vector))
		return bag_vector

	def get_json_match(self, df, request_data):
		'''
		Converts the matching carbon dioxide emissions data to json format
		'''
		row_stats = self.match_to_dataset(df, request_data)
		match = row_stats.to_json()
		return match

if __name__ == '__main__':
	data_path = './Food_Production.csv'
	logging_level = logging.DEBUG
	proc = Processor(logging_level, data_path)
	row_stats = proc.get_json_match(proc.df, proc.request_data)
	proc.log.debug('JSON row_stats: {}'.format(row_stats))
