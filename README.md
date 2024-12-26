
## Project Overview
This project provides an API to fetch the latest YouTube videos based on a predefined search query. The videos are fetched from the YouTube API and stored in a MongoDB database. The server periodically fetches new video data asynchronously, storing key information such as video title, description, publishing datetime, and thumbnail URLs. A paginated API allows users to query the database and retrieve the stored video data in reverse chronological order.

## Requirements
Python 3.x
Flask
Flask-Async
aiohttp
pymongo
dotenv
MongoDB

## Installation
### Clone the Repository


```git clone (https://github.com/RitikaMishra23/Youtube_search.git)```

```cd YoutubeQuery pagination<br>```

### Create a .env file with the following content:

#### YouTube data v3 API:<br>
 https://developers.google.com/youtube/v3/getting-started .<br>
#### Search API reference:<br>
 https://developers.google.com/youtube/v3/docs/search/list<br>
To fetch the latest videos you need to specify these: type=video, order=date, publishedAfter=<SOME_DATE_TIME> <br>

YOUTUBE_API_BASE_URL=https://www.googleapis.com/youtube/v3/search <br>
API_KEY=<YOUR_YOUTUBE_API_KEY> <br>
#### Connect application with Mongodb server .<br>
   ###### Step 1 <br>
Login to Mongodb Atlas<br>
##### Step 2 <br>
Connect to Cluster and get Connection String with username , password and database name
##### Step 3 <br>
Get MONGODB_URL - MONGO_URI=mongodb+srv://<Connection_String><br>
MONGO_URI=<YOUR_MONGODB_URI> <br>
Replace <YOUR_YOUTUBE_API_KEY> and <YOUR_MONGODB_URI> with your actual YouTube API key and MongoDB URI.<br>

## Install Dependencies

Install the required Python packages:

```pip install -r requirements.txt```

### Run the Application


## API Endpoints
GET /fetch_data
Fetches video data from the database in a paginated format. You can pass the page_number as a URL parameter to retrieve a specific page.

Example:


```GET /fetch_data?page_number=1<br>```
```GET /search_videos/<keyword><br>```
Search videos based on the provided keyword in the video title or description.

Example:

```GET /search_videos/cricket```
```GET /initiate_fetch```
Starts the process of fetching the latest videos from the YouTube API in the background. This will fetch the latest videos and store them in the database.
## Results

<img width="959" alt="1" src="https://github.com/user-attachments/assets/89f3855b-0b96-410a-bd54-f1b290e68ca6" />
![Untitled design (1)](https://github.com/user-attachments/assets/31d4ae0e-6af5-4b3f-9c9d-6c646c8f87f1)

![Untitled design (2)](https://github.com/user-attachments/assets/af39173b-4b48-44a4-a1af-a68dabc142a2)

![Untitled design (3)](https://github.com/user-attachments/assets/892bbf2d-9c5c-4bea-85b3-dea2c7921228)

<img width="947" alt="3" src="https://github.com/user-attachments/assets/89bd00ea-9c03-4f0f-bc01-b8f1e90eff34" />


## Challenges
### MongoDB server activation<br>
It lead to 505 errors

### API Rate Limits:<br>
 The YouTube API has rate limits on how many requests can be made per day using a single API key. To ensure continuity, the solution involves using multiple API keys and switching to the next available key if one key exceeds its quota.
<img width="959" alt="4" src="https://github.com/user-attachments/assets/15bdc474-5109-4bf6-9722-0be0cff55967" />

<img width="959" alt="5" src="https://github.com/user-attachments/assets/92dd112c-f888-4e14-aa4e-cb3b9e5b535f" />



 




