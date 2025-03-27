from homeassistant.components.update import UpdateEntity, UpdateEntityFeature
from homeassistant.helpers.update_coordinator import CoordinatorEntity
from homeassistant.helpers.entity import EntityCategory
from .const import DOMAIN
import aiohttp

async def async_setup_entry(hass, entry, async_add_entities):
    async_add_entities([MultiServiceUpdaterEntity(hass, entry)])

class MultiServiceUpdaterEntity(UpdateEntity):
    def __init__(self, hass, entry):
        self.hass = hass
        self.entry = entry
        self._attr_unique_id = f"{DOMAIN}_{entry.data['name']}"
        self._attr_name = f"{entry.data['name'].capitalize()} Update"
        self._attr_entity_category = EntityCategory.CONFIG
        self._attr_supported_features = UpdateEntityFeature.INSTALL

    @property
    def installed_version(self):
        state = self.hass.states.get(self.entry.data["current_version_sensor"])
        return state.state if state else None

    @property
    def latest_version(self):
        state = self.hass.states.get(self.entry.data["latest_version_sensor"])
        return state.state if state else None

    @property
    def available(self):
        return self.installed_version is not None and self.latest_version is not None

    async def async_install(self, version: str, backup: bool, **kwargs):
        url = self.entry.data["update_url"]
        token = self.entry.data["api_token"]

        headers = {
            "Authorization": f"Bearer {token}",
        }

        try:
            async with aiohttp.ClientSession() as session:
                async with session.post(url, headers=headers) as response:
                    if response.status != 200:
                        raise Exception(f"Update failed: {await response.text()}")
        except Exception as e:
            raise Exception(f"Update request failed: {e}")
