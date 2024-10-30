# Space Ark Constructor
Space Ark Constructor is an in-development CLI and Web application to build ships for my [SPACE ARK miniature skirmish wargame](https://ryanlaliberty.itch.io/space-ark). It is meant as a replacement of the current [SPACE ARK Ship Builder](https://docs.google.com/spreadsheets/d/1gFEB0nsJ_nbAZvH3rNx8fDrZaWCASOcdjBhYto1-SyE/edit?gid=1120119713#gid=1120119713) Google Sheet. 

* `ShipClass` is the primary Ship object class and includes methods for each ship construction step as well as helper methods to check if key ship attributes like mass and max damage exceed their thresholds.
* `constructor__cli` is the CLI app for ship construction
* `constructor__web` is the web app for ship construction, built using the Streamlit framework
* `build_data` contains dicts from which `ShipClass` generates a ship