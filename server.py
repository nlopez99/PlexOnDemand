import os
import requests
from app.movie import MovieSearch
from app.ftp import FTPClient
from app.torrent import TorrentClient
from app.utils import clean_movie_title
from dotenv import load_dotenv
from fastapi import FastAPI, Request, Response, HTTPException
import redis
from twilio.twiml.messaging_response import MessagingResponse, Message
from typing import Dict, List, Optional, Tuple


# Services

app = FastAPI()
cache = redis.Redis(host="redis", port=6379)
movie_search = MovieSearch()
torrent_client = TorrentClient()


# Utility Functions


def create_movie_response(response: str, cover_url: str = "") -> str:
    response = MessagingResponse()
    message = Message()
    message.body(response)
    if cover_url:
        message.media(cover_url)
    response.append(message)
    return str(response)


@app.post("/movies")
async def search_movies(request: Request) -> Response:

    message_data = await request.form()
    body: str = message_data["Body"].lower()

    possible_search: str = body[:6]
    possible_yes: str = body[:3]
    possible_no: str = body[:2]
    possible_status: str = body[:5]

    # parse body for what user is trying to do
    if "search" == possible_search:

        # everything after `search` keyword
        movie_title: str = body[7:]
        movie_title: str = clean_movie_title(movie_title=movie_title)
        movie: Dict = movie_search.search_movies(movie_title=movie_title)
        title, cover_url = movie_search.get_movie_data(movie_json=movie)

        cache.set("movie", title)

        response = create_movie_response(
            cover_url=cover_url,
            response=f"Were you looking for {title}",
        )

        return Response(content=response, media_type="application/xml")

    elif "yes" == possible_yes:
        movie_title = cache.get("movie")
        movie_json: Dict = movie_search.search_movies(movie_title=movie_title)
        torrent_url: str = movie_search.get_movie_url(movie_json=movie_json)
        movie_filepath: bool = movie_search.download_torrent_file(torrent_url)
        if movie_filepath:
            print(f"Downloaded Successfully: {movie_filepath}")
            print("Adding to Qbittorent Client...")

            try:
                torrent_client.download_torrent(filepath=movie_filepath)

            except Exception as e:
                print(str(e))

            response = create_movie_response(
                response=f"Downloading {str(movie_title)} Now"
            )
            return Response(content=response, media_type="application/xml")

        else:
            response = create_movie_response(response="Sorry something went wrong:/")
            return Response(content=response, media_type="application/xml")

    elif "no" == possible_no:
        response = create_movie_response(
            response="Sorry:/ Please Try to Match Your Search as Close as Possible"
        )
        return Response(content=str(response), media_type="application/xml")

    elif possible_status:
        status = torrent_client.get_status()
        return Response(
            content="\n".join(s for s in status), media_type="application/xml"
        )

    else:
        raise HTTPException(status_code=400, detail="Unknown Command")
