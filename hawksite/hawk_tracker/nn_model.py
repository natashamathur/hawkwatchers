import math
import nltk
import math
import pandas as pd
import numpy as np 
import enchant

import sklearn
import sklearn.neural_network
import sklearn.naive_bayes
import sklearn.tree
import sklearn.ensemble

from sklearn.model_selection import train_test_split

def check_english(new_text, thresh = .25):
	'''
	Takes a release text and roughly determines the number of non-english
	words. If the percentage of non-english words is greater or equal to
	the specified threshold, return False. Else, return True.
	'''

	d = enchant.Dict('en_US')

	word_list = new_text.split(' ')
	non_en = 0

	for w in word_list:
		if not d.check(w):
			non_en += 1

	return non_en/len(word_list) <= thresh


def predict(model, new_text):
	'''
	Takes a model specification and new release text and, 
	using the classifier specified, trains
	on the tf-idf scores for all press releases since February 1994,
	predicting whether the new text heralds an increase in the federal
	interest rate.

	Inputs:
		model (str): a string specifying the classifier desired
		new_text (str): a string representation of the new release text

	Outputs:
		prediction (boolean) 
	'''

	# reads local csv with all releases from Feb 1994 ['release_text'], 
	# the month ['month'] & year ['year'] of release, 
	# the change in interest rate associated with that month ['Change'],
	# and a boolean expression indicating whether
	# the interest rate increased ['increase']
	
	releaserates_df = pd.read_csv('hawk_tracker/allreleaserates.csv', index_col=0)


	# computes tf-idf for all release texts and creates a vector representation
	# of each document's scores
	TFVectorizer = sklearn.feature_extraction.text.TfidfVectorizer(max_df=15,
		stop_words='english', norm='l2')

	TFVects = TFVectorizer.fit_transform(releaserates_df['release_text'])
	releaserates_df['vect'] = [np.array(v).flatten() for v in TFVects.todense()]

	# instantiate model specified
	if model == "NN":
		clf = sklearn.neural_network.MLPClassifier()
	
	elif model == 'DT':
		clf = sklearn.tree.DecisionTreeClassifier(max_depth=10)
	
	elif model == 'BAG':
		tree = sklearn.tree.DecisionTreeClassifier(max_depth=10) 
		clf = sklearn.ensemble.BaggingClassifier(tree, n_estimators=100,
			max_samples=0.8) 
	
	elif model == 'NB':
		clf = sklearn.naive_bayes.GaussianNB()


	# fit model
	clf.fit(np.stack(releaserates_df['vect'], axis=0), releaserates_df['increase'])

	# compute tf-idf for new_text
	TFVects_test = TFVectorizer.transform([new_text])
	test_vects = [np.array(v).flatten() for v in TFVects_test.todense()]

	# classify new_text 
	y_pred = clf.predict(np.stack(test_vects, axis=0))

	return y_pred[0]




