from dotenv import load_dotenv
from qbittorrent import Client
from typing import Tuple, List
import os


load_dotenv()


class TorrentClient:
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
