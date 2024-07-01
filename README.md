# Space Ark Constructor
Space Ark Constructor is an in-development CLI and Web application to build ships for my [SPACE ARK miniature skirmish wargame](https://ryanlaliberty.itch.io/space-ark). It is meant as a replacement of the current [SPACE ARK Ship Builder](https://docs.google.com/spreadsheets/d/1gFEB0nsJ_nbAZvH3rNx8fDrZaWCASOcdjBhYto1-SyE/edit?gid=1120119713#gid=1120119713) Google Sheet. 

`ShipClass` is the primary Ship object class and includes methods for each ship construction step as well as helper methods to check if key ship attributes like mass and max damage exceed their thresholds.
`ship_constructor` is the CLI app for ship construction
`build_data` contains dicts from which `ShipClass` generates a ship
`ship_reader` will be a tool to read ship json files and pretty print them

## TODO
### ShipClass
* JSON ship design export method
* JSON gameplay ship card export method (requires lookup of weapon and equipment play stats)
### CLI App
* Input validation
* Error handling
* Menu-driven so ship construction steps can be accessed arbitratily
### Web App
* ...everything