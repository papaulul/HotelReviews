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
modelname = 'review.sav'
filename = 'files/review_kmeans.pkl'
hotel_path = 'files/hotel_info.pkl'
from sklearn.preprocessing import StandardScaler  # For scaling dataset
df = pd.read_pickle(filename)
hotel_info = pd.read_pickle(hotel_path)
print(hotel_info.shape)
hotel_info = hotel_info.merge(pd.DataFrame(df['hotel_name'].unique(), columns=['hotel_name']), how = 'right', on= 'hotel_name')

#%%
drop_col = ['hotel_name','url','low_price','high_price']
hotels = hotel_info['hotel_name'].values
df_quant = hotel_info.drop(drop_col,axis = 1)
df_quant['num_rooms'] = df_quant['num_rooms'].apply(lambda x: int(x) if isinstance(x,str) else 0)
#%%
ss = StandardScaler()
scaled_feature = ss.fit_transform(df_quant.values)
with open('files/quant_scaled.sav','wb') as fin:
    pickle.dump(ss, fin)
df_transformed = pd.DataFrame(scaled_feature,index = df_quant.index, columns = df_quant.columns)
#%%

range_n_clusters = range(5, 101, 5)
from sklearn.cluster import KMeans
sse = []
for n_clusters in range_n_clusters:
    kmeans_model = KMeans(n_clusters=n_clusters).fit(df_transformed)
    sse.append(kmeans_model.inertia_)
    print(n_clusters)

import matplotlib.pyplot as plt
from matplotlib.collections import EventCollection
fig = plt.plot(range_n_clusters,sse,'-r')
plt.xlabel('Number of Clusters')
plt.ylabel('silhouette score')
plt.suptitle('How to choose the Number of clusters for KMeans')
plt.savefig("silhouette1.png")

#%%
filename = "files/hotel.sav"

true_k = 30
model = KMeans(n_clusters=true_k,init='k-means++',n_jobs = 1,verbose=1)
model = model.fit(df_transformed)
pickle.dump(model, open(filename, 'wb'))
print("Model Done")

model = pickle.load(open(filename, 'rb'))
hotel_info['hotel_pred'] = np.nan
for i in range(0,len(df_transformed)):
    hotel_info['hotel_pred'].iloc[i] = model.predict([df_transformed.iloc[i]])
    print(i)

#%% 
df = df.merge(hotel_info[['hotel_name','hotel_pred']], how = 'inner', on = 'hotel_name')
#%%
df.to_pickle('files/review_final.pkl')

#%%
