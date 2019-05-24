
#%% 
import os
import pandas as pd
import numpy as np
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.metrics.pairwise import euclidean_distances
import nltk; nltk.download('stopwords')
from nltk.corpus import stopwords
from sklearn.cluster import MiniBatchKMeans, KMeans
from sklearn import metrics
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics import adjusted_rand_score
import pickle
from sklearn.decomposition import PCA
filename = 'review.sav'

#%%
file_path = "files/eda.pkl"
review = pd.read_pickle(file_path)

#%%
corpus = review['review'].tolist()

#%%
stop_words = stopwords.words('english')
vectorizer = TfidfVectorizer(analyzer='word',
    max_df=.95,
    min_df=.05,   # minimum reqd occurences of a word 
    stop_words=stop_words, # remove stop words
    lowercase=True,  # convert all words to lowercase
    token_pattern='[a-zA-Z0-9]{3,}'  # num chars > 3
                            )
features=vectorizer.fit_transform(corpus).todense()
with open('files/vectorizer.pkl', 'wb') as fin:
    pickle.dump(vectorizer, fin)

#%%

range_n_clusters= range(10,711,100)
sse = []
for n_clusters in range_n_clusters:
    kmeans_model= MiniBatchKMeans(n_clusters, batch_size=1000).fit(features)
    sse.append(kmeans_model.inertia_)
    print(n_clusters)
print(sse)
import matplotlib.pyplot as plt
from matplotlib.collections import EventCollection
fig = plt.plot(range_n_clusters,sse,'-r')
plt.xlabel('Number of Clusters')
plt.ylabel('silhouette score')
plt.suptitle('How to choose the Number of clusters for KMeans')
plt.savefig('silhouette.png')
true_k = 200
rev_model = KMeans(n_clusters=true_k,init='k-means++',n_jobs = 1,verbose=1)
rev_model = rev_model.fit(features)
pickle.dump(rev_model, open(filename, 'wb'))
print("Model Done")


features_fit = vectorizer.fit(corpus)
rev_model = pickle.load(open(filename, 'rb'))
review['review_trans'] = review['review'].apply(lambda x: features_fit.transform([x]).todense())
preds = []
for i in review['review_trans'].values:
    preds.append(rev_model.predict(i))
review['review_preds'] = preds
review.to_pickle('files/review_kmeans.pkl')
print(review[['review','review_preds']].head())
#%%
