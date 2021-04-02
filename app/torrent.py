""" Torrent Service """

import os
from typing import List, Tuple

from dotenv import load_dotenv
from qbittorrent import Client

load_dotenv()


class TorrentClient:
    """ Class to Interface with the Qbittorent Client """

    def __init__(self):
        self.download_dir: str = "/media"
        self.client: Client = Client("http://qbittorrent:8080")
        self.client.login("admin", "adminadmin")

    def get_torrent_file(self) -> str:
        """ Gets Torrent File from Download Directory """
        # grab first and only torrent file from directory
        torrent_file: str = [
            file
            for file in os.listdir(self.download_dir)
            if os.path.isfile(os.path.join(self.download_dir, file))
        ][0]
        return os.path.join(self.download_dir, torrent_file)

    @property
    def is_torrent_active(self) -> bool:
        """ Returns True/False if a torrent is active """
        return bool(self.client.torrents(filter="downloading"))

    def download_torrent(self, filepath: str) -> None:
        """ Adds .torrent file to Qbittorent Downloads """
        with open(filepath, "rb") as torrent_file:
            self.client.download_from_file(torrent_file)

    def get_status(self) -> List[Tuple[str, str, str]]:
        """ Gets Name, Percent Downloaded, and Time Left for Dowloading Torrents """
        torrents = self.client.torrents(filter="downloading")
        torrents_statuses = []
        for torrent in torrents:
            name = torrent["name"]

            amount_left = torrent["amount_left"]
            downloaded = torrent["downloaded"]
            pct_rounded = round((downloaded / amount_left) * 100, 2)

            # convert to min from seconds
            est_time = torrent["eta"]
            time_left = round(est_time / 60, 2)

            torrents_statuses.append((name, f"{pct_rounded}%", f"{time_left} minutes"))

        return torrents_statuses
