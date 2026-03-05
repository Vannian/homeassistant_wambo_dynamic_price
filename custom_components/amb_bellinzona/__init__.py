"""The AMB Bellinzona Dynamic Tariff integration."""
from __future__ import annotations

import logging
from homeassistant.core import HomeAssistant
from homeassistant.helpers.typing import ConfigType

from .const import DOMAIN, PLATFORMS

_LOGGER = logging.getLogger(__name__)

async def async_setup(hass: HomeAssistant, config: ConfigType) -> bool:
    """Set up the AMB Bellinzona component via YAML."""
    # This check ensures the domain exists in your configuration.yaml
    if DOMAIN not in config:
        return True

    # This tells Home Assistant to look for sensor.py and binary_sensor.py
    for platform in PLATFORMS:
        hass.async_create_task(
            hass.helpers.discovery.async_load_platform(platform, DOMAIN, {}, config)
        )

    return True