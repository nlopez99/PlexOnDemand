from fastapi import FastAPI
from app.movie import MovieSearch
from app.ftp import FTPClient
from app.utils import clean_movie_title

app = FastAPI()
movie_search = MovieSearch()


@app.get("/movies")
async def search_movies(query: str):
    movie_title = clean_movie_title(movie_title=query)
    torrent_url = movie_search.get_movie_url(movie_title=movie_title)
    success = movie_search.download_torrent_file(torrent_url)
    return {"status": success}
