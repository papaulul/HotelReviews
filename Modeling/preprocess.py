#%% 
import os
import pandas as pd
import numpy as np
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.metrics.pairwise import euclidean_distances
import nltk; nltk.download('stopwords')
from nltk.corpus import stopwords
from sklearn.cluster import MiniBatchKMeans
from sklearn import metrics
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics import adjusted_rand_score
import pickle


#%%
file_path = "files/eda.pkl"
review = pd.read_pickle(file_path)

#%%
corpus = review['review'].tolist()

#%%
stop_words = stopwords.words('english')
vectorizer = CountVectorizer(analyzer='word',       
                             min_df=10,                        # minimum reqd occurences of a word 
                             stop_words=stop_words,             # remove stop words
                             lowercase=True,                   # convert all words to lowercase
                             token_pattern='[a-zA-Z0-9]{3,}')  # num chars > 3


#%%
features = vectorizer.fit_transform(corpus).todense()


#%%
range_n_clusters= range(10,2001,100)
sse = []
for n_clusters in range_n_clusters:
    kmeans_model= MiniBatchKMeans(n_clusters, batch_size=200).fit(features)
    sse.append(kmeans_model.inertia_)
    print(n_clusters)
print(sse)
#%%
##range_n_clusters= range(10,101,10)
#sse=[12011668.406510657, 11748264.97404771, 11837031.248091476, 12125361.078760743, 11901080.665186785, 11476987.38165655, 11361799.540334808, 11385328.062169634, 11712111.19644797, 11729303.019994028]
import matplotlib.pyplot as plt
from matplotlib.collections import EventCollection
fig = plt.plot(range_n_clusters,sse,'-r')
plt.xlabel('Number of Clusters')
plt.ylabel('silhouette score')
plt.suptitle('How to choose the Number of clusters for KMeans')

#%%
