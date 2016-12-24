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

df1 = pd.read_pickle('presidential_speeches.pickle')
df2 = pd.read_pickle('presidential_speeches2.pickle')
dataframe = df1.append(df2)

def get_words(text):
    p_stemmer = PorterStemmer()
    return [p_stemmer.stem(word) for word in simple_preprocess(text) if word not in STOPWORDS]
    
def gen_corpus(dataframe): 
    speeches = dataframe.transcript
    docs = speeches.tolist()
    words = [get_words(doc) for doc in docs]
    print("1")
    counts = corpora.Dictionary(words)
    print("1.5")
    corpus = [counts.doc2bow(word) for word in words]
    print("2")
    #pickle.dump(texts, open("words_list.pickle", "wb"))
    #pickle.dump(corpus, open("corpus.pickle", "wb"))
    speeches_topics = LdaModel(corpus=corpus,
                               id2word=counts,
                               num_topics=20,
                               passes=1)
    print("3")
    vis_data = gensimvis.prepare(speeches_topics, corpus, counts)
    print("4")
    pyLDAvis.display(vis_data)

gen_corpus(dataframe)