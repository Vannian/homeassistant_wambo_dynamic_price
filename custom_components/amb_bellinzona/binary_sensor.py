from __future__ import annotations

from homeassistant.components.binary_sensor import BinarySensorEntity, BinarySensorDeviceClass
from homeassistant.config_entries import ConfigEntry
from homeassistant.core import HomeAssistant
from homeassistant.helpers.entity_platform import AddEntitiesCallback
from homeassistant.helpers.update_coordinator import CoordinatorEntity

from .const import DOMAIN, ATTRIBUTION
from .coordinator import AmbCHPricesCoordinator


async def async_setup_entry(
    hass: HomeAssistant,
    entry: ConfigEntry,
    async_add_entities: AddEntitiesCallback,
) -> None:
    """Set up the binary sensors."""
    coordinator: AmbCHPricesCoordinator = hass.data[DOMAIN][entry.entry_id]

    periods = coordinator.data.get("periods", [])

    entities = []

    for i, period in enumerate(periods):
        entities.append(
            AmbCHPricePeriodBinarySensor(
                coordinator,
                period,
                idx=i,
                count=len(periods)
            )
        )

    # Extra helpful sensors
    entities.append(CurrentPriceBinarySensor(coordinator))
    entities.append(NextChangeBinarySensor(coordinator))

    async_add_entities(entities, True)


class AmbCHPricePeriodBinarySensor(CoordinatorEntity, BinarySensorEntity):
    """Binary sensor for one green/red period."""

    _attr_has_entity_name = True
    _attr_attribution = ATTRIBUTION
    _attr_device_class = BinarySensorDeviceClass.RUNNING  # or None

    def __init__(
        self,
        coordinator: AmbCHPricesCoordinator,
        period: dict,
        idx: int,
        count: int,
    ) -> None:
        super().__init__(coordinator)
        self._period = period
        self._idx = idx
        self._attr_unique_id = f"{DOMAIN}_period_{idx}"
        self._attr_name = f"Price Period {idx+1}/{count}"

    @property
    def is_on(self) -> bool | None:
        """True = low price (green)."""
        return self._period.get("is_low")

    @property
    def icon(self) -> str | None:
        return "mdi:leaf" if self.is_on else "mdi:alert"

    @property
    def extra_state_attributes(self) -> dict:
        p = self._period
        return {
            "start": p["start"].isoformat(),
            "end": p["end"].isoformat(),
            "color_hex": p["color"],
            "duration_min": round(p["duration_minutes"]),
            "fetch_date": self.coordinator.today_str,
        }


class CurrentPriceBinarySensor(CoordinatorEntity, BinarySensorEntity):
    """Shows if current period is low price."""

    _attr_has_entity_name = True
    _attr_name = "Current Price Low"
    _attr_unique_id = f"{DOMAIN}_current_low"
    _attr_device_class = BinarySensorDeviceClass.RUNNING
    _attr_attribution = ATTRIBUTION

    def __init__(self, coordinator: AmbCHPricesCoordinator) -> None:
        super().__init__(coordinator)

    @property
    def is_on(self) -> bool | None:
        color = self.coordinator.data.get("current_color")
        return color == "#05DA3A" if color else None

    @property
    def icon(self) -> str | None:
        return "mdi:currency-usd-off" if self.is_on else "mdi:currency-usd"

    @property
    def extra_state_attributes(self) -> dict:
        now = datetime.now().astimezone()
        return {
            "current_color": self.coordinator.data.get("current_color"),
            "as_of": now.isoformat(),
        }


class NextChangeBinarySensor(CoordinatorEntity, BinarySensorEntity):
    """Next time the price color changes."""

    _attr_has_entity_name = True
    _attr_name = "Next Price Change"
    _attr_unique_id = f"{DOMAIN}_next_change"
    _attr_device_class = None
    _attr_attribution = ATTRIBUTION

    def __init__(self, coordinator: AmbCHPricesCoordinator) -> None:
        super().__init__(coordinator)

    @property
    def is_on(self) -> bool:
        return False  # informational only

    @property
    def icon(self) -> str:
        return "mdi:clock-fast"

    @property
    def extra_state_attributes(self) -> dict:
        periods = self.coordinator.data.get("periods", [])
        now = datetime.now().astimezone()

        next_change = None
        next_is_low = None

        for p in periods:
            if p["start"] <= now < p["end"]:
                next_change = p["end"]
                next_is_low = not p["is_low"]  # opposite of current
                break
            if p["start"] > now:
                next_change = p["start"]
                next_is_low = p["is_low"]
                break

        attr = {
            "next_change_time": next_change.isoformat() if next_change else None,
            "next_is_low_price": next_is_low,
        }
        return attr