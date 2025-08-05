## ORF Weather Forecast - Home Assistant Custom Component

[![Open your Home Assistant instance and open a repository inside the Home Assistant Community Store.](https://my.home-assistant.io/badges/hacs_repository.svg)](https://my.home-assistant.io/redirect/hacs_repository/?owner=petres&repository=ha-orf-weather-forecast)

This custom Home Assistant component offers a weather entity that extracts the daily forecast from the Austrian public broadcaster's website, [wetter.orf.at](https://wetter.orf.at). It delivers a 5-day weather forecast for various locations throughout Austria.

Residing in the inner area of Vienna, I've observed that many forecasts tend to underestimate the maximum and minimum temperatures. Whether this is also the case for other locations, I cannot say.


###  Locations

*Wien*: Wien-Innere Stadt, Wien-Hohe Warte  
*Burgenland*: Eisenstadt, Kleinzicken  
*Kärnten*: Klagenfurt, Dellach im Drautal  
*Niederösterreich*: St. Pölten, Stift Zwettl  
*Oberösterreich*: Linz-Stadt, Gmunden  
*Salzburg*: Salzburg-Freisaal, Mariapfarr  
*Steiermark*: Graz-Universität, Aigen im Ennstal  
*Tirol*: Innsbruck, Lienz  
*Vorarlberg*: Bregenz, Brand


### Installation

Home Assistant instance with HACS installed is required.

1.  Go to your Home Assistant's **HACS** page and click the three dots in the top right corner and select **Custom repositories**.
2.  Fill the `Repository` field with `petres/ha-orf-weather-forecast` and select `Integration` as the category. Click **Add**.
3.  The "ORF Weather Forecast" integration will now be available in HACS. Click **Install**.
4.  Restart Home Assistant.
5.  Add the device `ORF Weather Forecast` in Home Assistant.

Now you could add a card like

```
  - type: weather-forecast
    entity: weather.wien_innere_stadt_orf_weather
    forecast_type: daily
    show_current: false
```

to add it to your dashboard.

### Disclaimer

**No Affiliation:** This project is not affiliated with, endorsed by, or in any way officially connected with the ORF (Österreichischer Rundfunk). It is an independent, open-source project that utilizes publicly available data.

**AI-Generated Code:** This custom component was largely developed with the assistance of an AI language model. While it has been tested, it may contain bugs or unforeseen issues. Please use it with this understanding.

**Web Scraping Fragility:** This component relies on web scraping the ORF website. If the structure of the website changes, this integration may break. If you encounter issues, please check the repository for updates or file an issue.

### Contributing

Contributions are welcome! If you would like to improve the component, please feel free to submit a pull request.
