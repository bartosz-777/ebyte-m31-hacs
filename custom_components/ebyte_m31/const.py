"""Constants for the Ebyte M31 Modbus integration."""
from __future__ import annotations

from dataclasses import dataclass

from homeassistant.const import CONF_HOST, CONF_PORT

DOMAIN = "ebyte_m31"

DEFAULT_HOST = "192.168.1.100"
DEFAULT_PORT = 502

MODBUS_ADDRESS = 0
MODBUS_SLAVE = 1
DISCRETE_INPUT_COUNT = 8


@dataclass(frozen=True)
class BinarySensorDefinition:
    """Definition for one discrete input entity."""

    key: str
    name: str
    address: int
    icon: str | None = None


BINARY_SENSOR_DEFINITIONS: tuple[BinarySensorDefinition, ...] = tuple(
    BinarySensorDefinition(
        key=f"input_{index}",
        name=f"Discrete input {index}",
        address=index,
        icon="mdi:toggle-switch",
    )
    for index in range(DISCRETE_INPUT_COUNT)
)
