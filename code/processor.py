# vim: set sw=4 noet ts=4 fileencoding=utf-8:

import pandas as pd
import os
import logging
import pdb

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

	#XXX: will need to access kaggle data through server eventually
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
		self.log.info('kaggle foods: {}'.format(foods))
		# iterate over kaggle food titles and try to match it 
		# Simple way: re expression matching
		# More complex way: NLP processing to match to related foods if 
		# exact food is not found
		for i, food_title in enumerate(foods):
			#XXX this may use Soymilk for milk instead of Milk for milk...
			# need more robust matching
			if title in food_title:
				pdb.set_trace()
				# Integer based row slicing
				row_stats = df.iloc[i]
				self.log.info(row_stats)

		return row_stats


if __name__ == '__main__':
	data_path = './Food_Production.csv'
	logging_level = logging.INFO
	proc = Processor(logging_level, data_path)
	proc.match_to_dataset(proc.df, proc.request_data)
		

