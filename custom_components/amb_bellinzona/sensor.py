import logging
from datetime import datetime
from homeassistant.components.sensor import SensorEntity
from homeassistant.config_entries import ConfigEntry
from homeassistant.core import HomeAssistant
from aiohttp import ClientSession, ClientTimeout
from .const import DOMAIN, API_URL

_LOGGER = logging.getLogger(__name__)


async def async_setup_entry(
    hass: HomeAssistant,
    entry: ConfigEntry,
    async_add_entities,
) -> None:
    """Set up the AMB Dynamic Sensor from a config entry."""
    session = ClientSession()
    async_add_entities([AMBDynamicSensor(session)], True)


class AMBDynamicSensor(SensorEntity):
    """Represents AMB Bellinzona dynamic tariff data."""

    def __init__(self, session: ClientSession):
        self._state = None
        self._attributes = {}
        self._session = session

    @property
    def name(self) -> str:
        return "AMB Dynamic Data"

    @property
    def unique_id(self) -> str:
        return "amb_bellinzona_dynamic_data"

    @property
    def state(self):
        return self._state

    @property
    def extra_state_attributes(self):
        return self._attributes

    async def async_update(self):
        """Fetch new data from AMB API asynchronously."""
        try:
            date_str = datetime.now().strftime("%Y-%m-%dT00:00:00.000Z")
            payload = {"date": date_str}

            timeout = ClientTimeout(total=10)
            async with self._session.post(API_URL, json=payload, timeout=timeout) as resp:
                resp.raise_for_status()
                data = await resp.json()

            self._attributes = {
                "bgColors": data.get("bgColors", []),
                "labels": data.get("labels", []),
                "last_update": datetime.now().isoformat(),
            }
            self._state = "Online"
        except Exception as e:
            _LOGGER.error("Error fetching AMB data: %s", e)
            self._state = "None"