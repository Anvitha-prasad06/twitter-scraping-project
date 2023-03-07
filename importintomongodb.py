import pymongo 
import pandas as pd
import json

client = pymongo.MongoClient("mongodb://localhost:27017")

df = pd.read_csv("tweets.csv")

data = df.to_dict(orient = "records")

db = client["twitterScrapper"]

print(db)

db.Twitter.insert_many(data)