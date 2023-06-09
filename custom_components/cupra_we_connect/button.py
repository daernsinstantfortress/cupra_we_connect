"""Button integration."""
from weconnect_cupra import weconnect_cupra

from homeassistant.components.button import ButtonEntity

from . import get_object_value, set_ac_charging_speed, set_climatisation, start_stop_charging
from .const import DOMAIN


async def async_setup_entry(hass, config_entry, async_add_entities):
    """Add buttons for passed config_entry in HA."""
    we_connect: weconnect_cupra.WeConnect = hass.data[DOMAIN][config_entry.entry_id]
    vehicles = hass.data[DOMAIN][config_entry.entry_id + "_vehicles"]

    entities = []
    for vehicle in vehicles:  # weConnect.vehicles.items():
        entities.append(VolkswagenIDStartClimateButton(vehicle, we_connect))
        entities.append(VolkswagenIDStopClimateButton(vehicle, we_connect))
        entities.append(VolkswagenIDStartChargingButton(vehicle, we_connect))
        entities.append(VolkswagenIDStopChargingButton(vehicle, we_connect))
        entities.append(VolkswagenIDToggleACChargeSpeed(vehicle, we_connect))

    async_add_entities(entities)

    return True


class VolkswagenIDStartClimateButton(ButtonEntity):
    """Button for starting climate."""

    def __init__(self, vehicle, we_connect) -> None:
        """Initialize VolkswagenID vehicle sensor."""
        self._attr_name = f"{vehicle.nickname} Start Climate"
        self._attr_unique_id = f"{vehicle.vin}-start_climate"
        self._we_connect = we_connect
        self._vehicle = vehicle

    def press(self) -> None:
        """Handle the button press."""
        set_climatisation(self._vehicle.vin.value, self._we_connect, "start", 0)


class VolkswagenIDStopClimateButton(ButtonEntity):
    """Button for starting climate."""

    def __init__(self, vehicle, we_connect) -> None:
        """Initialize VolkswagenID vehicle sensor."""
        self._attr_name = f"{vehicle.nickname} Stop Climate"
        self._attr_unique_id = f"{vehicle.vin}-stop_climate"
        self._we_connect = we_connect
        self._vehicle = vehicle

    def press(self) -> None:
        """Handle the button press."""
        set_climatisation(self._vehicle.vin.value, self._we_connect, "stop", 0)


class VolkswagenIDStartChargingButton(ButtonEntity):
    """Button for starting charging."""

    def __init__(self, vehicle, we_connect) -> None:
        """Initialize VolkswagenID vehicle sensor."""
        self._attr_name = f"{vehicle.nickname} Start Charging"
        self._attr_unique_id = f"{vehicle.vin}-start_charging"
        self._we_connect = we_connect
        self._vehicle = vehicle

    def press(self) -> None:
        """Handle the button press."""
        start_stop_charging(self._vehicle.vin.value, self._we_connect, "start")


class VolkswagenIDStopChargingButton(ButtonEntity):
    """Button for starting climate."""

    def __init__(self, vehicle, we_connect) -> None:
        """Initialize VolkswagenID vehicle sensor."""
        self._attr_name = f"{vehicle.nickname} Stop Charging"
        self._attr_unique_id = f"{vehicle.vin}-stop_charging"
        self._we_connect = we_connect
        self._vehicle = vehicle

    def press(self) -> None:
        """Handle the button press."""
        start_stop_charging(self._vehicle.vin.value, self._we_connect, "stop")


class VolkswagenIDToggleACChargeSpeed(ButtonEntity):
    """Button for toggling the charge speed."""

    def __init__(self, vehicle, we_connect: weconnect_cupra.WeConnect) -> None:
        """Initialize VolkswagenID vehicle sensor."""
        self._attr_name = f"{vehicle.nickname} Toggle AC Charge Speed"
        self._attr_unique_id = f"{vehicle.vin}-toggle_ac_charge_speed"
        self._we_connect = we_connect
        self._vehicle = vehicle

    def press(self) -> None:
        """Handle the button press."""

        current_state = get_object_value(
            self._vehicle.domains["charging"]["chargingSettings"].maxChargeCurrentAC
        )

        if current_state == "maximum":
            set_ac_charging_speed(
                self._vehicle.vin.value,
                self._we_connect,
                "reduced",
            )
        else:
            set_ac_charging_speed(
                self._vehicle.vin.value,
                self._we_connect,
                "maximum",
            )
