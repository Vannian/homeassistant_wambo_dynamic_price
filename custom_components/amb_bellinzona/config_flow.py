from homeassistant import config_entries
from homeassistant.data_entry_flow import FlowResult

from .const import DOMAIN


class AMBBellinzonaFlow(config_entries.ConfigFlow, domain=DOMAIN):
    """Handle a config flow for AMB Bellinzona Dynamic Tariff."""

    VERSION = 1

    async def async_step_user(self, user_input=None) -> FlowResult:
            if self._async_current_entries():
                # Abort if already configured (prevents multiple identical entries)
                return self.async_abort(reason="single_instance_allowed")
    
            if user_input is not None:
                return self.async_create_entry(title="AMB Bellinzona", data=user_input or {})
    
            return self.async_show_form(step_id="user", data_schema={}, errors={})