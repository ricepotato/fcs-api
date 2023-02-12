import boto3
from mypy_boto3_dynamodb import DynamoDBServiceResource
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


@pytest.fixture
def dynamodb_resource(settings: config.Settings) -> DynamoDBServiceResource:
    dynamodb_resource = boto3.resource(
        "dynamodb",
        region_name=settings.region_name,
        aws_access_key_id=settings.aws_access_key,
        aws_secret_access_key=settings.aws_secret_key,
    )
    return dynamodb_resource
