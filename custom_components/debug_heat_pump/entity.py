"""DebugHeatPumpEntity class."""
from __future__ import annotations

from homeassistant.helpers.entity import DeviceInfo
from homeassistant.helpers.update_coordinator import CoordinatorEntity

from .const import ATTRIBUTION, DOMAIN, NAME, VERSION
from .coordinator import DebugHeatPumpCoordinator


class DebugHeatPumpEntity(CoordinatorEntity):
    """DebugHeatPumpEntity class."""

    _attr_attribution = ATTRIBUTION

    def __init__(self, coordinator: DebugHeatPumpCoordinator) -> None:
        """Initialize."""
        super().__init__(coordinator)
        self._attr_device_info = DeviceInfo(
            identifiers={(DOMAIN, 'Debug_heat_pump_device')},
            name=NAME,
            model=VERSION,
            manufacturer=NAME,
        )

    @property
    def unique_id(self):
        """Return unique id for the Number."""
        return self.entity_description.key + '_id'
