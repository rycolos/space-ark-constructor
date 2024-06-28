import json

sclass_details = [
    {
        "sclass": "Frigate",
        "size": "Small",
        "tam": 30,
        "armor": "3+" 
    },
    {
        "sclass": "Destroyer",
        "size": "Small",
        "tam": 40,
        "armor": "3+" 
    }
]

strength = ['Light', 'Average', 'Heavy', 'Ultra Heavy']

class Ship:
    def __init__(self, name, sclass, size, tam, armor, outer_hull_strength, inner_hull_strength,
                outer_hull_mass=None, outer_hull_pv=None, critical=None,
                inner_hull_mass=None, inner_hull_pv=None, total_pv=None):
        if not name:
            raise ValueError("Missing name")
        
        self.name = name 
        self.sclass = sclass
        self.size = size
        self.tam = tam
        self.armor = armor
        self.outer_hull_strength = outer_hull_strength
        self.outer_hull_mass = outer_hull_mass
        self.outer_hull_pv = outer_hull_pv
        self.critical = critical
        self.inner_hull_strength = inner_hull_strength
        self.inner_hull_mass = inner_hull_mass
        self.inner_hull_pv = inner_hull_pv
        self.total_pv = total_pv

    #ship class validation
    @property #getter
    def sclass(self):
        return self._sclass

    @sclass.setter #setter
    def sclass(self, sclass):
        if sclass not in [i['sclass'] for i in sclass_details]:
            raise ValueError("Invalid class")
        self._sclass = sclass

    #outer hull validation
    @property #getter
    def outer_hull_strength(self):
        return self._outer_hull_strength

    @sclass.setter #setter
    def outer_hull_strength(self, outer_hull_strength):
        if outer_hull_strength not in strength:
            raise ValueError("Invalid strength")
        self._outer_hull_strength = outer_hull_strength

    def outer_hull(self):
        match self._outer_hull_strength:
            case "Light":
                self.outer_hull_mass = self.tam[0] * .2
                self.outer_hull_pv = self.outer_hull_mass * 3
                return self.outer_hull_mass, self.outer_hull_pv
            case "Average":
                self.outer_hull_mass = self.tam[0] * .25
                self.outer_hull_pv = self.outer_hull_mass * 3
                return self.outer_hull_mass, self.outer_hull_pv
    
    def inner_hull(self):
        match self.inner_hull_strength:
            case "Light":
                self.inner_hull_mass = self.tam[0] * .05
                self.inner_hull_pv = self.inner_hull_mass * 3
                return self.inner_hull_mass, self.inner_hull_pv
            case "Average":
                self.inner_hull_mass = self.tam[0] * .1
                self.inner_hull_pv = self.inner_hull_mass * 3
                return self.inner_hull_mass, self.inner_hull_pv

    def critical_treshold(self):
        self.critical = self.outer_hull_mass * .3
        return self.critical

    def track_mass(self):
        ...
    
    def track_pv(self):
        self.total_pv = self.outer_hull_pv + self.inner_hull_pv
        return self.total_pv

def build_base_ship():
    name = input("Name: ")
    sclass = input("Class: ")
    size = [s['size'] for s in sclass_details if s['sclass'] == sclass]
    tam = [s['tam'] for s in sclass_details if s['sclass'] == sclass]
    armor = [s['armor'] for s in sclass_details if s['sclass'] == sclass]

    outer_hull_strength = input("Outer Hull Strength (Light, Average, Heavy, Ultra Heavy): ")
    inner_hull_strength = input("Inner Hull Strength (Light, Average, Heavy, Ultra Heavy): ")

    return Ship(name, sclass, size, tam, armor, outer_hull_strength, inner_hull_strength)

def load_ship(ship_file):
    with open(ship_file, 'r') as ship:
        parsed_ship = json.load(ship)
    return parsed_ship

if __name__ == "__main__":
    # parsed_ship = load_ship('ship_default.json')
    # for key, value in parsed_ship.items():
    #     print(f"{key}: {value}")
    
    ship = build_base_ship()
    print(f"\n**Your ship**\nName: {ship.name}\nClass: {ship.sclass}\nSize: {ship.size[0]}\nTotal Availble Mass: {ship.tam[0]}\nArmor: {ship.armor[0]}")
    
    ship.outer_hull()
    print(f"Outer Hull Mass: {ship.outer_hull_mass}")
    print(f"Outer Hull PV: {ship.outer_hull_pv}")
    
    ship.inner_hull()
    print(f"Inner Hull Mass: {ship.inner_hull_mass}")
    print(f"Inner Hull PV: {ship.inner_hull_pv}")

    ship.critical_treshold()
    print(f"Critical Threshold: {ship.critical}")

    ship.track_pv()
    print(f"Total PV: {ship.total_pv}")