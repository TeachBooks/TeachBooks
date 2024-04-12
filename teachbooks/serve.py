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
        if self.port is None:
            self.port = self._find_port()
        
        proc = psutil.Popen([sys.executable, "-u", "-m", "http.server", str(self.port)],
                            cwd=self.dir,
                            stderr=DEVNULL,
                            stdout=DEVNULL) # Does this work on Windows?

        sleep(0.1)

        # Check if the subprocess is still running
        if proc.status() != "running":
            proc.terminate()
            raise RuntimeError("Error launching the server. Perhaps a server is already running?")
        else:
            self._pid = proc.pid
            self._save()


    def stop(self) -> None: 
        psutil.Process(pid=self._pid).terminate()        


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
        with open(workdir / "server" / "state.pickle", "rb") as f:
            server = pickle.load(f)
        return server
