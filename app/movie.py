import os
import re
from typing import Dict, Tuple

import requests


class MovieService:
    """ Class for searching and downloading movies """

    def __init__(self):
        """ Initializes Endpoint and Download Directory """
        self.base_api_url: str = "https://yts.mx/api/v2/"
        self.movies_endpoint: str = "list_movies.json"
        self.download_dir: str = "/media"

    def search_movies(self, movie_title: str) -> Dict:
        """ Searches Movie by Title, Returns Movie Data as JSON """
        params = {"limit": 1, "query_term": movie_title, "sort_by": "download_count"}
        search_url = self.base_api_url + self.movies_endpoint

        try:
            response = requests.get(search_url, params=params)
            assert response.ok

            movie_json = response.json()
            assert movie_json["status"] == "ok"

            # Gets only data for the movies, not response
            return movie_json["data"]["movies"][0]

        except Exception as e:
            print(str(e))

    def get_movie_url(self, movie_json: Dict) -> str:
        """ Return Movie Magnet URL from Movie ID """
        best_torrent = self.pick_most_seeds(movie_json["torrents"])
        return best_torrent["url"]

    def get_movie_data(self, movie_json: Dict) -> Tuple[str, str]:
        """ Gets Movie Full Name and Cover Picture Returns as Tuple """
        movie_title = movie_json["title_long"]
        movie_cover_url = movie_json["medium_cover_image"]
        return movie_title, movie_cover_url

    def download_torrent_file(self, torrent_url: str) -> bool:
        """ Downloads a Torrent File for a Movie to be Consumed By Torrent Client"""
        try:
            response = requests.get(torrent_url, allow_redirects=True)
            content_header = response.headers.get("content-disposition")
            dirty_name = re.findall("filename=(.+)", content_header)[0]
            filename = "_".join(dirty_name.split()).strip('"')
            filepath = os.path.join(self.download_dir, filename)
            with open(filepath, "wb") as file:
                file.write(response.content)

            return filepath

        except requests.exceptions.HTTPError as e:
            print(str(e))
            return False

    @staticmethod
    def pick_most_seeds(torrents: Dict) -> Dict:
        """ Picks the Best Torrent Available Based on Most Seeds """
        sorted_torrents = sorted(torrents, key=lambda x: x["seeds"])
        most_seeds = list(sorted_torrents)[0]
        return most_seeds
