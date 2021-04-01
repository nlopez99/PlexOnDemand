import os
import requests
from app.movie import MovieService
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
movie_service = MovieService()
torrent_client = TorrentClient()


# Utility Functions


def create_movie_response(message: str, cover_url: str = "") -> MessagingResponse:
    messaging_response = MessagingResponse()
    msg = messaging_response.message(message)
    if cover_url:
        msg.media(cover_url)
    return Response(content=str(messaging_response), media_type="application/xml")


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
        movie: Dict = movie_service.search_movies(movie_title=movie_title)
        if not movie:
            response = create_movie_response(
                message="Sorry can't find this movie:/ Please Try to Match Your Search as Close as Possible"
            )
            return response
        title, cover_url = movie_service.get_movie_data(movie_json=movie)

        cache.set("movie", title)

        response = create_movie_response(
            message=f"Were you looking for {title}? (yes/no)",
            cover_url=cover_url,
        )

        return response

    elif "yes" == possible_yes:
        movie_title = cache.get("movie")
        movie_json: Dict = movie_service.search_movies(movie_title=movie_title)

        torrent_url: str = movie_service.get_movie_url(movie_json=movie_json)
        movie_filepath: bool = movie_service.download_torrent_file(torrent_url)

        if movie_filepath:

            try:
                torrent_client.download_torrent(filepath=movie_filepath)
                response = create_movie_response(
                    message=f"Downloading {str(movie_title, 'utf-8')} Now:), please text 'status' for further updates!"
                )

            except Exception as e:
                response = create_movie_response(
                    message=f"Error Downloading {movie_title}, please text Nino this: {str(e)}"
                )

            return response

        else:
            response = create_movie_response(message="Sorry something went wrong:/")
            return response

    elif "no" == possible_no:
        response = create_movie_response(
            message="Sorry:/ Please Try to Match Your Search as Close as Possible"
        )
        return response

    elif possible_status:
        current_status = ""
        status = torrent_client.get_status()
        for name, percent, time_left in status:
            current_status += f"{name}: {percent} ({time_left})\n"

        response = create_movie_response(
            message=current_status,
        )

        return response

    else:
        response = create_movie_response(
            message="Sorry Unknown Command:/ Usage: 'Search Movie Title' or 'Status'"
        )
        return response
