"""Data coordinator for the Ebyte M31 Modbus integration."""
from __future__ import annotations

import logging
from datetime import timedelta
from typing import TYPE_CHECKING

from homeassistant.helpers.update_coordinator import DataUpdateCoordinator

from .const import DOMAIN

if TYPE_CHECKING:
    from .hub import EbyteM31Hub

_LOGGER = logging.getLogger(__name__)


class EbyteM31Coordinator(DataUpdateCoordinator[dict[str, bool]]):
    """Coordinate polling of the discrete input register values."""

    def __init__(self, hass, hub: "EbyteM31Hub") -> None:
        super().__init__(
            hass,
            _LOGGER,
            name=DOMAIN,
            update_interval=timedelta(seconds=10),
        )
        self.hub = hub

    async def _async_update_data(self) -> dict[str, bool]:
        values = await self.hub.async_read_discrete_inputs(count=8)
        return {f"input_{index}": bool(value) for index, value in enumerate(values)}
