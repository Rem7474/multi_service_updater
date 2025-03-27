from homeassistant.config_entries import ConfigEntry
from homeassistant.core import HomeAssistant

DOMAIN = "multi_service_updater"


async def async_setup(hass: HomeAssistant, config: dict):
    """Set up the integration from configuration.yaml (not used here)."""
    return True


async def async_setup_entry(hass: HomeAssistant, entry: ConfigEntry):
    """Set up the integration from a config entry (via UI)."""
    hass.data.setdefault(DOMAIN, {})
    await hass.config_entries.async_forward_entry_setup(entry, "update")
    return True


async def async_unload_entry(hass: HomeAssistant, entry: ConfigEntry):
    """Unload a config entry."""
    await hass.config_entries.async_forward_entry_unload(entry, "update")
    return True
