import pytest
import dotenv
import pathlib

from fcs import config


@pytest.fixture
def env():
    env_path = pathlib.Path(__file__).parent.parent.parent / ".env"
    assert env_path.exists()
    dotenv.load_dotenv(dotenv_path=env_path)
    yield


@pytest.fixture
def settings(env):
    yield config.Settings()
