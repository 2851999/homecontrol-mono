from homecontrol_base_api.config.base import Config

from pydantic.dataclasses import dataclass


@dataclass
class TestConfigData:
    value: str


class TestConfig(Config[TestConfigData]):

    def __init__(self):
        super().__init__("test.json", TestConfigData)


config = TestConfig()
print(config._data)
