import streamlit as st
import pandas as pd
import datetime
import pymongo

#DISPLAYING DATASET
#Reading csv file via pandas and add a button to display the loaded dataset and its length
st.title('**:red[Twitter Scraping]**')

df=pd.read_csv("tweets.csv")
st.text('')  

result=st.button('Click here for original dataset')
if result:
    st.write(len(df.index))
    st.dataframe(df)
    
def convert_df_csv(df):
    return df.to_csv()

def convert_df_json(df):
    return df.to_json()

def convert_df_dict(df):
    return df.to_dict('records')

csv=convert_df_csv(df)
Json_data=convert_df_json(df)

st.text('')
st.header("**:green[Filter the dataset :]**")

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

df=pd.read_csv("tweets.csv")

# Convert the date column to datetime

df['Date'] = pd.to_datetime(df['Date'])

begin_date = st.date_input('Enter the begin state', value=df['Date'].min().date())
start_date = pd.to_datetime(begin_date).tz_localize('UTC')

end_date = st.date_input('Enter the end date', value=df['Date'].max().date())
end_date = pd.to_datetime(end_date).tz_localize('UTC') + pd.DateOffset(days=1)

result = df[(df['Date'] >= start_date) & (df['Date'] < end_date)]
    
# Adding downlaod buttons to down DF as CSV and JSON
 
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

st.header("**:blue[Upload into MongoDB :]**")
file="tweets.csv"

num_tweets = st.number_input(label='Enter the number of tweets to upload', min_value=1, step=1,max_value=10000)
df=pd.read_csv(file,nrows=num_tweets)
link=pymongo.MongoClient("mongodb://localhost:27017")
db_name=st.text_input(label='Enter the existing DB name to connect or new DB name to create')
db_collection=st.text_input(label='Enter the collection name or new collection name to create')

#adding a button to upload the data to MongoDB

db_upload=st.button(label='Upload to MongoDB')
if db_upload:
    db=link[db_name]
    Collection=db[db_collection]
    docs=convert_df_dict(df)
    Collection.insert_many(docs)
    st.write(f"{len(docs)} tweets uploaded to {db_name} : {db_collection}")
