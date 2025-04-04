from homeassistant import config_entries
import voluptuous as vol
from .const import DOMAIN

class MultiServiceUpdaterConfigFlow(config_entries.ConfigFlow, domain=DOMAIN):
    async def async_step_user(self, user_input=None):
        if user_input is not None:
            return self.async_create_entry(title=user_input["name"], data=user_input)

        return self.async_show_form(
            step_id="user",
            data_schema=vol.Schema({
                vol.Required("name"): str,
                vol.Required("current_version_sensor"): str,
                vol.Required("latest_version_sensor"): str,
                vol.Required("update_url"): str,
                vol.Required("api_token"): str,
            }),
        )
