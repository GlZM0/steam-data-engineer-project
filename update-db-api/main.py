import pandas as pd
from datetime import datetime
import boto3
from pymongo.mongo_client import MongoClient
from pymongo.server_api import ServerApi
from botocore.exceptions import ClientError
import pytz
import os
import logging

s3 = boto3.client('s3')
logger = logging.getLogger()
logger.setLevel(logging.INFO)

def lambda_handler(event, context):
    uri = <MongoDB Atlas uri>
    client = MongoClient(uri, server_api=ServerApi('1'))
    db = client[<database>]
    collection = db[<collection>]
    
    client.db_name.command('ping')
    
    bucket = event['Records'][0]['s3']['bucket']['name']
    key = event['Records'][0]['s3']['object']['key']
    current_datetime = datetime.now(pytz.utc)
    dict_list = []
    item_list = [] 

    response = s3.get_object(Bucket=bucket, Key=key)
    data = response['Body']

    df = pd.read_csv(data, sep=";")
    df['condition'] = df['condition'].where(pd.notnull(df['condition']), None)

 
    for index, row in df.iterrows():
        row_dict = row.to_dict()
        dict_list.append(row_dict)

    for record in df.to_dict(orient="records"):
        existing_item = collection.find_one({"name": record["name"], "condition": record["condition"]})
        if(existing_item):
            print("Old item details: ", existing_item["_id"], existing_item["name"], "Price: ", existing_item["price"])
            print("New item details: ", record["name"], "Price: ", record["price"])
            collection.update_one({"_id": existing_item["_id"]}, {"$set": {"price": record["price"], "color": record["color"], "colorHex": record["colorHex"], "updatedAt": current_datetime}})
            print(" ")
        else:
            print("New item: ", record["name"], "Price: ", record["price"], "added to db")
            record["updatedAt"] = current_datetime
            collection.insert_one(record)
            print(" ")
        
    return {'statusCode': 200, 'body': 'File processed and uploaded successfully'}