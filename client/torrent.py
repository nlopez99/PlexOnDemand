from dotenv import load_dotenv
from qbittorrent import Client
from typing import Tuple, List
import os


load_dotenv()


class TorrentClient:
    def __init__(self):
        self.download_dir: str = "/home/user/Downloads"
        self.client: Client = Client("http://qbittorrent:8080")
        self.client.login("admin", "adminadmin")

    def get_torrent_file(self) -> str:
        """ Gets Torrent File from Download Directory """
        torrent_files = [
            file
            for file in os.listdir(self.download_dir)
            if os.path.isfile(os.path.join(self.download_dir, file))
        ]
        return torrent_files[0] if torrent_files else ""

    @property
    def is_torrent_active(self) -> bool:
        """ Returns True/False if a torrent is active """
        return bool(self.client.torrents(filter="downloading"))

    def download_torrent(self, filename: str) -> None:
        """ Adds .torrent file to Qbittorent Downloads """
        torrent_path = os.path.join(self.download_dir, filename)
        with open(torrent_path, "rb") as torrent_file:
            self.client.download_from_file(torrent_file)
