from homeassistant.components.update import UpdateEntity, UpdateEntityFeature
from homeassistant.core import HomeAssistant
from homeassistant.helpers.update_coordinator import CoordinatorEntity
from homeassistant.config_entries import ConfigEntry
from homeassistant.helpers.entity_platform import AddEntitiesCallback
from homeassistant.helpers.typing import ConfigType, DiscoveryInfoType
from homeassistant.const import ATTR_NAME
import logging
import aiohttp

_LOGGER = logging.getLogger(__name__)

async def async_setup_entry(
    hass: HomeAssistant,
    config_entry: ConfigEntry,
    async_add_entities: AddEntitiesCallback
):
    """Set up the update entity from a config entry."""
    data = config_entry.data
    name = data.get("name")
    current_version_sensor = data.get("current_version_sensor")
    latest_version_sensor = data.get("latest_version_sensor")
    update_url = data.get("update_url")
    api_token = data.get("api_token")

    update_entity = MultiServiceUpdateEntity(
        hass, name, current_version_sensor, latest_version_sensor, update_url, api_token
    )
    async_add_entities([update_entity], update_before_add=True)


class MultiServiceUpdateEntity(UpdateEntity):
    """Representation of an updatable service."""

    def __init__(
        self,
        hass: HomeAssistant,
        name: str,
        current_version_sensor: str,
        latest_version_sensor: str,
        update_url: str,
        api_token: str
    ):
        self.hass = hass
        self._attr_name = name
        self._attr_unique_id = f"multi_service_updater_{name.lower()}"
        self.current_version_sensor = current_version_sensor
        self.latest_version_sensor = latest_version_sensor
        self.update_url = update_url
        self.api_token = api_token
        self._attr_supported_features = UpdateEntityFeature.INSTALL

    @property
    def installed_version(self) -> str | None:
        return self.hass.states.get(self.current_version_sensor).state if self.hass.states.get(self.current_version_sensor) else None

    @property
    def latest_version(self) -> str | None:
        return self.hass.states.get(self.latest_version_sensor).state if self.hass.states.get(self.latest_version_sensor) else None

    @property
    def available(self) -> bool:
        return self.installed_version is not None and self.latest_version is not None

    @property
    def title(self) -> str:
        return self._attr_name

    async def async_install(self, version: str | None = None, backup: bool = False, **kwargs) -> None:
        """Install the update by calling the external API."""
        if not self.update_url:
            _LOGGER.error("No update URL provided for %s", self._attr_name)
            return

        headers = {}
        if self.api_token:
            headers["Authorization"] = f"Bearer {self.api_token}"

        try:
            async with aiohttp.ClientSession() as session:
                async with session.post(self.update_url, headers=headers) as resp:
                    if resp.status != 200:
                        text = await resp.text()
                        _LOGGER.error("Failed to update %s: %s", self._attr_name, text)
                    else:
                        _LOGGER.info("Update triggered for %s", self._attr_name)
        except Exception as e:
            _LOGGER.error("Error updating %s: %s", self._attr_name, str(e))
