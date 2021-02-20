import os
import requests
from dotenv import load_dotenv
from fastapi import FastAPI, Request, Response, HTTPException
from client.torrent import TorrentClient
from client.ftp import FTPClient
from twilio.twiml.messaging_response import MessagingResponse


load_dotenv()
app = FastAPI()
MOVIE_API_URL = "http://server:5000/"


@app.post("/download")
async def download_movie(filename: str):
    pass


@app.post("/search")
async def search_movies(request: Request):
    message_data = await request.form()
    body = message_data["Body"].lower()

    if "search" not in body:
        raise HTTPException(status_code=400, detail="Missing Search Command")

    split_message = body.split("search ")

    if len(split_message) == 2:
        movie_title = split_message[-1]

    else:
        raise HTTPException(status_code=400, detail="Error in Search Command")

    params = {"query": movie_title}
    movie_resp = requests.get(MOVIE_API_URL + "movies", params=params)
    print(movie_resp.status_code)
    response = MessagingResponse()
    response.message(f"You said: {body}")

    return Response(content=str(response), media_type="application/xml")
