import pickle
import sys
import os
import socket
import platform
from subprocess import DEVNULL
from pathlib import Path
from typing import TypeVar
from time import sleep

import psutil

STATUS = {
    "Linux": "sleeping",
    "Darwin": "running",
    "Windows": "running"
}

Server_t = TypeVar("Server_t", bound="Server")


class ServerError(Exception):
    pass


class Server:
    statefile = "state.pickle"

    def __init__(self, servedir: Path | str, workdir: Path | str, port: int | None = None) -> None:
        self.servedir = Path(servedir)
        self.workdir = Path(workdir)
        self.port = port

        self._pid = None
        self._statepath = self.workdir / self.statefile

        if not os.path.exists(self.workdir):
            os.makedirs(self.workdir)


    def start(self) -> None:
        if self.port is None:
            self.port = self._find_port()
        
        proc = psutil.Popen([sys.executable, "-u", "-m", "http.server", str(self.port)],
                            cwd=self.servedir,
                            stderr=DEVNULL,
                            stdout=DEVNULL)

        sleep(0.1)

        # Check if the subprocess is still running
        if proc.status() != STATUS[platform.system()]:
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

        if os.path.exists(self._statepath):
            os.remove(self._statepath)

        self._pid = None


    def _save(self) -> None:
        with open(self._statepath, "wb") as f:
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


    @classmethod
    def load(cls, workdir) -> Server_t:
        try:
            with open(workdir / cls.statefile, "rb") as f:
                server = pickle.load(f)
        except FileNotFoundError as exc:
            raise ServerError("Server information not found.") from exc
        return server
