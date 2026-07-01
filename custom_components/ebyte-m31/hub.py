from __future__ import annotations

import logging
import struct
import threading
from typing import TYPE_CHECKING

from pymodbus.client import ModbusTcpClient
from pymodbus.exceptions import ModbusException

from .const import DTYPE_FLOAT32, DTYPE_INT16, DTYPE_UINT16, DTYPE_UINT32, REG_INPUT

if TYPE_CHECKING:
    from homeassistant.core import HomeAssistant

_LOGGER = logging.getLogger(__name__)

_MAX_REGISTERS_PER_READ = 125
_MODBUS_TIMEOUT = 5  # seconds per request
_VALIDATION_REGISTER_ADDRESS = 1004


class ModbusNotEnabledError(Exception):
    """Raised when TCP connects but Modbus TCP is not active on the device."""

class ebyteM31Hub:
    """Manages the connection to the Ebyte M31 device."""

    def __init__(self, hass: HomeAssistant, host: str, port: int) -> None:
        """Initialize the hub."""
        self._hass = hass
        self._host = host
        self._port = port
        self._lock = threading.Lock()
        self._client = ModbusTcpClient(host, port, timeout=_MODBUS_TIMEOUT)
        self._validate_connection()

    def _validate_connection(self) -> None:
        """Validate that the connection is working and Modbus is enabled."""
        if not self._client.connect():
            raise ConnectionError(f"Could not connect to {self._host}:{self._port}")

        try:
            result = self._client.read_input_registers(
                _VALIDATION_REGISTER_ADDRESS, 1
            )
            if result.isError():
                raise ModbusNotEnabledError(
                    f"Modbus TCP is not enabled on {self._host}:{self._port}"
                )
        except ModbusException as e:
            raise ModbusNotEnabledError(
                f"Modbus TCP is not enabled on {self._host}:{self._port}: {e}"
            )

    def read_registers(self, address: int, count: int):
        """Read registers from the device."""
        with self._lock:
            result = self._client.read_discrete_inputs(address, count)
            if result.isError():
                raise ModbusException(f"Error reading registers at {address}")
            return result.registers

    def close(self):
        """Close the connection to the device."""
        with self._lock:
            self._client.close()