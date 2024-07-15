"""Binary_sensor integration."""
from __future__ import annotations

from collections.abc import Callable
from dataclasses import dataclass

from weconnect_cupra import weconnect_cupra
from weconnect_cupra.elements.plug_status import PlugStatus
from weconnect_cupra.elements.window_heating_status import WindowHeatingStatus
from weconnect_cupra.elements.access_control_state import AccessControlState
from weconnect_cupra.elements.connection_state import ConnectionState


from homeassistant.components.binary_sensor import (
    BinarySensorDeviceClass,
    BinarySensorEntity,
    BinarySensorEntityDescription,
)
from homeassistant.helpers.update_coordinator import DataUpdateCoordinator

from . import VolkswagenIDBaseEntity, get_object_value
from .const import DOMAIN


@dataclass
class VolkswagenIdBinaryEntityDescription(BinarySensorEntityDescription):
    """Describes Volkswagen ID binary sensor entity."""

    value: Callable = lambda x, y: x
    on_value: object | None = None


SENSORS: tuple[VolkswagenIdBinaryEntityDescription, ...] = (
    VolkswagenIdBinaryEntityDescription(
        key="climatisationWithoutExternalPower",
        name="Climatisation Without External Power",
        value=lambda data: data["climatisation"][
            "climatisationSettings"
        ].climatisationWithoutExternalPower.value,
    ),
    VolkswagenIdBinaryEntityDescription(
        key="climatisationAtUnlock",
        name="Climatisation At Unlock",
        value=lambda data: data["climatisation"][
            "climatisationSettings"
        ].climatisationAtUnlock.value,
    ),
    VolkswagenIdBinaryEntityDescription(
        key="zoneFrontLeftEnabled",
        name="Zone Front Left Enabled",
        value=lambda data: data["climatisation"][
            "climatisationSettings"
        ].zoneFrontLeftEnabled.value,
    ),
    VolkswagenIdBinaryEntityDescription(
        key="zoneFrontRightEnabled",
        name="Zone Front Right Enabled",
        value=lambda data: data["climatisation"][
            "climatisationSettings"
        ].zoneFrontRightEnabled.value,
    ),
    VolkswagenIdBinaryEntityDescription(
        key="windowHeatingEnabled",
        name="Window Heating Enabled",
        value=lambda data: data["climatisation"][
            "climatisationSettings"
        ].windowHeatingEnabled.value,
    ),
    VolkswagenIdBinaryEntityDescription(
        key="frontWindowHeatingState",
        name="Front Window Heating State",
        value=lambda data: data["climatisation"]["windowHeatingStatus"]
        .windows["front"]
        .windowHeatingState.value,
        on_value=WindowHeatingStatus.Window.WindowHeatingState.ON,
    ),
    VolkswagenIdBinaryEntityDescription(
        key="rearWindowHeatingState",
        name="Rear Window Heating State",
        value=lambda data: data["climatisation"]["windowHeatingStatus"]
        .windows["rear"]
        .windowHeatingState.value,
        on_value=WindowHeatingStatus.Window.WindowHeatingState.ON,
    ),
    VolkswagenIdBinaryEntityDescription(
        key="autoUnlockPlugWhenCharged",
        name="Auto Unlock Plug When Charged",
        value=lambda data: data["charging"][
            "chargingSettings"
        ].autoUnlockPlugWhenCharged.value,
        on_value="on",  # ChargingSettings.UnlockPlugState.ON,
    ),
    VolkswagenIdBinaryEntityDescription(
        key="plugConnectionState",
        name="Plug Connection State",
        value=lambda data: data["charging"]["plugStatus"].plugConnectionState.value,
        device_class=BinarySensorDeviceClass.PLUG,
        on_value=PlugStatus.PlugConnectionState.CONNECTED,
    ),
    VolkswagenIdBinaryEntityDescription(
        key="plugLockState",
        name="Plug Lock State",
        value=lambda data: data["charging"]["plugStatus"].plugLockState.value,
        device_class=BinarySensorDeviceClass.LOCK,
        on_value=PlugStatus.PlugLockState.UNLOCKED,
    ),
    # Not available from Cupra
    # VolkswagenIdBinaryEntityDescription(
    #     key="insufficientBatteryLevelWarning",
    #     name="Insufficient Battery Level Warning",
    #     value=lambda data: data["readiness"][
    #         "readinessStatus"
    #     ].connectionWarning.insufficientBatteryLevelWarning.value,
    # ),
    VolkswagenIdBinaryEntityDescription(
        name="Car Is Online",
        key="isOnline",
        value=lambda data: data["status"]["connectionStatus"].connectionState.value,
        device_class=BinarySensorDeviceClass.CONNECTIVITY,
        on_value=ConnectionState.ConnectionState.ONLINE
    ),
    # Not available from Cupra
    # VolkswagenIdBinaryEntityDescription(
    #     name="Car Is Active",
    #     key="isActive",
    #     value=lambda data: data["readiness"][
    #         "readinessStatus"
    #     ].connectionState.isActive.value,
    # ),
    VolkswagenIdBinaryEntityDescription(
        key="doorLockStatus",
        name="Door Lock Status",
        icon="mdi:car-door-lock",
        device_class=BinarySensorDeviceClass.LOCK,
        value=lambda data: data["access"]["accessStatus"].doorLockStatus.value,
        on_value=AccessControlState.LockState.UNLOCKED,
    ),
    VolkswagenIdBinaryEntityDescription(
        key="trunkLockStatus",
        name="Trunk Lock Status",
        icon="mdi:lock-outline",
        device_class=BinarySensorDeviceClass.LOCK,
        value=lambda data: data["access"]["accessStatus"]
        .doors["trunk"]
        .lockState.value,
        on_value=AccessControlState.LockState.UNLOCKED,
    ),
    VolkswagenIdBinaryEntityDescription(
        key="hoodLockStatus",
        name="Hood Lock Status",
        icon="mdi:lock-outline",
        device_class=BinarySensorDeviceClass.LOCK,
        value=lambda data: data["access"]["accessStatus"].doors["hood"].lockState.value,
        on_value=AccessControlState.LockState.UNLOCKED,
    ),
    VolkswagenIdBinaryEntityDescription(
        key="rearRightLockStatus",
        name="Door Rear Right Lock Status",
        icon="mdi:car-door-lock",
        device_class=BinarySensorDeviceClass.LOCK,
        value=lambda data: data["access"]["accessStatus"]
        .doors["rearRight"]
        .lockState.value,
        on_value=AccessControlState.LockState.UNLOCKED,
    ),
    VolkswagenIdBinaryEntityDescription(
        key="rearLeftLockStatus",
        name="Door Rear Left Lock Status",
        icon="mdi:car-door-lock",
        device_class=BinarySensorDeviceClass.LOCK,
        value=lambda data: data["access"]["accessStatus"]
        .doors["rearLeft"]
        .lockState.value,
        on_value=AccessControlState.LockState.UNLOCKED,
    ),
    VolkswagenIdBinaryEntityDescription(
        key="frontLeftLockStatus",
        name="Door Front Left Lock Status",
        icon="mdi:car-door-lock",
        device_class=BinarySensorDeviceClass.LOCK,
        value=lambda data: data["access"]["accessStatus"]
        .doors["frontLeft"]
        .lockState.value,
        on_value=AccessControlState.LockState.UNLOCKED,
    ),
    VolkswagenIdBinaryEntityDescription(
        key="frontRightLockStatus",
        name="Door Front Right Lock Status",
        icon="mdi:car-door-lock",
        device_class=BinarySensorDeviceClass.LOCK,
        value=lambda data: data["access"]["accessStatus"]
        .doors["frontRight"]
        .lockState.value,
        on_value=AccessControlState.LockState.UNLOCKED,
    ),
    VolkswagenIdBinaryEntityDescription(
        key="trunkOpenStatus",
        name="Trunk Open Status",
        device_class=BinarySensorDeviceClass.DOOR,
        value=lambda data: data["access"]["accessStatus"]
        .doors["trunk"]
        .openState.value,
        on_value=AccessControlState.OpenState.OPEN,
    ),
    VolkswagenIdBinaryEntityDescription(
        key="hoodOpenStatus",
        name="Hood Open Status",
        device_class=BinarySensorDeviceClass.DOOR,
        value=lambda data: data["access"]["accessStatus"].doors["hood"].openState.value,
        on_value=AccessControlState.OpenState.OPEN,
    ),
    VolkswagenIdBinaryEntityDescription(
        key="rearRightOpenStatus",
        name="Door Rear Right Open Status",
        icon="mdi:car-door",
        device_class=BinarySensorDeviceClass.DOOR,
        value=lambda data: data["access"]["accessStatus"]
        .doors["rearRight"]
        .openState.value,
        on_value=AccessControlState.OpenState.OPEN,
    ),
    VolkswagenIdBinaryEntityDescription(
        key="rearLeftOpenStatus",
        name="Door Rear Left Open Status",
        icon="mdi:car-door",
        device_class=BinarySensorDeviceClass.DOOR,
        value=lambda data: data["access"]["accessStatus"]
        .doors["rearLeft"]
        .openState.value,
        on_value=AccessControlState.OpenState.OPEN,
    ),
    VolkswagenIdBinaryEntityDescription(
        key="frontLeftOpenStatus",
        name="Door Front Left Open Status",
        icon="mdi:car-door",
        device_class=BinarySensorDeviceClass.DOOR,
        value=lambda data: data["access"]["accessStatus"]
        .doors["frontLeft"]
        .openState.value,
        on_value=AccessControlState.OpenState.OPEN,
    ),
    VolkswagenIdBinaryEntityDescription(
        key="frontRightOpenStatus",
        name="Door Front Right Open Status",
        icon="mdi:car-door",
        device_class=BinarySensorDeviceClass.DOOR,
        value=lambda data: data["access"]["accessStatus"]
        .doors["frontRight"]
        .openState.value,
        on_value=AccessControlState.OpenState.OPEN,
    ),
    VolkswagenIdBinaryEntityDescription(
        key="windowRearRightOpenStatus",
        name="Window Rear Right Open Status",
        icon="mdi:window-closed",
        device_class=BinarySensorDeviceClass.WINDOW,
        value=lambda data: data["access"]["accessStatus"]
        .windows["rearRight"]
        .openState.value,
        on_value=AccessControlState.OpenState.OPEN,
    ),
    VolkswagenIdBinaryEntityDescription(
        key="windowRearLeftOpenStatus",
        name="Window Rear Left Open Status",
        icon="mdi:window-closed",
        device_class=BinarySensorDeviceClass.WINDOW,
        value=lambda data: data["access"]["accessStatus"]
        .windows["rearLeft"]
        .openState.value,
        on_value=AccessControlState.OpenState.OPEN,
    ),
    VolkswagenIdBinaryEntityDescription(
        key="windowFrontLeftOpenStatus",
        name="Window Front Left Open Status",
        icon="mdi:window-closed",
        device_class=BinarySensorDeviceClass.WINDOW,
        value=lambda data: data["access"]["accessStatus"]
        .windows["frontLeft"]
        .openState.value,
        on_value=AccessControlState.OpenState.OPEN,
    ),
    VolkswagenIdBinaryEntityDescription(
        key="windowfrontRightOpenStatus",
        name="Window Front Right Open Status",
        icon="mdi:window-closed",
        device_class=BinarySensorDeviceClass.WINDOW,
        value=lambda data: data["access"]["accessStatus"]
        .windows["frontRight"]
        .openState.value,
        on_value=AccessControlState.OpenState.OPEN,
    ),
    VolkswagenIdBinaryEntityDescription(
        key="overallStatus",
        name="Overall Status",
        icon="mdi:car-info",
        device_class=BinarySensorDeviceClass.LOCK,
        value=lambda data: data["access"]["accessStatus"].overallStatus.value,
        on_value=AccessControlState.OverallState.UNSAFE,
    ),
    VolkswagenIdBinaryEntityDescription(
        key="engineStatus",
        name="Engine Status",
        icon="mdi:engine-outline",
        device_class=BinarySensorDeviceClass.POWER,
        value=lambda data: data["access"]["accessStatus"].engineStatus.value,
        on_value=AccessControlState.EngineState.ON,
    ),
    VolkswagenIdBinaryEntityDescription(
        key="lightsStatus",
        name="Lights Status",
        icon="mdi:car-light-dimmed",
        device_class=BinarySensorDeviceClass.LIGHT,
        value=lambda data: data["access"]["accessStatus"].lightsStatus.value,
        on_value=AccessControlState.LightsState.ON,
    ),
)


async def async_setup_entry(hass, config_entry, async_add_entities):
    """Add sensors for passed config_entry in HA."""
    we_connect: weconnect_cupra.WeConnect = hass.data[DOMAIN][config_entry.entry_id]
    coordinator = hass.data[DOMAIN][config_entry.entry_id + "_coordinator"]

    # Fetch initial data so we have data when entities subscribe
    await coordinator.async_config_entry_first_refresh()

    entities: list[VolkswagenIDSensor] = []

    for index, vehicle in enumerate(coordinator.data):
        for sensor in SENSORS:
            entities.append(VolkswagenIDSensor(sensor, we_connect, coordinator, index))
    if entities:
        async_add_entities(entities)


class VolkswagenIDSensor(VolkswagenIDBaseEntity, BinarySensorEntity):
    """Representation of a VolkswagenID vehicle sensor."""

    entity_description: VolkswagenIdBinaryEntityDescription

    def __init__(
        self,
        sensor: VolkswagenIdBinaryEntityDescription,
        we_connect: weconnect_cupra.WeConnect,
        coordinator: DataUpdateCoordinator,
        index: int,
    ) -> None:
        """Initialize VolkswagenID vehicle sensor."""
        super().__init__(we_connect, coordinator, index)

        self.entity_description = sensor
        self._coordinator = coordinator
        self._attr_name = f"{self.data.nickname} {sensor.name}"
        self._attr_unique_id = f"{self.data.vin}-{sensor.key}"

    @property
    def is_on(self) -> bool:
        """Return true if sensor is on."""
        try:
            state = self.entity_description.value(self.data.domains)
            if isinstance(state, bool):
                return state

            state = get_object_value(state)
            return state == get_object_value(self.entity_description.on_value)

        except KeyError:
            return None
