import streamlit as st
import pandas as pd
import datetime
from PIL import Image
import pymongo

#DISPLAYING DATASET
#Reading csv file via pandas and add a button to display the loaded dataset and its length
st.header('**:blue[Twitter Scraping:]**')

df=pd.read_csv("tweets.csv")

st.text('')  

result=st.button('**_Click here to view a dataset_**')
if result:
    st.write(len(df.index))
    st.dataframe(df)

#functions to convert DataFrame to CSV,JSON and DICTIONARY    

def convert_df_csv(df):
    return df.to_csv()

def convert_df_json(df):
    return df.to_json()

def convert_df_dict(df):
    return df.to_dict('records')

# Adding downlaod buttons to down DF as CSV and JSON

csv=convert_df_csv(df)
Json_data=convert_df_json(df)

st.write('Click the below buttons to downlod the datset as **CSV** and **JSON** files')

col1,col2,col3,col4=st.columns(4)

with col1:
    st.download_button(label='Download CSV',
                       data=csv,
                       file_name='tweets.csv',
                       mime='text/csv')
with col2:
    st.download_button(label='Download JSON',
                       data=Json_data,
                       file_name='tweets.json',
                       mime='application/json')




df=pd.read_csv("tweets.csv")

# Defining a function to filter the data based on given hashtag

def filter_hashtag(hashtag):
    if hashtag:
        filtered_hashtag = df[df['Tweet'].str.contains(hashtag)]
        if not filtered_hashtag.empty:
            st.write('Number of tweets:',len(filtered_hashtag.index))
            st.write(filtered_hashtag)
            return filtered_hashtag
        else:
            st.write('No data found for the given hashtag')

hashtag = st.text_input(label='Please type your hashtag in the search bar')

filtered_data = filter_hashtag(hashtag)

# Adding downlaod buttons to down DF as CSV and JSON
#st.write('Click the below buttons to downlod the #hashtag filtered datset as **CSV** and **JSON** files')

col1,col2,col3,col4=st.columns(4)
with col1:    
    if filtered_data is not None:       
        csv = convert_df_csv(filtered_data)
        st.download_button(label='Download CSV', data=csv, file_name='twitter.csv', mime='text/csv')

with col2:
    if filtered_data is not None:
        json = convert_df_json(filtered_data)
        st.download_button(label='Download JSON', data=json, file_name='twitter.json', mime='application/json')
    
st.text('')  
st.text('') 
st.text('')   

df=pd.read_csv("tweets.csv")

# Convert the date column to datetime

df['Date'] = pd.to_datetime(df['Date'])

begin_date = st.date_input('Enter the begin state', value=df['Date'].min().date())
start_date = pd.to_datetime(begin_date).tz_localize('UTC')

end_date = st.date_input('Enter the end date', value=df['Date'].max().date())
end_date = pd.to_datetime(end_date).tz_localize('UTC') + pd.DateOffset(days=1)

result = df[(df['Date'] >= start_date) & (df['Date'] < end_date)]

#display as DataFrame

st.write('Number of tweets',len(result.index))
display=st.button('**Click here to view the filtered dataset**')

if display:
    st.write(result)
    
# Adding downlaod buttons to down DF as CSV and JSON

st.write('Click the below buttons to downlod the filtered datset as **CSV** and **JSON** files')   

col1,col2,col3,col4=st.columns(4)

with col1:
    if result is not None:
        csv = convert_df_csv(result)    
        st.download_button(label='Download CSV', data=csv, file_name='twitter_datefilter.csv', mime='text/csv')
with col2:
    if result is not None:
        json = convert_df_json(result)
        st.download_button(label='Download JSON', data=json, file_name='twitter_hashtag.json', mime='application/json')
        
#getting input from user such as Database,collection, number tweets

file="tweets.csv"

num_tweets = st.number_input(label='Enter the number of tweets to upload', min_value=1, step=1,max_value=10000)
df=pd.read_csv(file,nrows=num_tweets)
link=pymongo.MongoClient("mongodb://localhost:27017")
db_name=st.text_input(label='Enter the existing DB name to connect or new DB name to create')
db_collection=st.text_input(label='Enter the collection name or new collection name to create')

#adding a button to upload the data to MongoDB

db_upload=st.button(label='**_Upload to MongoDB_**')
if db_upload:
    db=link[db_name]
    Collection=db[db_collection]
    docs=convert_df_dict(df)
    Collection.insert_many(docs)
    st.write(f"{len(docs)} tweets uploaded to {db_name} : {db_collection}")