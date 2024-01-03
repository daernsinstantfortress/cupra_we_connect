"""Sensor integration."""
from __future__ import annotations

from collections.abc import Callable
from dataclasses import dataclass
from typing import cast

from weconnect_cupra import weconnect_cupra

from homeassistant.components.sensor import (
    SensorEntity,
    SensorEntityDescription,
    SensorStateClass,
    SensorDeviceClass,
)
from homeassistant.const import (
#     DEVICE_CLASS_BATTERY,
#     DEVICE_CLASS_POWER,
#     DEVICE_CLASS_TEMPERATURE,
#     LENGTH_KILOMETERS,
#     LENGTH_MILES,
    PERCENTAGE,
#     POWER_KILO_WATT,
#     SPEED_KILOMETERS_PER_HOUR,
#     TEMP_CELSIUS,
#     TEMP_FAHRENHEIT,
#     TIME_DAYS,
#     TIME_MINUTES,
    UnitOfLength,
    UnitOfPower,
    UnitOfTime,
    UnitOfTemperature,
    UnitOfSpeed,
)
from homeassistant.helpers.typing import StateType
from homeassistant.helpers.update_coordinator import DataUpdateCoordinator

from . import VolkswagenIDBaseEntity, get_object_value
from .const import DOMAIN


@dataclass
class VolkswagenIdEntityDescription(SensorEntityDescription):
    """Describes Volkswagen ID sensor entity."""

    value: Callable = lambda x, y: x


SENSORS: tuple[VolkswagenIdEntityDescription, ...] = (
    # This is a string, not an number
    VolkswagenIdEntityDescription(
        key="climatisationState",
        name="Climatisation State",
        state_class=None,
        value=lambda data: data["climatisation"][
            "climatisationStatus"
        ].climatisationState.value,
    ),
    VolkswagenIdEntityDescription(
        key="remainingClimatisationTime_min",
        name="Remaining Climatisation Time",
        native_unit_of_measurement=UnitOfTime.MINUTES,
        state_class=SensorStateClass.MEASUREMENT,
        value=lambda data: data["climatisation"][
            "climatisationStatus"
        ].remainingClimatisationTime_min.value,
    ),
    VolkswagenIdEntityDescription(
        key="targetTemperature_C",
        name="Target Temperature C",
        device_class=SensorDeviceClass.TEMPERATURE,
        native_unit_of_measurement=UnitOfTemperature.CELSIUS,
        state_class=SensorStateClass.MEASUREMENT,
        value=lambda data: data["climatisation"][
            "climatisationSettings"
        ].targetTemperature_C.value,
    ),
    VolkswagenIdEntityDescription(
        key="targetTemperature_F",
        name="Target Temperature F",
        device_class=SensorDeviceClass.TEMPERATURE,
        native_unit_of_measurement=UnitOfTemperature.FAHRENHEIT,
        state_class=SensorStateClass.MEASUREMENT,
        value=lambda data: data["climatisation"][
            "climatisationSettings"
        ].targetTemperature_F.value,
    ),
    # Not available from Cupra
    # VolkswagenIdEntityDescription(
    #     key="unitInCar",
    #     name="Unit In car",
    #     state_class=None,
    #     value=lambda data: data["climatisation"][
    #         "climatisationSettings"
    #     ].unitInCar.value,
    # ),
    # This is a string, not an number
    VolkswagenIdEntityDescription(
        key="chargingState",
        name="Charging State",
        icon="mdi:ev-station",
        state_class=None,
        value=lambda data: data["charging"]["chargingStatus"].chargingState.value,
    ),
    VolkswagenIdEntityDescription(
        key="remainingChargingTimeToComplete_min",
        name="Remaining Charging Time",
        native_unit_of_measurement=UnitOfTime.MINUTES,
        state_class=SensorStateClass.MEASUREMENT,
        value=lambda data: data["charging"][
            "chargingStatus"
        ].remainingChargingTimeToComplete_min.value,
    ),
    # This is a string, not an number
    VolkswagenIdEntityDescription(
        key="chargeMode",
        name="Charging Mode",
        state_class=None,
        icon="mdi:ev-station",
        value=lambda data: data["charging"]["chargingStatus"].chargeMode.value,
    ),
    VolkswagenIdEntityDescription(
        key="chargePower_kW",
        name="Charge Power",
        native_unit_of_measurement=UnitOfPower.KILO_WATT,
        device_class=SensorDeviceClass.POWER,
        state_class=SensorStateClass.MEASUREMENT,
        value=lambda data: data["charging"]["chargingStatus"].chargePower_kW.value,
    ),
    VolkswagenIdEntityDescription(
        key="chargeRate_kmph",
        name="Charge Rate",
        native_unit_of_measurement=UnitOfSpeed.KILOMETERS_PER_HOUR,
        state_class=SensorStateClass.MEASUREMENT,
        value=lambda data: data["charging"]["chargingStatus"].chargeRate_kmph.value,
    ),
    # Not available for Cupra ?
    VolkswagenIdEntityDescription(
        key="chargingSettings",
        name="Charging Settings",
        state_class=None,
        value=lambda data: data["charging"]["chargingStatus"].chargingSettings.value,
    ),
    # This is a string, not an number
    VolkswagenIdEntityDescription(
        key="chargeType",
        name="Charge Type",
        state_class=None,
        value=lambda data: data["charging"]["chargingStatus"].chargeType.value,
    ),
    # This is a string, not an number
    VolkswagenIdEntityDescription(
        key="maxChargeCurrentAC",
        name="Max Charge Current AC",
        state_class=None,
        value=lambda data: data["charging"][
            "chargingSettings"
        ].maxChargeCurrentAC.value,
    ),
    VolkswagenIdEntityDescription(
        key="targetSOC_pct",
        name="Target State of Charge",
        device_class=SensorDeviceClass.BATTERY,
        native_unit_of_measurement=PERCENTAGE,
        state_class=SensorStateClass.MEASUREMENT,
        value=lambda data: data["charging"]["chargingSettings"].targetSOC_pct.value,
    ),
    VolkswagenIdEntityDescription(
        key="currentSOC_pct",
        name="State of Charge",
        device_class=SensorDeviceClass.BATTERY,
        native_unit_of_measurement=PERCENTAGE,
        state_class=SensorStateClass.MEASUREMENT,
        value=lambda data: data["charging"]["batteryStatus"].currentSOC_pct.value,
    ),
    VolkswagenIdEntityDescription(
        name="Range in Kilometers",
        key="cruisingRangeElectric_km",
        native_unit_of_measurement=UnitOfLength.KILOMETERS,
        state_class=SensorStateClass.MEASUREMENT,
        value=lambda data: data["charging"][
            "batteryStatus"
        ].cruisingRangeElectric_km.value,
    ),
    VolkswagenIdEntityDescription(
        name="Range in Miles",
        key="cruisingRangeElectric_mi",
        native_unit_of_measurement=UnitOfLength.MILES,
        state_class=SensorStateClass.MEASUREMENT,
        value=lambda data: data["charging"][
            "batteryStatus"
        ].cruisingRangeElectric_km.value,
    ),
    # Not supported by Cupra
    # VolkswagenIdEntityDescription(
    #     name="Health Inspection",
    #     key="inspectionDue",
    #     native_unit_of_measurement=TIME_DAYS,
    #     state_class=SensorStateClass.MEASUREMENT,
    #     value=lambda data: data["vehicleHealthInspection"][
    #         "maintenanceStatus"
    #     ].inspectionDue_days.value if "vehicleHealthInspection" in data else None,
    # ),
    VolkswagenIdEntityDescription(
        name="Odometer in Kilometers",
        key="odometer_km",
        native_unit_of_measurement=UnitOfLength.KILOMETERS,
        state_class=SensorStateClass.MEASUREMENT,
        value=lambda data: data["measurements"][
            "odometerStatus"
        ].odometer.value,
    ),
    VolkswagenIdEntityDescription(
        name="Odometer in Miles",
        key="odometer_mi",
        native_unit_of_measurement=UnitOfLength.MILES,
        state_class=SensorStateClass.MEASUREMENT,
        value=lambda data: data["measurements"][
            "odometerStatus"
        ].odometer.value,
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


class VolkswagenIDSensor(VolkswagenIDBaseEntity, SensorEntity):
    """Representation of a VolkswagenID vehicle sensor."""

    entity_description: VolkswagenIdEntityDescription

    def __init__(
        self,
        sensor: VolkswagenIdEntityDescription,
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
        self._attr_native_unit_of_measurement = sensor.native_unit_of_measurement
        self._attr_state_class = sensor.state_class

    @property
    def native_value(self) -> StateType:
        """Return the state."""

        state = get_object_value(self.entity_description.value(self.data.domains))

        if self.entity_description.key == "cruisingRangeElectric_mi":
            state = int(float(state) * 0.62137)

        if state and self.entity_description.key == "odometer_mi":
            state = int(float(state) * 0.62137)

        return cast(StateType, state)
