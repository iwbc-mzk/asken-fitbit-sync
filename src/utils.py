import logging
from logging import config
import os

import yaml

from .const import UNITS


def micrograms_to_iu(mcg: float) -> float:
    return mcg * 40


def salt_g_to_sodium_mg(salt: float) -> float:
    return salt * 1000 / 2.54


def remove_unit(nutrition_value: str) -> float:
    """Remove unit from nutrition value and convert to float."""

    for unit in UNITS:
        if nutrition_value.endswith(unit):
            return float(nutrition_value[: -UNITS[unit]["word_cnt"]].strip())

    return float(nutrition_value)


def get_logger(name: str) -> logging.Logger:
    """Get a logger with the specified name."""

    if not logging.getHandlerNames():
        conf_file = (
            r"./src/logging.conf.prd.yaml"
            if os.environ.get("ENV") == "production"
            else r"./src/logging.conf.dev.yaml"
        )
        with open(conf_file, "r") as f:
            conf = yaml.safe_load(f.read())
            config.dictConfig(conf)

    return logging.getLogger(name)
