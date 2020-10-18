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
		self.request_data = {'title' : 'milk', 'ingredients' : 'dairy'}
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
		self.log.info('kaggle foods: {}'.format(foods))
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
		else:
			# Check ingredients -->
			row_stats = self.match_ingredients(
					df, ingredients, matches_i)
			pdb.set_trace()
		self.log.info('row_stats: {}'.format(row_stats))

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
			#XXX this may use Soymilk for milk instead of Milk for milk...
			# need more robust matching
			tokenized_title = self.tokenize([title])
			#for
			if title in food_title or food_title in title:
				matches_i[food_title] = i

		return matches_i


	def match_ingredients(self, df, ingredients, matches_i):
		'''
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
		#XXX what if tied??
		if (all(freq_vector) == 0):
			for i, freq in freq_vector:
				if freq == highest_match:
					match_title = tokenized_matches[i]
					match_i = matches_i[match_title]
					row_stats = df.iloc[match_i]
		pdb.set_trace()
		# sort bag of words to highest frequency first
		# List comprehension
		# matches_titles = [foods[i] for i in matches_i]
		# for higher_freq_word in bag_of_words:
			# for match, df_index in matches_titles:
				# if higher_freq_word in match:
					# row_stats = df.iloc[df_index]
					# break

				# if no matches were found in the ingredients
				# else
					# return empty row_stats because no foods matched the
					# amazon searched food
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
		#pdb.set_trace()
		#token_words = sorted(list(set(token_words)))
		return token_words

	def get_frequency_vector(self, tokenized1, tokenized2):
		longer_text = max(len(tokenized1), len(tokenized2))
		bag_vector = np.zeros(longer_text)
		for word1 in tokenized1:
			for i, word2 in enumerate(tokenized2):
				if word2 == word1:
					bag_vector[i] += 1
					self.log.info("{0}\n{1}\n".format(
							sentence, numpy.array(bag_vector)))
		return bag_vector

	def get_ingr_frequency_vector(self, token_matches, token_ingr):
		'''
		Returns vector of number of matches with token_ingr for
		each matched title in token_matches
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
					self.log.info("{0}\n{1}\n".format(
							sentence, numpy.array(bag_vector)))
		return bag_vector


if __name__ == '__main__':
	data_path = './Food_Production.csv'
	logging_level = logging.INFO
	proc = Processor(logging_level, data_path)
	row_stats = proc.match_to_dataset(proc.df, proc.request_data)
