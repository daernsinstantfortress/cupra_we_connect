"""Config flow for Cupra We Connect integration."""
from __future__ import annotations

import logging
from typing import Any

import voluptuous as vol

from weconnect_cupra import weconnect_cupra
from weconnect_cupra.service import Service

from homeassistant import config_entries
from homeassistant.core import HomeAssistant
from homeassistant.data_entry_flow import FlowResult
from homeassistant.exceptions import HomeAssistantError
from homeassistant.helpers.selector import selector

from .const import DOMAIN

_LOGGER = logging.getLogger(__name__)

STEP_USER_DATA_SCHEMA = vol.Schema(
    {
        vol.Required("username"): str,
        vol.Required("password"): str,
        vol.Required("service", default='MyCupra'): selector({
            "select": {
                "options": ["MyCupra"]
            }
        }),
    }
)


async def validate_input(hass: HomeAssistant, data: dict[str, Any]) -> dict[str, Any]:
    """Validate the user input allows us to connect."""

    _LOGGER.debug(f'validate_input with username={data["username"]}, service={Service(data["service"])}')

    we_connect = weconnect_cupra.WeConnect(
        username=data["username"],
        password=data["password"],
        service=Service(data["service"]),
        updateAfterLogin=False,
        loginOnInit=False
    )

    # TODO: ADD Validation on credentials

    await hass.async_add_executor_job(we_connect.login)
    await hass.async_add_executor_job(we_connect.update)

    # vin = next(iter(we_connect.vehicles.items()))[0]

    return {"title": "Cupra We Connect"}


class ConfigFlow(config_entries.ConfigFlow, domain=DOMAIN):
    """Handle a config flow for Cupra We Connect."""

    VERSION = 1

    async def async_step_user(
        self, user_input: dict[str, Any] | None = None
    ) -> FlowResult:
        """Handle the initial step."""
        if user_input is None:
            return self.async_show_form(
                step_id="user", data_schema=STEP_USER_DATA_SCHEMA
            )

        errors = {}

        try:
            info = await validate_input(self.hass, user_input)
        except CannotConnect:
            _LOGGER.exception("CannotConnect exception during setup", exc_info=1)
            errors["base"] = "cannot_connect"
        except InvalidAuth:
            _LOGGER.exception("InvalidAuth exception during setup", exc_info=1)
            errors["base"] = "invalid_auth"
        except Exception:  # pylint: disable=broad-except
            _LOGGER.exception("Unexpected exception during setup", exc_info=1)
            errors["base"] = "unknown"
        else:
            return self.async_create_entry(title=info["title"], data=user_input)

        return self.async_show_form(
            step_id="user", data_schema=STEP_USER_DATA_SCHEMA, errors=errors
        )


class CannotConnect(HomeAssistantError):
    """Error to indicate we cannot connect."""


class InvalidAuth(HomeAssistantError):
    """Error to indicate there is invalid auth."""
