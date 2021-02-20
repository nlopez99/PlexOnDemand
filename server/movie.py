import requests
import re
import os


class MovieSearch:
    def __init__(self):
        self.base_api_url: str = "https://yts.mx/api/v2/"
        self.movies_endpoint: str = "list_movies.json"
        self.download_dir: str = "/media"

    def get_movie_url(self, movie_title: str) -> str:
        """ Return Movie Magnet URL from Movie ID """

        params = {"limit": 1, "query_term": movie_title, "sort_by": "download_count"}
        search_url = self.base_api_url + self.movies_endpoint
        try:
            response = requests.get(search_url, params=params)
            assert response.ok

            movie_json = response.json()
            assert movie_json["status"] == "ok"

            movie = movie_json["data"]["movies"][0]
            best_torrent = self.pick_most_seeds(movie["torrents"])

            return best_torrent["url"]

        except Exception as e:
            print(str(e))

    def download_torrent_file(self, torrent_url: str) -> bool:
        """ Downloads a Torrent File for a Movie to be Consumed """
        try:
            response = requests.get(torrent_url, allow_redirects=True)
            content_header = response.headers.get("content-disposition")
            dirty_name = re.findall("filename=(.+)", content_header)[0]
            filename = "_".join(dirty_name.split()).strip('"')
            filepath = os.path.join(self.download_dir, filename)
            with open(filepath, "wb") as file:
                file.write(response.content)

            return True

        except requests.exceptions.HTTPError as e:
            print(str(e))

    @staticmethod
    def pick_most_seeds(torrents: dict) -> dict:
        """ Picks the Best Torrent Available Based on Most Seeds """
        sorted_torrents = sorted(torrents, key=lambda x: x["seeds"])
        most_seeds = list(sorted_torrents)[0]
        return most_seeds