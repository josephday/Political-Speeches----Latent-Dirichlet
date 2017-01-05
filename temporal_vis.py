import pandas as pd
import numpy as np
import pickle
from sklearn import manifold
import matplotlib.pyplot as plt
import mpld3
import colorsys
from mpld3 import plugins
import matplotlib.patches as mpatches
from mpldatacursor import datacursor





df1 = pd.read_pickle('presidential_speeches.pickle')
df2 = pd.read_pickle('presidential_speeches2.pickle')
dataframe = df1.append(df2)

speeches_topics = pd.read_pickle('topics.pickle')
corpus = pd.read_pickle('corpus.pickle')


def format(dataframe):
    speeches = dataframe.transcript
    doc_key = list(speeches.index)
    result = {}
    for doc_id in range(len(corpus)):
        doc_book = corpus[doc_id]
        doc_tops = speeches_topics.get_document_topics(doc_book, 0)
        tmp = []
        for top_id, top_prob in doc_tops:
            tmp.append(top_prob)
        result[doc_key[doc_id]] = tmp
    df = pd.DataFrame.from_dict(result, orient='index')
    return df


def tsne(df):
    df= format(df)
    tsne = manifold.TSNE(n_components=2, early_exaggeration = 2, init='pca', random_state=0)
    transformed = tsne.fit_transform(df)
    clusters = pd.DataFrame(transformed)
    clusters = clusters.set_index(df.index)
    #print (clusters.head(5))
    clusters.to_csv('speech_clusters.csv', sep=',')

    #from IPython import get_ipython
    #get_ipython().run_line_magic('matplotlib inline')
    mpld3.enable_notebook()
    presidents = [item.split('|')[0] for item in df.index.values.tolist()]
    unique = list(set(presidents))
    N = len(unique)
    HSVs = [(x*1.0/N, 0.7, 0.9) for x in range(N)]
    RGBs = list(map(lambda x: colorsys.hsv_to_rgb(*x), HSVs))
    #return RGBs
    colors = {}
    for i, p in enumerate(unique):
        colors[p] = RGBs[i]
    #return colors
    fig, ax = plt.subplots(subplot_kw=dict(axisbg='#EEEEEE'))#, figsize=(10,10))
    print(1)
    #ax.grid(color='black', linestyle='solid')
    print(2)
    '''return clusters.ix[:, 0]
    scatter = ax.scatter(clusters.ix[:, 0],
                        clusters.ix[:, 1],
                        s=80,
                        label=presidents,
                        alpha=0.3,
                        c=[colors[p] for p in presidents])'''
    xs = clusters.ix[:, 0].tolist()
    ys = clusters.ix[:, 1].tolist()

    for i in range(0,942):
        ax.scatter([xs[i]],
                  [ys[i]],
                  s=80,
                  label = presidents[i],
                  alpha=0.3,
                  c = colors[presidents[i]])
    print(3)

    ax.grid(color='black', linestyle='solid')
    print(4)
    ax.set_title("Clustering presidential speeches", size=20)
    print(5)
    labels = ['<h3>{president}</h3>'.format(president=x) for x in presidents] 
    print(6)
    tooltip = plugins.PointHTMLTooltip(scatter, labels)
    print(7)
    #plugins.connect(fig, tooltip)
    print(8)
    #legend = ax.legend(loc='upper center', shadow=True)
    #frame = legend.get_frame()
    #frame.set_facecolor('0.90')
    #for label in legend.get_texts():
    #    label.set_fontsize('large')
    print(9)
    plt.show(fig)
    #handled = []
    #for president in unique:
    #    handled.append(mpatches.Patch(color = colors[president], label = str(president))) 
    #plt.legend(handles = handled)
    #plt.show()
    

    