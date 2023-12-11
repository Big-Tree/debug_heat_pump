"""Sensor platform for debug heat pump."""
from __future__ import annotations

from homeassistant.components.sensor import SensorEntity, SensorEntityDescription, SensorStateClass
from homeassistant.components.sensor.const import SensorDeviceClass

from . import const
from .coordinator import DebugHeatPumpCoordinator
from .entity import DebugHeatPumpEntity


async def async_setup_entry(hass, entry, async_add_devices):
    """Set up the sensor platform."""
    coordinator = hass.data[const.DOMAIN][entry.entry_id]
    async_add_devices([
        OptisparkSensor(
            coordinator=coordinator,
            entity_description=SensorEntityDescription(
                key="external_temperature",
                name="External Temperature",
                icon="mdi:thermometer"),
            native_value=10,
            native_unit_of_measurement='°C',
            device_class=SensorDeviceClass.TEMPERATURE,
            suggested_display_precision=1,
        ),
        OptisparkSensor(
            coordinator=coordinator,
            entity_description=SensorEntityDescription(
                key="power_usage",
                name="Power Usage",
                icon="mdi:lightning-bolt"),
            native_value=800,
            native_unit_of_measurement='W',
            device_class=SensorDeviceClass.POWER,
            suggested_display_precision=1,
        ),]
    )


class OptisparkSensor(DebugHeatPumpEntity, SensorEntity):
    """optispark Sensor class."""

    def __init__(
        self,
        coordinator: DebugHeatPumpCoordinator,
        entity_description: SensorEntityDescription,
        native_value: float,
        device_class: str = None,
        native_unit_of_measurement: str = None,
        suggested_display_precision: int = None,
        state_class: SensorStateClass = SensorStateClass.MEASUREMENT,
    ) -> None:
        """Initialize the sensor class."""
        super().__init__(coordinator)
        self.entity_description = entity_description
        self._native_value = native_value
        self._device_class = device_class
        self._native_unit_of_measurement = native_unit_of_measurement
        self._suggested_display_precision = suggested_display_precision
        self._state_class = state_class

    @property
    def suggested_display_precision(self):
        """The number of decimals which should be used in the sensor's state when it's displayed."""
        return self._suggested_display_precision

    @property
    def device_class(self):
        """Type of sensor."""
        return self._device_class

    @property
    def native_unit_of_measurement(self):
        """The unit of measurement that the sensor's value is expressed in.

        If the native_unit_of_measurement is °C or °F, and its device_class is temperature, the
        sensor's unit_of_measurement will be the preferred temperature unit configured by the user
        and the sensor's state will be the native_value after an optional unit conversion.
        """
        return self._native_unit_of_measurement

    @property
    def native_value(self) -> float:
        """The value of the sensor in the sensor's native_unit_of_measurement.

        Using a device_class may restrict the types that can be returned by this property.
        """
        return self._native_value

    @property
    def state_class(self):
        """Type of state.

        If not None, the sensor is assumed to be numerical and will be displayed as a line-chart in
        the frontend instead of as discrete values.
        """
        return self._state_class
