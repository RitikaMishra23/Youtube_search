import requests
from search_database.db import connect_db
from flask import jsonify
import asyncio
import aiohttp
import time
from os import environ
from dotenv import load_dotenv, find_dotenv

load_dotenv(find_dotenv())

YOUTUBE_API_BASE_URL = environ.get('YOUTUBE_API_BASE_URL')
API_KEY = environ.get('API_KEY')

# Create a global variable to hold the database connection
db_collection = None

# Initialize the database connection asynchronously
async def init_db():
    global db_collection
    db_collection = connect_db()

# Controller for querying paginated video data from the database
async def fetch_data(page_number):
    items_per_page = 20
    page_number = int(page_number)

    # Ensure the db_collection is initialized before making DB queries
    if db_collection is None:
        await init_db()

    cursor = db_collection.find().skip((page_number - 1) * items_per_page).limit(items_per_page).sort('publishTime', -1)
    video_data = []

    async for record in cursor:
        video_data.append(record)
    
    return jsonify(video_data)

# Controller for searching videos by a keyword in the title/description
async def search_videos(keyword):
    if db_collection is None:
        await init_db()

    await db_collection.create_index([('title', "text"), ('description', "text")])
    cursor = db_collection.find({"$text": {"$search": keyword}}) 
    video_data = []
    
    async for record in cursor:
        video_data.append(record)

    return jsonify(video_data)


# Controller to fetch the latest video data from YouTube API
# async def fetch_video_details():
#     page_token = ""
#     while True:
#         params = {
#             "part": "snippet",
#             "maxResults": 50,
#             "type": "video",
#             "key": API_KEY,
#             "pageToken": page_token,
#             "publishedAfter": "2020-01-01T00:00:00Z",  # Filter for recent videos
#             "order": "date",  # Sort videos by date
#             "q": "Bollywood Music" 
#         }

#         try:
#             response = aiohttp(YOUTUBE_API_BASE_URL, params=params)
#             response.raise_for_status()
#         except requests.exceptions.RequestException as e:
#             print(f"API request error: {e}")
#             time.sleep(60) 
#             continue

#         video_list = []
#         if response.status_code == 200:
#             json_data = response.json()
#             if 'nextPageToken' in json_data:
#                 page_token = json_data['nextPageToken']
#             else:
#                 page_token = ''

#             for item in json_data.get("items", []):
#                 video_id = item.get("id", {}).get("videoId")
#                 snippet_info = item.get("snippet", {})
                
#                 video = {
#                     '_id': video_id,
#                     'title': str(snippet_info.get('title')),
#                     'description': snippet_info.get('description'),
#                     'thumbnail_url': snippet_info.get('thumbnails', {}).get('default', {}).get('url'),
#                     'publish_time': snippet_info.get('publishTime')
#                 }
#                 video_list.append(video)

#             # Insert video data into MongoDB
#             for video in video_list:
#                 time.sleep(2)  # Delay to avoid rate limiting
#                 if await db_collection.find_one({"_id": video["_id"]}):
#                     print('Duplicate video found, skipping...')
#                 else:
#                     await db_collection.insert_one(video)
#                     print(f"Video data saved to database: {video['_id']}")
#         time.sleep(10)  # Wait for the next API request
import aiohttp

async def fetch_video_details():
    page_token = ""
    while True:
        params = {
            "part": "snippet",
            "maxResults": 50,
            "type": "video",
            "key": API_KEY,
            "pageToken": page_token,
            "publishedAfter": "2020-01-01T00:00:00Z",  # Filter for recent videos
            "order": "date",  # Sort videos by date
            "q": "Bollywood Music"
        }

        try:
            async with aiohttp.ClientSession() as session:
                async with session.get(YOUTUBE_API_BASE_URL, params=params) as response:
                    response.raise_for_status()
                    json_data = await response.json()
                    
                    video_list = []
                    if 'nextPageToken' in json_data:
                        page_token = json_data['nextPageToken']
                    else:
                        page_token = ''

                    for item in json_data.get("items", []):
                        video_id = item.get("id", {}).get("videoId")
                        snippet_info = item.get("snippet", {})

                        video = {
                            '_id': video_id,
                            'title': str(snippet_info.get('title')),
                            'description': snippet_info.get('description'),
                            'thumbnail_url': snippet_info.get('thumbnails', {}).get('default', {}).get('url'),
                            'publish_time': snippet_info.get('publishTime')
                        }
                        video_list.append(video)

                    # Insert video data into MongoDB
                    for video in video_list:
                        time.sleep(2)  # Delay to avoid rate limiting
                        if await db_collection.find_one({"_id": video["_id"]}):
                            print('Duplicate video found, skipping...')
                        else:
                            await db_collection.insert_one(video)
                            print(f"Video data saved to database: {video['_id']}")
        except aiohttp.ClientError as e:
            print(f"API request error: {e}")
            time.sleep(60)  # Wait before retrying

        time.sleep(10)  # Wait before making the next request


# Function to initiate the fetching process
async def initiate_fetch():
    print('Starting video data fetch...')
    await fetch_video_details()

