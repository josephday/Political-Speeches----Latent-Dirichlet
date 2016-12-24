#%matplotlib inline  
from gensim.parsing.preprocessing import STOPWORDS
from gensim.utils import simple_preprocess
from gensim.models import TfidfModel, LsiModel
from gensim.models.ldamodel import LdaModel
from gensim import corpora
from gensim import matutils
import matplotlib.pyplot as plt
from sklearn.cluster import KMeans
from collections import defaultdict
import pyLDAvis.gensim as gensimvis
import pyLDAvis
import pandas as pd
import numpy as np
import pickle
import lda
from nltk.stem.porter import PorterStemmer

dataframe = pd.read_pickle('presidential_speeches.pickle')

def get_words(text):
    p_stemmer = PorterStemmer()
    return [p_stemmer.stem(word) for word in simple_preprocess(text) if word not in STOPWORDS]
    
speeches = dataframe.transcript
docs = speeches.tolist()
texts = [get_words(docs) for doc in docs]