# AMB Bellinzona Dynamic Tariff for Home Assistant

[![hacs_badge](https://img.shields.io/badge/HACS-Custom-orange.svg)](https://github.com/hacs/integration)
![Version](https://img.shields.io/badge/version-1.0.0-blue.svg)
![Ticino](https://img.shields.io/badge/Region-Ticino-red.svg)

A custom integration for **Azienda Multiservizi Bellinzona (AMB)** customers in Ticino, Switzerland, who are on the **Dynamic Electricity Tariff**. 

This integration fetches the daily 15-minute price schedule directly from the AMB HivePower API and provides a binary sensor to automate your home based on "Alta" (Peak) and "Bassa" (Off-peak) periods.

## Features
- **Real-time Tariff Tracking:** Automatically identifies if you are currently in a High or Low tariff window.
- **15-Minute Precision:** Matches the exact resolution provided by the AMB dynamic graph.
- **Automation Ready:** Use the `binary_sensor.amb_alta_tariffa` to pause heavy appliances (washing machines, EV chargers, heat pumps) during expensive peaks.
- **Daily Updates:** Automatically fetches the new schedule every day (AMB publishes the next day's data after 12:00 PM).

---

## Installation

### Method 1: HACS (Recommended)
1. Open **HACS** in your Home Assistant instance.
2. Click on the three dots in the top right corner and select **Custom repositories**.
3. Paste the URL of your repository: `https://github.com/Vannian/homeassistant_wambo_dynamic_price`
4. Select **Integration** as the category and click **Add**.
5. Find "AMB Bellinzona Dynamic Tariff" in the list and click **Download**.
6. **Restart** Home Assistant.

### Method 2: Manual
1. Download the `custom_components` folder from this repo.
2. Copy the `amb_bellinzona` folder into your Home Assistant `/config/custom_components/` directory.
3. **Restart** Home Assistant.

---

## Configuration

Add the following to your `configuration.yaml`:


```yaml
amb_bellinzona: