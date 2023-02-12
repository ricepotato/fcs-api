import pydantic


class Settings(pydantic.BaseSettings):
    aws_access_key: str = pydantic.Field(default=None, env="AWS_ACCESS_KEY")
    aws_secret_key: str = pydantic.Field(default=None, env="AWS_SECRET_KEY")
    region_name: str = pydantic.Field(default="ap-northeast-2", env="AWS_REGION_NAME")

    mongodb_url: str = pydantic.Field(default=None, env="MONGODB_URL")
