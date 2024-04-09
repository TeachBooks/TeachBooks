import pickle
import sys
import os

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
    dir: Path
    workdir: Path
    __pid: int | None = None

    def __post_init__(self):
        if not os.path.exists(self.workdir):
            os.makedirs(self.workdir)

    def start(self) -> None:
        proc = psutil.Popen([sys.executable, "-u", "-m", "http.server"],
                            cwd=self.dir,
                            stderr=DEVNULL,
                            stdout=DEVNULL) # Does this work on Windows?

        sleep(0.1)

        # Check if the subprocess is still running
        if proc.status() != "running":
            proc.terminate()
            raise RuntimeError("Error launching the server. Perhaps a server is already running?")
        else:
            self.__pid = proc.pid
            self._save()


    def stop(self) -> None: psutil.Process(pid=self.__pid).terminate()        


    def _save(self) -> None:
        with open(self.workdir / "state.pickle", "wb") as f:
            pickle.dump(self, f)


    @staticmethod
    def load(workdir) -> Server_t:
        with open(workdir / "state.pickle", "rb") as f:
            server = pickle.load(f)
        return server
