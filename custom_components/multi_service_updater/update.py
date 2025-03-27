from homeassistant.components.update import UpdateEntity
from homeassistant.helpers.entity import EntityCategory

from .const import *

async def async_setup_entry(hass, entry, async_add_entities):
    async_add_entities([MultiServiceUpdaterEntity(hass, entry)])

class MultiServiceUpdaterEntity(UpdateEntity):
    def __init__(self, hass, entry):
        self.hass = hass
        self._entry = entry
        self._attr_name = f"{entry.data[CONF_NAME]} Updater"
        self._attr_unique_id = entry.entry_id
        self._attr_entity_category = EntityCategory.CONFIG

    @property
    def installed_version(self):
        return self.hass.states.get(self._entry.data[CONF_SENSOR_CURRENT]).state

    @property
    def latest_version(self):
        return self.hass.states.get(self._entry.data[CONF_SENSOR_LATEST]).state

    @property
    def title(self):
        return self._entry.data[CONF_NAME]

    async def async_install(self, version, backup, **kwargs):
        import aiohttp

        headers = {}
        token = self._entry.data.get(CONF_API_TOKEN)
        if token:
            headers["Authorization"] = f"Bearer {token}"

        async with aiohttp.ClientSession() as session:
            async with session.post(self._entry.data[CONF_UPDATE_URL], headers=headers) as resp:
                if resp.status != 200:
                    raise Exception(f"Update failed: {await resp.text()}")

    @property
    def supported_features(self):
        return self.Feature.INSTALL