"""Weather platform for ORF Weather Forecast."""
from __future__ import annotations

import logging
from datetime import datetime

from homeassistant.components.weather import (
    Forecast,
    WeatherEntity,
    WeatherEntityFeature,
)
from homeassistant.const import UnitOfTemperature

from .const import DOMAIN, PLACE_INFO
from .orf_scraper import fetch_forecast_for_place

_LOGGER = logging.getLogger(__name__)

async def async_setup_entry(hass, config_entry, async_add_entities):
    """Set up via config entry."""
    place = config_entry.data.get("place", "Wien-Innere Stadt")
    if place not in PLACE_INFO:
        place = "Wien-Innere Stadt"
    async_add_entities([ORFWeatherEntity(hass, place)])

class ORFWeatherEntity(WeatherEntity):
    """Representation of an ORF weather forecast."""

    _attr_has_entity_name = True
    _attr_name = None
    _attr_native_temperature_unit = UnitOfTemperature.CELSIUS
    _attr_supported_features = WeatherEntityFeature.FORECAST_DAILY

    def __init__(self, hass, place):
        self.hass = hass
        self._place = place
        self._attr_name = f"{place} ORF Weather"
        self._attr_unique_id = f"orf_weather_{place.lower().replace(' ', '_').replace('-', '_')}"
        self._forecast_data = []

    async def async_update(self):
        """Fetch new forecast data and update state/attributes."""
        state_url = PLACE_INFO[self._place]["url"]
        self._forecast_data = await self.hass.async_add_executor_job(
            fetch_forecast_for_place, self._place, state_url
        )
        if not self._forecast_data:
            return

        today_iso = datetime.now().date().isoformat()
        current_weather_data = next(
            (row for row in self._forecast_data if row.get("date_iso") == today_iso),
            self._forecast_data[0],
        )

        self._attr_condition = current_weather_data["condition"]
        self._attr_native_temperature = current_weather_data["temp_max"]
        self._attr_native_templow = current_weather_data["temp_min"]

    @property
    def forecast(self) -> list[Forecast] | None:
        """Return the daily forecast."""
        if not self._forecast_data:
            return None
        return [
            {
                "datetime": row["date_iso"],
                "native_temperature": row["temp_max"],
                "native_templow": row["temp_min"],
                "condition": row["condition"],
            }
            for row in self._forecast_data
        ]

    async def async_forecast_daily(self) -> list[Forecast] | None:
        """Return the daily forecast."""
        return self.forecast