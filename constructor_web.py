from nicegui import ui
import build_data
from ShipClass import ShipClass
import json, jsonschema

ui.label('Space Ark Constructor')

ship_name = ui.input(label='Ship Name')
ship_class = ui.select(['Frigate', 'Destroyer'], label='Ship Class', value='Frigate')

ui.button('Build Ship',on_click=lambda: build_ship())
label = ui.label()

def build_ship():
    label.text = f"{ship_name.value}, {ship_class.value}"
    ship_name_int = ship_name.value
    ship_class_int = ship_class.value
    print(ship_name_int, ship_class_int)

ui.run(title='Space Ark Constructor')