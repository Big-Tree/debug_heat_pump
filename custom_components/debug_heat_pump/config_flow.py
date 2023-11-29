"""Adds config flow for debug_heat_pump."""
from __future__ import annotations

import voluptuous as vol
from homeassistant import config_entries
from homeassistant.helpers.selector import selector
from . import const

from .const import DOMAIN


class DebugHeatPumpFlowHandler(config_entries.ConfigFlow, domain=DOMAIN):
    """Config flow for debug_heat_pump."""

    VERSION = 1

    async def async_step_user(
        self,
        user_input: dict | None = None,
    ) -> config_entries.FlowResult:
        """Handle a flow initialized by the user."""
        _errors = {}
        if user_input is not None:
            return self.async_create_entry(
                title=f"Debug Heat Pump - {user_input[const.MODE]}",
                data=user_input)
        data_schema = {}
        #data_schema[const.MODES] = selector({
        data_schema[vol.Required(const.MODE, default=const.MODE_HEAT_COOL)] = selector({
            "select": {
                "options": [const.MODE_HEAT_COOL, const.MODE_HEAT, const.MODE_COOL]}
        })
        data_schema[vol.Required(const.TEMP_UNIT, default=const.TEMP_CELSIUS)] = selector({
            "select": {
                "options": [const.TEMP_CELSIUS, const.TEMP_FAHRENHEIT],
            },
        })

        return self.async_show_form(
            step_id="user",
            data_schema=vol.Schema(data_schema),
            #data_schema=vol.Schema({vol.Optional(const.MODE, default=const.MODE_COOL): bool}),
            #data_schema=vol.Schema({
            #    vol.Required(const.TEMP_UNIT): vol.In({
            #        "Continuous": "Continuous",
            #        "Intermittent": "Intermittent"
            #    })
            #}),
            errors=_errors,
        )
