"""Constants for the AMB Bellinzona integration."""

DOMAIN = "amb_bellinzona"
PLATFORMS = ["sensor", "binary_sensor"]

CONF_DATE = "date"  # not really used yet – we take today
API_URL = "https://www.amb.ch/Umbraco/Api/HivePower/GetChartData/"
UPDATE_INTERVAL = 3600  # 1 hour – but we can force daily reset
ATTRIBUTION = "Data from amb.ch HivePower"

COLOR_ALTA = "#E3051B"
COLOR_BASSA = "#05DA3A"
