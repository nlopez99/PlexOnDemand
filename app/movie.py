import requests
import shutil


class MovieSearch:
    def __init__(self):
        self.base_api_url: str = "https://yts.mx/api/v2/"
        self.movies_endpoint: str = "list_movies.json"

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

    @staticmethod
    def pick_most_seeds(torrents: dict) -> dict:
        """ Picks the Best Torrent Available Based on Most Seeds """
        sorted_torrents = sorted(torrents, key=lambda x: x["seeds"])
        most_seeds = list(sorted_torrents)[0]
        return most_seeds

    def get_torrent_status() -> bool:
        """ Returns Status of a Torrent """
        pass
