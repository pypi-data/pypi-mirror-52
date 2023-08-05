# Australian Weather Data (using bom.gov.au)
Access to the Australian [Bureau of Meteorology](https://bom.gov.au/) weather data.

[![Actions Status](https://github.com/tonyallan/weather-au/workflows/weather-au-build/badge.svg)](https://github.com/tonyallan/weather-au/actions)

Currently a work in progress!

## Disclaimer

This project is not related to nor is it endorsed by the Australian Bureau of Meteorology (BOM). 

From the BOM [copyright notice](http://reg.bom.gov.au/other/copyright.shtml): Where no terms of use are associated with a set of material, then you may download, use and copy that material for personal use, or use within your organisation but you may not supply that material to any other person or use it for any commercial purpose.

## Usage

### observations

```python3
from weather import observations

# Read and parse the XML file ftp://ftp.bom.gov.au/anon/gen/fwo/IDV60920.xml
obs = observations.Observations('Vic')

# Print the product ID associated with this XML file
print(f'Product ID: {obs.identifier}\n')

# <observations>
for station in obs.stations():

    # <station wmo-id="95936" ... description="Melbourne (Olympic Park)">
    wmo_id = station['wmo-id']                                  
    description = station['description']

    # <element units="Celsius" type="air_temperature">9.8</element>
    air_temperature = obs.air_temperature(station['wmo-id'])

    if air_temperature is None:
        print(f'{wmo_id} {description}')
    else:
        print(f'{wmo_id} {description}   ({air_temperature})')
```

Produces output:
```
Product ID: IDV60920

95936 Melbourne (Olympic Park)   (10.8)
94866 Melbourne Airport   (9.1)
94854 Avalon   (10.2)
```

### place

```python3
from weather import place

# Parse http://www.bom.gov.au/places/vic/parkville
obsp = place.Place('vic', 'parkville')

air_temperature = obsp.air_temperature()
station_id = obsp.station_id()

print(f'Station ID: {station_id}\nAir Temperature: {air_temperature}')
```

Produces output:
```
Station ID: 95936
Air Temperature: 10.8
```

### uv_index

```python3
from weather import uv_index

obs = uv_index.UvIndex('Vic')

print(f'Product ID: {obs.identifier}\n')

for area in obs.area():

    aac = area['aac']                                  
    description = area['description']
    print(f'{aac} {description}')

# VIC_PT042 Melbourne
print(obs.uv_alert('VIC_PT042'))
```

Produces output:
```
Product ID: IDZ00112

VIC_PT001 Aireys Inlet
VIC_PT002 Ararat
VIC_PT003 Avalon
...
Sun protection recommended from 10:30 am to  2:00 pm, UV Index predicted to reach 4 [Moderate]
```

## URL's

- Base for anon FTP data `ftp://ftp.bom.gov.au/anon/gen/`
- Capital City Observations - VIC - Melbourne (Olympic Park) `http://www.bom.gov.au/fwo/IDV60901/IDV60901.95936.json`
  - where `IDV60901` is the product, and
  - `95936` is the weather station id.
- Weather Observations - VIC - Melbourne (Olympic Park) `http://www.bom.gov.au/fwo/IDV60910/IDV60910.95936.json`
- `http://www.bom.gov.au/places/vic/parkville/`

## Resources

1. [FTP public products](http://www.bom.gov.au/catalogue/anon-ftp.shtml)
1. [Weather Data Services](http://www.bom.gov.au/catalogue/data-feeds.shtml)
1. [How to use BOM API for weather, tide and swell](https://stackoverflow.com/questions/39534018/how-to-use-bom-api-for-weather-tide-and-swell)
1. [Github has a number of projects using bom.gov.au data](https://github.com/search?q=bom.gov.au)
1. [256 km Melbourne Radar Loop](http://www.bom.gov.au/products/IDR022.loop.shtml)
1. [Catalogue of RSS Feeds](http://www.bom.gov.au/rss/)

