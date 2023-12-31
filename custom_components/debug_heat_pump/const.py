"""Constants for debug_heat_pump."""
from logging import Logger, getLogger

LOGGER: Logger = getLogger(__package__)

NAME = "Debug Heat Pump"
DOMAIN = "debug_heat_pump"
VERSION = "0.0.4"
ATTRIBUTION = "Attribution"

MODE = "debug_heat_pump_mode"
MODE_HEAT = "Heat"
MODE_HEAT_COOL = "Heat & Cool"
MODE_COOL = "Cool"

TEMP_UNIT = "Temperature Unit"
TEMP_CELSIUS = "°C"
TEMP_FAHRENHEIT = "°F"
