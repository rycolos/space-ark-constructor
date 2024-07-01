import json

def load_ship(ship_file):
    with open(ship_file, 'r') as ship:
        parsed_ship = json.load(ship)
    return parsed_ship

if __name__ == "__main__":
    parsed_ship = load_ship('ship_default.json')
    for key, value in parsed_ship.items():
        print(f"{key}: {value}")