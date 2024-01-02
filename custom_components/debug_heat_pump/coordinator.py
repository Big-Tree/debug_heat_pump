"""DataUpdateCoordinator for debug_heat_pump."""
from __future__ import annotations

from datetime import datetime, timedelta
import pandas as pd
import os

from homeassistant.core import HomeAssistant
from homeassistant.helpers.update_coordinator import DataUpdateCoordinator

from .api import DebugHeatPumpApi
from .const import DOMAIN, LOGGER
from . import const


class DebugHeatPumpCoordinator(DataUpdateCoordinator):
    """Class to manage fetching data from the API."""

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

        csv_file_path = self.hass.config.path()
        csv_file_path = os.path.join(
            csv_file_path,
            'custom_components/debug_heat_pump/data/Property_ID=EOH3204_cropped.csv')

        # If we are developing the integration the file path will be different.
        developing_integration = True
        if developing_integration:
            csv_file_path = self.hass.config.path().split('/')[:-1]
            csv_file_path.extend(['custom_components', 'debug_heat_pump', 'data', 'Property_ID=EOH3204_cropped.csv'])
            csv_file_path = '/'.join(csv_file_path)
        #csv_file_path.extend(['custom_components', 'debug_heat_pump', 'data', 'Property_ID=EOH3204_cropped.csv'])
        #csv_file_path = '/'.join(csv_file_path)
        df = pd.read_csv(csv_file_path)
        df = df[15249:-22630]  # 2022/01/01 00:00:00 - 2022/08/24 23:58:00
        self._external_air_temperature = df['External_Air_Temperature'].to_numpy()
        self._internal_air_temperature = df['Internal_Air_Temperature'].to_numpy()
        self._power = df['Power/kW'].to_numpy()

    async def _async_update_data(self):
        """Update data via library."""
        self._available = True

    def index(self):
        """Each index represents a two minute period."""
        now = datetime.now()
        begining_of_year = now.replace(month=1, day=1, minute=0, second=0, microsecond=0)
        seconds_since = now.timestamp() - begining_of_year.timestamp()
        index = int(seconds_since/2)
        return index

    def celcius_conversion(self, x):
        """Ensure celcius readings are converted to the correct unit.

        Data is stored in °C, so readings need to be converted to °F if set in the config_flow.
        """
        unit = self.config_entry.data[const.TEMP_UNIT]
        if unit == const.TEMP_CELSIUS:
            return x
        elif unit == const.TEMP_FAHRENHEIT:
            # Convert our Celcius readings to Farenheit
            return x*9/5 + 32

    def power_conversion(self, x):
        """Ensure power readings are converted to the correct unit.

        Data is stored in kW, so readings need to be converted to W if set in the config_flow.
        """
        unit = self.config_entry.data[const.POWER_UNIT]
        if unit == const.POWER_KW:
            return x
        elif unit == const.POWER_W:
            return x * 1000
        elif unit == 'w':
            return x * 1000


    @property
    def available(self) -> bool:
        """Return True if entity is available."""
        return self._available

    @property
    def external_air_temperature(self):
        """Current external air temperature."""
        celcius_reading = self._external_air_temperature.take(self.index(), mode='wrap')
        return self.celcius_conversion(celcius_reading)

    @property
    def internal_air_temperature(self):
        """Current internal air temperature."""
        celcius_reading = self._internal_air_temperature.take(self.index(), mode='wrap')
        return self.celcius_conversion(celcius_reading)

    @property
    def power(self):
        """Current heat pump power usage."""
        kw_reading = self._power.take(self.index(), mode='wrap')
        return self.power_conversion(kw_reading)
