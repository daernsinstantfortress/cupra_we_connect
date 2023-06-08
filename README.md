# Cupra We Connect
_Cupra We Connect ID sensor provides statistics from the Cupra ID Api thru [WeConnect-Cupra-python lib](https://pypi.org/project/weconnect-cupra-daern/)._

**This component will set up the following platforms.**

Platform | Description
-- | --
`sensor` | Show information from your Cupra Born car.
`button` | Start climatization in your Cupra Born car.

![image](https://user-images.githubusercontent.com/15835274/149675681-a0c6804c-3179-4fd3-ad74-ab489c8986dd.png)


## Installation

### HACS
The easiest way to add this to your Homeassistant installation is using [HACS](https://custom-components.github.io/hacs/) and add this repository as a custom repository. And then follow the instructions under [Configuration](#configuration) below.

### Manual

1. Using the tool of choice open the directory (folder) for your HA configuration (where you find `configuration.yaml`).
2. If you do not have a `custom_components` directory (folder) there, you need to create it.
3. In the `custom_components` directory (folder) create a new folder called `cupra_we_connect`.
4. Download _all_ the files from the `custom_components/cupra_we_connect/` directory (folder) in this repository.
5. Place the files you downloaded in the new directory (folder) you created.
6. Follow the instructions under [Configuration](#configuration) below.

Using your HA configuration directory (folder) as a starting point you should now also have this:

```text
custom_components/cupra_we_connect/__init__.py
custom_components/cupra_we_connect/manifest.json
custom_components/cupra_we_connect/sensor.py
.. etc
```

##  Configuration 

It's important that you first use the app, connect the app to the car and use it at least once. 
After that enable the integration on the integration page in Home Assistant with your e-mail and password that you use to login into the app. Wait a couple of seconds and 1 or more devices (your cars) with entities will show up. 

## Tested Cars

* Cupra Born 2021-

## Requirements

Home Assistant Core *2022.7.0* or higher

## Thanks
Many thanks to @mitch-dc for the original implementation of the VW ID integration upon which this is based