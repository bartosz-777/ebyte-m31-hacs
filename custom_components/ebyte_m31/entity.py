"""Base entity for the Ebyte M31 integration."""
from __future__ import annotations

from homeassistant.helpers.update_coordinator import CoordinatorEntity

from .coordinator import EbyteM31Coordinator


class EbyteM31Entity(CoordinatorEntity[EbyteM31Coordinator]):
    """Common entity behavior for the integration."""

    def __init__(self, coordinator: EbyteM31Coordinator, entry_id: str, key: str, name: str) -> None:
        super().__init__(coordinator)
        self._attr_has_entity_name = True
        self._attr_name = name
        self._attr_unique_id = f"{entry_id}_{key}"
        self._key = key

    @property
    def available(self) -> bool:
        return self.coordinator.last_update_success

    async def async_update(self) -> None:
        await self.coordinator.async_request_refresh()
