# Candy-API-to-JSON

This python script is designed to communicate with Candy/Hoover washer dryers to produce a JSON readable by Home Assistant.

Tested and working on:

- Hoover DXW4H7A1TCEX-01 WIFI Tumble Dryer

## Getting the API Key

- Obtain the key for the machine using: https://github.com/MelvinGr/CandySimplyFi-tool

- Add your KEY and DEVICE_IP to candy.py and place in your Home Assistant config/pyscripts.

## Configuring Home Assistant

candy.py gets the data, decodes it and strips down the JSON to meet Home Assistants 255 character limit on sensors.

- example templates including translations of machine program codes can be found in configuration.yaml.
- example cards can be found in lovelace.yaml. These use custom:card-mod, custom:fold-entity-row and custom:config-template-card integrations.
