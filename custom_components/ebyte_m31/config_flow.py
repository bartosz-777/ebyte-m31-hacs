"""Config flow for the Ebyte M31 integration."""
from __future__ import annotations

import logging
from typing import Any

import voluptuous as vol

from homeassistant import config_entries
from homeassistant.const import CONF_HOST, CONF_PORT
from homeassistant.core import callback
from homeassistant.data_entry_flow import FlowResult

from .const import DEFAULT_HOST, DEFAULT_PORT, DOMAIN, bridgeModels
from .hub import EbyteM31Hub, ModbusNotEnabledError

_LOGGER = logging.getLogger(__name__)

STEP_USER_DATA_SCHEMA = vol.Schema(
    {
        vol.Required(CONF_HOST, default=DEFAULT_HOST): vol.All(str, vol.Length(min=1)),
        vol.Required(CONF_PORT, default=DEFAULT_PORT): vol.Coerce(int),
        vol.Required("model", default="AAAX4440G"): vol.In([model["name"] for model in bridgeModels]),
    }
)


class EbyteM31ConfigFlow(config_entries.ConfigFlow, domain=DOMAIN):
    """Handle a config flow for the Ebyte M31 integration."""

    VERSION = 1

    async def async_step_user(self, user_input: dict[str, Any] | None = None) -> FlowResult:
        errors: dict[str, str] = {}

        if user_input is not None:
            hub = EbyteM31Hub(user_input[CONF_HOST], user_input[CONF_PORT])
            try:
                await hub.async_validate_modbus_protocol()
                await self.async_set_unique_id(
                    f"{user_input[CONF_HOST]}:{user_input[CONF_PORT]}"
                )
                self._abort_if_unique_id_configured()
                return self.async_create_entry(title="Ebyte M31", data=user_input)
            except (ConnectionError, ModbusNotEnabledError):
                errors["base"] = "cannot_connect"
            except Exception:  # noqa: BLE001
                _LOGGER.exception("Unexpected error during config flow")
                errors["base"] = "unknown"
            finally:
                await hub.async_close()

        return self.async_show_form(
            step_id="user",
            data_schema=STEP_USER_DATA_SCHEMA,
            errors=errors,
        )
    @staticmethod
    @callback
    def async_get_options_flow(config_entry) -> EbyteM31OptionsFlowHandler:
        """Get the options flow for this handler."""
        return EbyteM31OptionsFlowHandler(config_entry)


class EbyteM31OptionsFlowHandler(config_entries.OptionsFlow):
    """Handle Ebyte M31 options."""

    def __init__(self, config_entry: config_entries.ConfigEntry) -> None:
        """Initialize Ebyte M31 options flow."""
        self.config_entry = config_entry

    async def async_step_init(self, user_input: dict[str, Any] | None = None) -> FlowResult:
        """Manage the options."""
        if user_input is not None:
            return self.async_create_entry(title="", data=user_input)

        return self.async_show_form(
            step_id="init",
            data_schema=STEP_USER_DATA_SCHEMA,
        )