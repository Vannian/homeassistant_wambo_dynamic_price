
import logging
import requests
from datetime import datetime, timedelta
from homeassistant.helpers.entity import Entity
from .const import DOMAIN, API_URL

_LOGGER = logging.getLogger(__name__)

async def async_setup_platform(hass, config, async_add_entities, discovery_info=None):
    async_add_entities([AMBDynamicSensor()], True)

class AMBDynamicSensor(Entity):

    def __init__(self):
        self._state = None
        self._attributes = {}

    @property
    def name(self):
        return "AMB Dynamic Data"

    @property
    def unique_id(self):
        return "amb_bellinzona_dynamic_data"

    @property
    def state(self):
        return self._state

    @property
    def extra_state_attributes(self):
        return self._attributes

    def update(self):
        try:
            # Prepare the current date for the POST payload
            date_str = datetime.now().strftime("%Y-%m-%dT00:00:00.000Z")
            payload = {"date": date_str}
            
            response = requests.post(API_URL, json=payload, timeout=10)
            response.raise_for_status()
            data = response.json()

            self._attributes = {
                "bgColors": data.get("bgColors", []),
                "labels": data.get("labels", []),
                "last_update": datetime.now().isoformat()
            }
            self._state = "Online"
        except Exception as e:
            _LOGGER.error("Error fetching AMB data: %s", e)
            self._state = "Error"