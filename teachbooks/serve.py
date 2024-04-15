import pickle
import sys
import os
import socket

import psutil

from subprocess import DEVNULL
from pathlib import Path
from dataclasses import dataclass
from http.server import HTTPServer, BaseHTTPRequestHandler
from time import sleep
from typing import TypeVar, Type

Server_t = TypeVar("Server_t", bound="Server")


class ServerError(Exception):
    pass


@dataclass
class Server:
    dir: Path | str
    workdir: Path | str
    port: int | None = None
    _pid: int | None = None


    def __post_init__(self):
        self.dir = Path(self.dir)
        self.workdir = Path(self.workdir)

        if not os.path.exists(self.workdir / "server"):
            os.makedirs(self.workdir / "server")


    def start(self) -> None:
        # Check for an existing server and stop it
        try:
            self.load(self.workdir).stop()
        except (ServerError, psutil.NoSuchProcess):
            pass

        if self.port is None:
            self.port = self._find_port()
        
        proc = psutil.Popen([sys.executable, "-u", "-m", "http.server", str(self.port)],
                            cwd=self.dir,
                            stderr=DEVNULL,
                            stdout=DEVNULL)

        sleep(0.1)

        # Check if the subprocess is still running
        if proc.status() != "running":
            proc.terminate()
            raise RuntimeError("Error launching the server. Perhaps a server is already running on the selected port?")
        else:
            self._pid = proc.pid
            self._save()


    def stop(self) -> None:
        try:
            psutil.Process(pid=self._pid).terminate()
        except psutil.NoSuchProcess:
            pass

        if os.path.exists(self.workdir / "server" / "state.pickle"):
            os.remove(self.workdir / "server" / "state.pickle")

        self._pid = None


    def _save(self) -> None:
        with open(self.workdir / "server" / "state.pickle", "wb") as f:
            pickle.dump(self, f)


    @property
    def url(self) -> str:
        return f"http://localhost:{self.port}"


    @staticmethod
    def _find_port() -> int:
        # https://stackoverflow.com/a/1365284
        sock = socket.socket()
        sock.bind(('', 0))
        return sock.getsockname()[1]


    @staticmethod
    def load(workdir) -> Server_t:
        try:
            with open(workdir / "server" / "state.pickle", "rb") as f:
                server = pickle.load(f)
        except FileNotFoundError as exc:
            raise ServerError("Server information not found.") from exc
        return server
