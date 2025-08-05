"""Scraping logic for ORF Weather Forecast."""
import logging
import re
from datetime import datetime

import requests
from bs4 import BeautifulSoup

_LOGGER = logging.getLogger(__name__)

# This scraper is now fully standalone. It relies on the caller to provide the correct state URL.

# Attempt to import Home Assistant constants. If it fails, we are running standalone.
try:
    from homeassistant.components.weather import (
        ATTR_CONDITION_CLOUDY,
        ATTR_CONDITION_FOG,
        ATTR_CONDITION_LIGHTNING,
        ATTR_CONDITION_PARTLYCLOUDY,
        ATTR_CONDITION_RAINY,
        ATTR_CONDITION_SNOWY,
        ATTR_CONDITION_SNOWY_RAINY,
        ATTR_CONDITION_SUNNY,
    )

    CONDITION_MAP = {
        "wolkenlos": ATTR_CONDITION_SUNNY,
        "sonnig": ATTR_CONDITION_SUNNY,
        "heiter": ATTR_CONDITION_PARTLYCLOUDY,
        "wolkig": ATTR_CONDITION_CLOUDY,
        "bewölkt": ATTR_CONDITION_CLOUDY,
        "stark bewölkt": ATTR_CONDITION_CLOUDY,
        "bedeckt": ATTR_CONDITION_CLOUDY,
        "regnerisch": ATTR_CONDITION_RAINY,
        "Regen": ATTR_CONDITION_RAINY,
        "Schnee": ATTR_CONDITION_SNOWY,
        "Schneeregen": ATTR_CONDITION_SNOWY_RAINY,
        "Gewitter": ATTR_CONDITION_LIGHTNING,
        "Nebel": ATTR_CONDITION_FOG,
    }
    DEFAULT_CONDITION = ATTR_CONDITION_CLOUDY
except ImportError:
    _LOGGER.info("Running in standalone mode. Using string fallbacks for conditions.")
    CONDITION_MAP = {
        "wolkenlos": "sunny",
        "sonnig": "sunny",
        "heiter": "partlycloudy",
        "wolkig": "cloudy",
        "bewölkt": "cloudy",
        "stark bewölkt": "cloudy",
        "bedeckt": "cloudy",
        "regnerisch": "rainy",
        "Regen": "rainy",
        "Schnee": "snowy",
        "Schneeregen": "snowy-rainy",
        "Gewitter": "lightning",
        "Nebel": "fog",
    }
    DEFAULT_CONDITION = "cloudy"


def map_condition(text):
    text = text.lower()
    for k, v in CONDITION_MAP.items():
        if k in text:
            return v
    return DEFAULT_CONDITION


def parse_german_date(date_str, current_year):
    match = re.search(r"(\d{1,2})\.(\d{1,2})\.", date_str)
    if match:
        day = int(match.group(1))
        month = int(match.group(2))
        try:
            dt = datetime(current_year, month, day)
            return dt.date().isoformat()
        except Exception:
            return ""
    return ""


def split_temperature(temp_str):
    match = re.match(r"(\d+)[°º]C/(\d+)[°º]C", temp_str.replace("º", "°"))
    if match:
        return int(match.group(1)), int(match.group(2))
    return None, None


def fetch_forecast_for_place(place, state_url):
    """Fetches weather forecast data from wetter.orf.at."""
    url = f"https://wetter.orf.at/{state_url}/prognose"
    headers = {
        "User-Agent": "Mozilla/5.0 (compatible; WetterScraper/1.0; +https://wetter.orf.at/)"
    }
    try:
        response = requests.get(url, headers=headers)
        response.raise_for_status()
        soup = BeautifulSoup(response.content, "html.parser")
        tables = soup.find_all("table")
        current_year = datetime.now().year
        for table in tables:
            header_row = table.find("tr")
            header_cols = []
            if header_row:
                ths = header_row.find_all("th")
                if len(ths) > 1:
                    header_cols = [th.get_text(strip=True) for th in ths[1:]]
            if not header_cols:
                continue
            weather_row = None
            temp_row = None
            for row in table.find_all("tr"):
                th = row.find("th", class_="legendCol")
                if th:
                    th_text = th.get_text(strip=True)
                    if f"Prognose für {place}" in th_text:
                        weather_row = [td.get_text(strip=True) for td in row.find_all("td")]
                    elif f"Temperatur für{place}" in th_text or f"Temperatur für {place}" in th_text:
                        temp_row = [td.get_text(strip=True) for td in row.find_all("td")]
            if weather_row and temp_row and header_cols:
                data = []
                for date, weather, temp in zip(header_cols, weather_row, temp_row):
                    date_iso = parse_german_date(date, current_year)
                    temp_min, temp_max = split_temperature(temp)
                    if date_iso and temp_min is not None:
                        data.append(
                            {
                                "date_iso": date_iso,
                                "weather_text": weather,
                                "condition": map_condition(weather),
                                "temp_min": temp_min,
                                "temp_max": temp_max,
                            }
                        )
                return data
    except requests.exceptions.RequestException as e:
        _LOGGER.error(f"Error fetching data for '{place}': {e}")
    except Exception as e:
        _LOGGER.error(f"An error occurred during scraping for '{place}': {e}")
    return []