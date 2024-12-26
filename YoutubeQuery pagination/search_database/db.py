# import motor.motor_asyncio
# from os import environ
# from dotenv import load_dotenv, find_dotenv
# load_dotenv(find_dotenv())

# mongo_uri = environ.get('MONGO_URI')

# async def connect_db():
#     print('Establishing connection to MongoDB...')
#     client = motor.motor_asyncio.AsyncIOMotorClient(mongo_uri, serverSelectionTimeoutMS=30000)
#     database = client.get_database('YouTubeVideos')
#     db_collection = database.video_search
#     print('Connected to MongoDB successfully!')
#     return db_collection

import pymongo
from os import environ, path
from dotenv import load_dotenv, find_dotenv
load_dotenv(find_dotenv())

# getting SECRET Mongo_URI
mongoURI = environ.get('MONGO_URI')

# connecting to database
from motor.motor_asyncio import AsyncIOMotorClient

async def connect_db():
    print('Connecting to MongoDB...')
    client = AsyncIOMotorClient(mongoURI, serverSelectionTimeoutMS=30000)
    database = client.get_database('YoutubeData')
    db = database.ysearch
    print('Connected to Database!')
    return db

