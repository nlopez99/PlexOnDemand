import os
from ftplib import FTP, error_perm, error_reply
from dotenv import load_dotenv
from socket import error as SocketError


load_dotenv()


class FTPClient:
    def __init__(self):
        self.server_host: str = None
        self.server_port: str = None
        self.server_ftp_dir: str = None
        self.torrent_dir: str = None
        self.ftp_user: str = os.environ.get("FTP_LOGIN")
        self.ftp_pass: str = os.environ.get("FTP_PASS")
        self.client: FTP = self.connect_client()

    def __enter__(self):
        self.client.getwelcome()

    def __exit__(self):
        self.client.close()

    @property
    def connection_status(self) -> bool:
        try:
            self.client.sendcmd("NOOP")
            return True

        except (SocketError, error_perm, error_reply):
            return False

    def connect_client(self) -> None:
        try:
            client = FTP(
                host=self.server_host,
                port=self.server_port,
                user=self.ftp_user,
                passwd=self.ftp_pass,
            )
            client.sendcmd("NOOP")
            return client

        except (SocketError, error_perm, error_reply) as e:
            print(str(e))

    def tranfer_file(self, filename) -> None:
        with open(filename, "rb") as file:
            self.client.storbinary(f"STOR {filename}", file)