"""
Support for Volkswagen WeConnect Platform
"""
import logging

from weconnect_cupra import weconnect_cupra

from homeassistant.components.device_tracker import SourceType
from homeassistant.components.device_tracker.config_entry import TrackerEntity
from homeassistant.helpers.update_coordinator import DataUpdateCoordinator

from . import VolkswagenIDBaseEntity, get_object_value
from .const import DOMAIN

_LOGGER = logging.getLogger(__name__)


async def async_setup_entry(hass, config_entry, async_add_entities):
    """Add device trackers for passed config_entry in HA."""
    we_connect: weconnect_cupra.WeConnect = hass.data[DOMAIN][config_entry.entry_id]
    coordinator = hass.data[DOMAIN][config_entry.entry_id + "_coordinator"]

    # Fetch initial data
    await coordinator.async_refresh()

    entities = []

    for index, vehicle in enumerate(coordinator.data):
        entities.append(VolkswagenIDSensor(we_connect, coordinator, index))

    if entities:
        async_add_entities(entities)


class VolkswagenIDSensor(VolkswagenIDBaseEntity, TrackerEntity):
    """Representation of a VolkswagenID vehicle tracker."""

    def __init__(self, we_connect: weconnect_cupra.WeConnect, coordinator: DataUpdateCoordinator, index: int) -> None:
        super().__init__(we_connect, coordinator, index)
        self._coordinator = coordinator
        self._attr_name = f"{self.data.nickname} tracker"
        self._attr_unique_id = f"{self.data.vin}-tracker"

    @property
    def latitude(self) -> float:
        try:
            return get_object_value(self.data.domains["parking"]["parkingPosition"].latitude.value)
        except KeyError:
            return None

    @property
    def longitude(self) -> float:
        try:
            return get_object_value(self.data.domains["parking"]["parkingPosition"].longitude.value)
        except KeyError:
            return None

    @property
    def source_type(self):
        return SourceType.GPS

    @property
    def icon(self):
        return "mdi:car"
