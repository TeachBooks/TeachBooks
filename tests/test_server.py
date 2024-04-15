import pytest
import os

from pathlib import Path

from teachbooks.serve import Server

SERVE_DIR = Path(".")
WORK_DIR = Path("./.teachbooks")


@pytest.fixture
def server():
    server = Server(dir=SERVE_DIR, workdir=WORK_DIR, port=8000)
    return server

@pytest.fixture
def running_server(server):
    server.start()
    yield server
    server.stop()


@pytest.mark.parametrize(
    "port", [None, 8000]
)
def test_create(port):
    server = Server(dir=SERVE_DIR, workdir=WORK_DIR, port=port)
    assert server.dir == Path(".")
    assert server.workdir == Path("./.teachbooks")
    assert server.port == port
    assert server._pid == None


def test_start(running_server):
    server = running_server
    assert server.port is not None
    assert server._pid is not None
    assert server.url == "http://localhost:8000"

    
def test_save_and_load(running_server):
    running_server._save()
    
    new_server = Server.load(WORK_DIR)
    assert new_server.dir == running_server.dir
    assert new_server.workdir == running_server.workdir
    assert new_server.port == running_server.port
    assert new_server._pid == running_server._pid


def test_stop(server):
    server.start()
    server.stop()
    
    assert not os.path.exists(WORK_DIR / "server" / "state.pickle")
    assert server._pid == None