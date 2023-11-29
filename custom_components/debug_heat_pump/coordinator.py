"""DataUpdateCoordinator for debug_heat_pump."""
from __future__ import annotations

from datetime import timedelta

from homeassistant.config_entries import ConfigEntry
from homeassistant.core import HomeAssistant
from homeassistant.helpers.update_coordinator import DataUpdateCoordinator

from .api import DebugHeatPumpApi
from .const import DOMAIN, LOGGER


# https://developers.home-assistant.io/docs/integration_fetching_data#coordinated-single-api-poll-for-data-for-all-entities
class DebugHeatPumpCoordinator(DataUpdateCoordinator):
    """Class to manage fetching data from the API."""

    config_entry: ConfigEntry

    def __init__(
        self,
        hass: HomeAssistant,
        client: DebugHeatPumpApi,
    ) -> None:
        """Initialize."""
        self.client = client
        super().__init__(
            hass=hass,
            logger=LOGGER,
            name=DOMAIN,
            update_interval=timedelta(seconds=60),
        )

    async def _async_update_data(self):
        """Update data via library."""
        self._available = True
        #try:
        #    return await self.client.async_get_data()
        #except DebugHeatPumpApiAuthenticationError as exception:
        #    raise ConfigEntryAuthFailed(exception) from exception
        #except DebugHeatPumpApiError as exception:
        #    raise UpdateFailed(exception) from exception

    @property
    def available(self) -> bool:
        """Return True if entity is available."""
        return self._available
