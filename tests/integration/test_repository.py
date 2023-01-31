import boto3

from fcs import config, repository


def test_repository(settings: config.Settings):
    dynamodb_resource = boto3.resource(
        "dynamodb",
        region_name=settings.region_name,
        aws_access_key_id=settings.aws_access_key,
        aws_secret_access_key=settings.aws_secret_key,
    )
    repo = repository.DynamoRepository(dyn_resource=dynamodb_resource)
    tables = repo.list_tables()
    assert tables
