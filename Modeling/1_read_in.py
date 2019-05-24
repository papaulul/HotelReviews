#%%
import os
import pandas as pd
import numpy as np
import pymongo
from pymongo import MongoClient
print ('Mongo version', pymongo.__version__)
client = MongoClient('localhost', 27017)
db = client.reviews
reviews = db.full 
hotel = db.hotel
import re
import pickle

#%%
hotel = pd.DataFrame(list(hotel.find()), columns = ['_id', 'hotelname', 'hotel_rating', 'url', 'num_amenities', 'amenities', 'price_range', 'num_rooms'])
hotel.rename({'hotelname': 'hotel_name'}, axis=1 ,inplace = True)
#%%
reviews = pd.DataFrame(list(reviews.find()), columns = ['_id', 'review', 'hotel_name', 'travel_type', 'bubble', 'url'])
reviews.rename({'bubble': 'hotel_rating'}, axis=1 ,inplace = True)

#%%
df = [hotel, reviews]

for dframe in df: 
    dframe.drop('_id', axis=1, inplace = True)
    dframe['hotel_name'] = dframe['hotel_name'].apply(lambda x: x[0])

#%%
# Hotel Preprocessing 
def review_cleaning(text):
    # Removes More in list
    if "More" in text: 
        text.remove("More")
    # if list was just More or empty, turns to NA 
    if len(text) == 0:
        return np.NaN
    # Else returns the whole review 
    else: 
        return " ".join(text).strip()

reviews['review']=reviews['review'].apply(review_cleaning)
hotel['hotel_rating_hotel']=hotel['hotel_rating'].apply(lambda x: float(str(x).split(" ")[0]) if x != None else np.NaN)
reviews['hotel_rating_review']=reviews['hotel_rating'].apply(lambda x: int(str(x).split("_")[-1][0]) if x != None else np.NaN)
hotel.drop('hotel_rating', axis = 1 , inplace = True)
reviews.drop('hotel_rating', axis = 1 , inplace = True)


#%% 
hotel['low_price']=hotel['price_range'].apply(lambda x: int(x[0][1:]) if x[0] != "NAN" else np.NaN)
hotel['high_price']=hotel['price_range'].apply(lambda x: int(x[2][1:].replace(",","")) if x[0] != "NAN" else np.NaN)
hotel.drop('price_range', axis = 1, inplace = True)

#%%
# Expanding amenities to individual columns 
# Will hold all unique amenities
list_of_all_amenities = []
# Loop through each row checking to see if any new amenities can be added
for row in hotel['amenities']:
    for ele in row: 
        if ele not in list_of_all_amenities:
            list_of_all_amenities.append(ele)
# Sort to make it easier 
list_of_all_amenities = sorted(list_of_all_amenities)
# New df that will contain all new columns for amenities 
versus = hotel[['hotel_name','amenities']]
# Sort the existing amenities for each hotel
versus['amenities'] = versus['amenities'].apply(lambda x: sorted(x))
# Creates new columns for all amenities and set it as false
for i in list_of_all_amenities:
    versus[i] = False
# iterate over each value for amenities and set the index of the amenities to true    
for ind,value in enumerate(versus['amenities']):
    for ele in value:
        versus.set_value(ind,ele, True) 
# Returns columns back to hotel and removes amenities         
hotel = hotel.merge(versus.drop('amenities',axis=1), how = 'inner', on ="hotel_name").drop('amenities',axis=1)
hotel.to_pickle('files/hotel_info.pkl')
#%%
reviews['hotel_name'].loc[reviews[reviews['hotel_name'] == "Hotel Indigo Atlanta – Vinings"].index]= "Hotel Indigo Atlanta - Vinings"
reviews['hotel_name'].loc[reviews[reviews['hotel_name'] == 'DoubleTree by Hilton Hotel Atlanta North Druid Hills – Emory Area'].index]= 'DoubleTree by Hilton Hotel Atlanta North Druid Hills - Emory Area'
#%%
final = reviews.merge(hotel, how ='left', on= 'hotel_name')

final.to_pickle('files/read_in.pkl')

#%%

#%%
