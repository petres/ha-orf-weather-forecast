"""Config flow for ORF Weather Forecast integration."""
from homeassistant import config_entries
from homeassistant.core import callback
import voluptuous as vol

from .const import DOMAIN, PLACE_INFO

PLACES = list(PLACE_INFO.keys())

class OrfWeatherForecastConfigFlow(config_entries.ConfigFlow, domain=DOMAIN):
    """Handle a config flow for ORF Weather Forecast."""

    VERSION = 1

    async def async_step_user(self, user_input=None):
        """Handle the initial step."""
        errors = {}
        if user_input is not None:
            return self.async_create_entry(
                title=f"ORF Weather Forecast ({user_input['place']})",
                data={"place": user_input["place"]}
            )

        return self.async_show_form(
            step_id="user",
            data_schema=vol.Schema({
                vol.Required("place", default=PLACES[0]): vol.In(PLACES)
            }),
            errors=errors
        )