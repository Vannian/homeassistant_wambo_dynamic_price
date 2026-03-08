from homeassistant.components.binary_sensor import BinarySensorEntity, BinarySensorDeviceClass
from homeassistant.config_entries import ConfigEntry
from homeassistant.core import HomeAssistant
from datetime import datetime
from .const import COLOR_ALTA, COLOR_BASSA, DOMAIN


async def async_setup_entry(
    hass: HomeAssistant,
    entry: ConfigEntry,
    async_add_entities,
) -> None:
    """Set up AMB Bellinzona binary sensor from a config entry."""
    async_add_entities([AMBAltaTariffaSensor(hass)], True)


class AMBAltaTariffaSensor(BinarySensorEntity):
    """Binary sensor that indicates high tariff (red) slots."""

    def __init__(self, hass: HomeAssistant) -> None:
        """Initialize the sensor."""
        self.hass = hass

    @property
    def name(self) -> str:
        return "AMB Alta Tariffa"

    @property
    def unique_id(self) -> str:
        return "amb_alta_tariffa_binary"

    @property
    def device_class(self) -> BinarySensorDeviceClass:
        return BinarySensorDeviceClass.POWER

    @property
    def is_on(self) -> bool:
        """Calculate if we are currently in a Red (High) slot."""
        # Get data from the main data sensor
        state = self.hass.states.get("sensor.amb_dynamic_data")
        if not state or "bgColors" not in state.attributes:
            return False

        colors = state.attributes["bgColors"]
        if not colors:
            return False

        # Calculate index (0-95) for the current 15-minute slot
        now = datetime.now()
        index = (now.hour * 4) + (now.minute // 15)

        if index < len(colors):
            return colors[index] == COLOR_ALTA
        return False