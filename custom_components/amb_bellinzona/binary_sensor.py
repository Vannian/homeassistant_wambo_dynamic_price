from homeassistant.components.binary_sensor import BinarySensorEntity, BinarySensorDeviceClass
from datetime import datetime
from .const import COLOR_ALTA

async def async_setup_platform(hass, config, async_add_entities, discovery_info=None):
    
    async_add_entities([AMBAltaTariffaSensor()], True)

class AMBAltaTariffaSensor(BinarySensorEntity):    

    @property
    def name(self):
        return "AMB Alta Tariffa"

    @property
    def unique_id(self):
        return "amb_alta_tariffa_binary"

    @property
    def device_class(self):
        return BinarySensorDeviceClass.POWER

    @property
    def is_on(self):
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
        