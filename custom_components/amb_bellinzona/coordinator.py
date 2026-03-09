from __future__ import annotations

from datetime import date, datetime, timedelta
import logging

from homeassistant.core import HomeAssistant
from homeassistant.helpers.update_coordinator import DataUpdateCoordinator, UpdateFailed

import aiohttp

from .const import DOMAIN, API_URL

_LOGGER = logging.getLogger(__name__)

class AmbCHPricesCoordinator(DataUpdateCoordinator[dict]):
    """Data coordinator for amb.ch prices."""

    def __init__(self, hass: HomeAssistant) -> None:
        """Initialize coordinator."""
        super().__init__(
            hass,
            _LOGGER,
            name=DOMAIN,
            update_interval=timedelta(seconds=UPDATE_INTERVAL),
        )
        self._session = aiohttp.ClientSession()
        self.today_str = None
        self._last_fetch_date = None

    async def _async_update_data(self) -> dict:
        """Fetch data from API."""
        today = date.today().isoformat()
        
        # Only re-fetch if date changed or first time (to reduce calls)
        if self._last_fetch_date == today and self.data is not None:
            return self.data

        try:
            payload = {"date": today}
            async with self._session.post(API_URL, json=payload, timeout=15) as resp:
                if resp.status != 200:
                    raise UpdateFailed(f"API error {resp.status}")
                data = await resp.json()

            self._last_fetch_date = today
            self.today_str = today
            return self._parse_data(data)

        except Exception as err:
            raise UpdateFailed(f"Error communicating with amb.ch API: {err}") from err

    def _parse_data(self, raw: dict) -> dict:
        """Parse labels + bgColors into list of periods."""
        labels = raw.get("labels", [])
        colors = raw.get("bgColors", [])

        if len(labels) != len(colors):
            _LOGGER.warning("Labels and colors length mismatch")
            return {"periods": [], "current_color": "unknown"}

        periods = []
        current_color = None
        current_start = None

        for i, (ts_str, color) in enumerate(zip(labels, colors)):
            # Parse timestamp – remove +00:00 if needed
            ts_str_clean = ts_str.replace("+00:00", "")
            dt = datetime.fromisoformat(ts_str_clean)

            if i == 0:
                current_start = dt
                current_color = color

            if color != current_color or i == len(labels) - 1:
                # End of previous block
                periods.append({
                    "start": current_start,
                    "end": dt,  # end is start of next different block
                    "color": current_color,
                    "is_low": current_color == "#05DA3A",
                    "duration_minutes": (dt - current_start).total_seconds() / 60
                })
                current_start = dt
                current_color = color

        # Last block end = midnight next day (or last label + 15 min)
        if periods:
            last = periods[-1]
            if last["end"] == last["start"]:
                # Single point – assume 15 min
                last["end"] = last["start"] + timedelta(minutes=15)

        return {
            "periods": periods,
            "current_color": periods[0]["color"] if periods else "unknown",
            "fetch_date": self.today_str
        }
