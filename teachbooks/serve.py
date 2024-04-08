import pickle
import sys

import psutil

from subprocess import DEVNULL
from pathlib import Path
from dataclasses import dataclass


@dataclass
class Server:
    dir: Path
    workdir: Path
    __pid: int = None

    def start(self) -> None:
        proc = psutil.Popen([sys.executable, "-u", "-m", "http.server"],
                            cwd=self.dir,
                            stdout=DEVNULL) # Does this work on Windows?

        self.__pid = proc.pid
        self._save()

    def stop(self) -> None: psutil.Process(pid=self.__pid).terminate()        


    def _save(self) -> None:
        with open("test", "wb") as f:
            pickle.dump(self, f)

    @staticmethod
    def load() -> None:
        with open("test", "rb") as f:
            data = pickle.load(f)
        return data
