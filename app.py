from flask import Flask
from os import environ
from dotenv import load_dotenv, find_dotenv
import asyncio


# Import controller functions
from search_database.services import fetch_data, search_videos, initiate_fetch

from os import environ
from dotenv import load_dotenv, find_dotenv
import secrets

load_dotenv(find_dotenv())

# Generate a 32-byte secret key
# secret_key = secrets.token_hex(32)

SECRET_KEY = secrets.token_hex(32)


app = Flask(__name__)
app.secret_key = SECRET_KEY

# # Route for home page
@app.route("/")
def hello_world():
    return "<p>Ritika, Mishra!</p>"

# Route for querying database
@app.route("/fetch_data")
@app.route("/fetch_data/<int:page_number>")
def query_DB(page=1):
    return asyncio.run(fetch_data(page))

# Route for searching video titles and descriptions
@app.route("/search_videos")
@app.route("/search_videos/<keyword>")
def search_DB(tag=''):
    print(tag)
    return asyncio.run(search_videos(tag))

# Route for starting the fetching process from YouTube
@app.route("/initiate_fetch")
def start_fetching():
    asyncio.run(initiate_fetch())
    return "Started fetching latest YouTube videos!"

if __name__ == "__main__":
    app.run(debug=True)
