from dataclasses import dataclass
from enum import Enum

from decouple import config

APP_NAME = "cdktf-gcp-cloud-functions-trial"
REGION = config("REGION", "us-east1")
ENVIRONMENT = config("ENV", "dev")


class StrEnum(str, Enum):
    """Base class for String Enum.

    Args:
        str (str): String object
        Enum (Enum): Enum class

    Returns:
        Enum: String Enum
    """

    def __str__(self):
        """Represent value as string.

        Returns:
            str: String representation
        """
        return str(self.value)


class Env(StrEnum):
    """Constants for environment names.

    Args:
        StrEnum (Enum): String Enum class
    """

    DEV = "dev"
    STAGING = "staging"
    PRODUCTION = "prod"


@dataclass
class EnvData:
    """Data class to hold environment data."""

    name: str

    def env_name(self, item_name):
        """Generate environment specific name.

        Args:
            item_name (str): Name of item.

        Returns:
            str: Environment specific name.
        """
        return f"{item_name}-{self.name}".lower()


dev_environment_data = EnvData(name=str(Env.DEV))

staging_environment_data = EnvData(name=str(Env.STAGING))

prod_environment_data = EnvData(name=str(Env.PRODUCTION))
