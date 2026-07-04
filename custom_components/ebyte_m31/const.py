"""Constants for the Ebyte M31 Modbus integration."""
from __future__ import annotations

from dataclasses import dataclass

from homeassistant.const import CONF_HOST, CONF_PORT

DOMAIN = "ebyte_m31"

DEFAULT_HOST = ""
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

bridgeModels = [
{"name": "AAAX4440G", "digital_inputs": 4, "digital_outputs": 4, "analog_inputs": 4, "analog_outputs": 0},
{"name": "AXAX4040G", "digital_inputs": 4, "digital_outputs": 4, "analog_inputs": 4, "analog_outputs": 0},
{"name": "AXAX8080G", "digital_inputs": 8, "digital_outputs": 8, "analog_inputs": 8, "analog_outputs": 0},
{"name": "AXXX8000G", "digital_inputs": 8, "digital_outputs": 8, "analog_inputs": 8, "analog_outputs": 0},
{"name": "XXAX0080G", "digital_inputs": 0, "digital_outputs": 8, "analog_inputs": 8, "analog_outputs": 0},
{"name": "AXXXA000G", "digital_inputs": 16, "digital_outputs": 0, "analog_inputs": 0, "analog_outputs": 0},
{"name": "XXAX00AOG", "digital_inputs": 0, "digital_outputs": 16, "analog_inputs": 0, "analog_outputs": 0},
{"name": "XAXX0800G", "digital_inputs": 0, "digital_outputs": 0, "analog_inputs": 8, "analog_outputs": 0},
{"name": "XAXA0404G", "digital_inputs": 0, "digital_outputs": 0, "analog_inputs": 4, "analog_outputs": 0},
{"name": "XXXA0008G", "digital_inputs": 0, "digital_outputs": 0, "analog_inputs": 0, "analog_outputs": 8},
{"name": "XFXX0800G", "digital_inputs": 0, "digital_outputs": 0, "analog_inputs": 8, "analog_outputs": 0},
{"name": "XGXX0800G", "digital_inputs": 0, "digital_outputs": 0, "analog_inputs": 8, "analog_outputs": 0}
]