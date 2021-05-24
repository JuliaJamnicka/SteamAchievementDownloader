# SteamAchievementDownloader
A tool that uses Steam Web API to download achievement data of players with public profiles and converts the data into an event log, e.g., for process mining analysis.

Any game that contains Steam achievements can be added to the Models.Game enum, with its value being the Steam app id. 

To download the achievement data, you can do this:

```
scraper = SteamScraper(Game.<ENUM_NAME>)
scraper.run()
```

The event log will be saved automatically to Logs as a CSV file.
Additionally, other player stats and the most common achievements are also saved in JSON files.
