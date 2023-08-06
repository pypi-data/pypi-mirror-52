

"""
[TITLE]
Author: 
Updated Date: 

Tokenisation
Splitting strings into individual words & symbols

Stemming
Normalising tokens into its base form or root form

Lemmatisation
Similar to stemming but outputs a proper word.

Parts of Speech (POS)
Used to tag the different types of words and the role they play in a sentence

Stopwords
Words that are not useful for NLP

Named Entity Recognition (NER)
Further tagging of nouns to determine what category they fall into - e.g. person, organisation, location, etc

Syntax Tree
Represents the syntactic structure of sentences or strings To render a syntax tree in a notebook, you'll need to download ghostscript

Chunking
Picking up individual pieces of information and grouping them into bigger pieces

"""

########## IMPORT LIBRARIES ##########
import pandas as pd
import numpy as np
import nltk
import spacy as spy


########## LOAD DATA ##########

### Via CSV ###
df = pd.read_csv(r"directory")

### Via API ###
# https://www.peterbe.com/plog/best-practice-with-retries-with-requests
# Troubleshooting: requests library, hotspot or WiFi NOT VPN, status code output by request
