from __future__ import annotations
import yaml
from pydantic import BaseModel


def read_config(file: str) -> ConfigList:
    with open(file) as f:
        confs = ConfigList(confs=yaml.load(f))
    return confs


class ConfigList(BaseModel):
    confs: list[Config]


class Config(BaseModel):
    title: str
    twitter: str
    endpoint: str


ConfigList.update_forward_refs()
