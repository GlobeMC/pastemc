from typing import Annotated

import yaml
from loguru import logger
from pydantic import AfterValidator, BaseModel, model_validator


class S3Settings(BaseModel, validate_assignment=True):
    access_key: str
    secret_key: str
    region: str | None = None
    endpoint: str
    bucket: str
    subpath: str = "/"
    secure: bool = False
    public_endpoint: Annotated[
        str, AfterValidator(lambda v: v.removesuffix("/"))
    ] | None = None

    @property
    def internal_endpoint(self):
        return f"{'https' if self.secure else 'http'}://{self.endpoint}/{self.bucket}"

    @model_validator(mode="after")
    def check_public_endpoint(self):
        if self.public_endpoint is None:
            self.public_endpoint = self.internal_endpoint
            logger.info(f"automatically set public endpoint: {self.public_endpoint}")
        return self


class AppSettings(BaseModel):
    s3: S3Settings


SETTINGS = AppSettings(
    **yaml.load(open(".config.yaml", encoding="utf-8"), yaml.SafeLoader)
)

logger.info("settings loaded")
