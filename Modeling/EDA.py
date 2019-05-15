#%% 
import os
import pandas as pd
import numpy as np
import re
import pickle
import matplotlib.pyplot as plt
import seaborn as sns
sns.set_style('whitegrid')
#%% 
data_path = 'files/read_in.pkl'
reviews = pd.read_pickle(data_path)
review = reviews.copy()
#%%
reviews.describe()

#%%
count_review = reviews.groupby('hotel_name').agg('count')['review']
plt.hist(count_review.values, bins = 75)
plt.title('Histogram of # reviews per hotel')

#%%
plt.hist(count_review[count_review.values<200].values, bins = 20)
plt.title('Histogram of # reviews per hotel')
#%%
sum(count_review.values < 50)

#%%
plt.hist(count_review[count_review.values>50].values, bins = 75)
plt.title('Histogram of # reviews per hotel')

#%%
count_review[count_review.values <= 50]

#%%
reviews.groupby('hotel_rating_review').agg('count')['review']

#%%
for i in reviews.columns[2:]:
    try : 
        print(reviews.groupby(i).agg('count')['review'])
    except:
        print("Not Compatible for ", i)

#%%
plt.scatter(reviews.groupby('hotel_rating_hotel').agg('mean')['hotel_rating_review'].index,reviews.groupby('hotel_rating_hotel').agg('mean')['hotel_rating_review'].values)
plt.title("Average hotel rating by review vs hotel rating in Trip Advisor")


#%%
review['hotel_name'] = reviews['hotel_name'].apply(lambda x: x if x in list(set(count_review[count_review.values > 50].index)) else np.NaN)


#%%
review = review.dropna(axis=0)

#%%
review.head()

#%%
plt.scatter(review.groupby('hotel_rating_hotel').agg('mean')['hotel_rating_review'].index,review.groupby('hotel_rating_hotel').agg('mean')['hotel_rating_review'].values)
plt.title("Average hotel rating by review vs hotel rating in Trip Advisor")


#%%
review.groupby('hotel_rating_hotel').agg('mean')['hotel_rating_review']

#%%
