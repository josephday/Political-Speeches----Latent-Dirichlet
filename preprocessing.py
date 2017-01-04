from gensim.parsing.preprocessing import STOPWORDS
from gensim.models.ldamodel import LdaModel
from gensim import corpora
import matplotlib.pyplot as plt
from sklearn.cluster import KMeans
import pandas as pd
import numpy as np
import pickle
from nltk.stem.porter import PorterStemmer
from nltk.tokenize import RegexpTokenizer


df1 = pd.read_pickle('presidential_speeches.pickle')
df2 = pd.read_pickle('presidential_speeches2.pickle')
dataframe = df1.append(df2)

tokenizer = RegexpTokenizer(r'\w+')
p_stemmer = PorterStemmer()

   
def get_words(text):
    '''Takes in a large string, such as a speech,
    and returns list of stemmed, non-stop tokens
    '''
    raw = text.lower()    
    return [p_stemmer.stem(word) for word in tokenizer.tokenize(raw) if word not in STOPWORDS]


def gen_corpus(dataframe): 
    '''Takes in dataframe of large strings, such as speeches,
    and returns speeches_topics, a Latent Dirichlet Topic Model.
    Pickles the list of word lists and the corpus along the way.
    '''
    speeches = dataframe.transcript
    docs = speeches.tolist()
    words = [get_words(doc) for doc in docs]
    counts = corpora.Dictionary(words)
    corpus = [counts.doc2bow(word) for word in words]
    pickle.dump(words, open("words_list.pickle", "wb"))
    pickle.dump(corpus, open("corpus.pickle", "wb"))
    #Note: speed and passes have negative correlation
    #Cont. precision and passes have positive correlation
    #10 will be decently precise, but take 5-10 min on my VM
    speeches_topics = LdaModel(corpus=corpus,
                               id2word=counts,
                               num_topics=20,
                               passes=10)
    
    pickle.dump(speeches_topics, open("topics.pickle", "wb"))
    return speeches_topics
