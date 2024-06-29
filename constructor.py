sclass_details = [
    {
        "sclass": "FRIGATE", #ship class
        "size": "Small",
        "tam": 30, #total available mass
        "armor_roll": "3+",
        "mdpa": 9 #max damage per arc
    },
    {
        "sclass": "DESTROYER",
        "size": "Small",
        "tam": 40,
        "armor_roll": "3+",
        "mdpa": 12
    }
]

equipment_details = [
    {
        "id": 1,
        "name": "None",
        "mass_factor": 0,
        "pv_factor": 0
    },
    {
        "id": 2,
        "name": "Long Range Sensors",
        "mass_factor": .04,
        "pv_factor": 9
    },
    {
        "id": 3,
        "name": "Agile Thrusters",
        "mass_factor": .05,
        "pv_factor": 9
    }
]

outer_strength_details = [
    {
        "id": 1,
        "name": "Light",
        "mass_factor": .2
    },
    {
        "id": 2,
        "name": "Average",
        "mass_factor": .25
    },
    {
        "id": 3,
        "name": "Heavy",
        "mass_factor": .3
    },
    {
        "id": 4,
        "name": "Ultra Heavy",
        "mass_factor": .35
    }
]

inner_strength_details = [
    {
        "id": 1,
        "name": "Light",
        "mass_factor": .05
    },
    {
        "id": 2,
        "name": "Average",
        "mass_factor": .1
    },
    {
        "id": 3,
        "name": "Heavy",
        "mass_factor": .15
    },
    {
        "id": 4,
        "name": "Ultra Heavy",
        "mass_factor": .20
    }
]

crew_quality_details = [
    {
        "id": 1,
        "name": "Recruit",
        "pv_factor": .8,
        "max_stress": 6 
    },
    {
        "id": 2,
        "name": "Regular",
        "pv_factor": 1,
        "max_stress": 7 
    },
    {
        "id": 3,
        "name": "Veteran",
        "pv_factor": 1.2,
        "max_stress": 8 
    }
]

class Ship:
    def __init__(self, name: str, sclass: str, size: str, tam: int, armor_roll: str, mdpa: int) -> None: 
        
        self.name = name 
        self.sclass = sclass
        self.size = size
        self.tam = tam
        self.armor_roll = armor_roll
        self.mdpa = mdpa

        self.equipment_names = []
        self.thrust_points = 0
        self.outer_hull_mass = 0
        self.inner_hull_mass = 0
        self.propulsion_mass = 0
        self.total_equipment_mass = 0
        self.outer_hull_pv = 0
        self.inner_hull_pv = 0
        self.propulsion_pv = 0
        self.total_equipment_pv = 0

    def outer_hull(self, outer_hull_strength: int) -> tuple[int, int, int]:
        """Calculate outer hull mass, PV, critical threshold"""

        mass_factor = [s['mass_factor'] for s in outer_strength_details if s['id'] == outer_hull_strength]
        self.outer_hull_mass = round(self.tam[0] * mass_factor[0])
        self.outer_hull_pv = round(self.outer_hull_mass * 3)
        self.critical_threshold = round(self.outer_hull_mass * .3)
        return self.outer_hull_mass, self.outer_hull_pv, self.critical_threshold
        
    def inner_hull(self, inner_hull_strength: int) -> tuple[int, int, int]:
        """Calculate inner hull mass, PV"""

        mass_factor = [s['mass_factor'] for s in inner_strength_details if s['id'] == inner_hull_strength]
        self.inner_hull_mass = round(self.tam[0] * mass_factor[0])
        self.inner_hull_pv = round(self.outer_hull_mass * 3)
        return self.inner_hull_mass, self.inner_hull_pv

    def propulsion(self, thrust_points: int) -> tuple[int, int, int, int]:
        """Calculate propulsion mass, pv, max_thrust"""
        self.thrust_points = thrust_points
        self.propulsion_mass = round(thrust_points * (self.tam[0] * .07))
        self.propulsion_pv = round(self.propulsion_mass * 2)
        self.max_thrust = round(thrust_points * 1.5)
        return self.thrust_points, self.propulsion_mass, self.propulsion_pv, self.max_thrust
    
    def weapons(self):
        #per arc - arc has weapon list (by id), total damage, total mass, total pv
            #check max damage
        #all weapons - total mass, total pv
            #check mass
        ...
    
    def equipment(self, *items) -> tuple[int, int, int, str]:
        """Calculate total equipment mass, total equipment pv and generate string list of equipment names"""
        for item in items:
            mass_factor = [s['mass_factor'] for s in equipment_details if s['id'] == item]
            self.total_equipment_mass = round(ship.total_equipment_mass + (self.tam[0] * mass_factor[0]))
            pv_factor = [s['pv_factor'] for s in equipment_details if s['id'] == item]
            self.total_equipment_pv = round(ship.total_equipment_pv + (self.total_equipment_mass * pv_factor[0]))
            name = [s["name"] for s in equipment_details if s['id'] == item]
            self.equipment_names.append(name[0])
        return self.total_equipment_mass, self.total_equipment_pv, self.equipment_names
    
    # def fixed_cost(self):
    #     self.fixed_cost_mass = round(self.tam[0] * .03)
    #     self.fixed_cost_pv = round(self.fixed_cost_mass * 2)
    #     return self.fixed_cost_mass, self.fixed_cost_pv
    
    def set_quality(self, crew_quality: int) -> tuple[int, int]:
        """Calculate final PV and retrieve Max Stress"""
        self.crew_quality = crew_quality
        self.track_base_pv()
        self.pv_factor = [s['pv_factor'] for s in crew_quality_details if s['id'] == crew_quality]
        self.final_pv = round(self.total_base_pv * self.pv_factor[0])
        self.max_stress = [s['max_stress'] for s in crew_quality_details if s['id'] == crew_quality]
        self.max_stress = self.max_stress[0]
        return self.final_pv, self.max_stress

    def track_mass(self) -> tuple[int, int, int]:
        """Calculate current mass, mass distance from TAM, and bool for if TAM exceeded"""
        self.total_mass = self.outer_hull_mass + self.inner_hull_mass + self.propulsion_mass + self.total_equipment_mass #+ self.fixed_cost_mass
        self.mass_delta = self.tam[0] - self.total_mass
        self.tam_exceeded = self.mass_delta < 0
        return self.total_mass, self.mass_delta, self.tam_exceeded
    
    def track_base_pv(self) -> int:
        """Calculate current base PV"""
        self.total_base_pv = self.outer_hull_pv + self.inner_hull_pv + self.propulsion_pv + self.total_equipment_pv #+ self.fixed_cost_pv
        return self.total_base_pv

###CLI BUILDER
def build_base_ship() -> Ship:
    """Instantiate base ship from name and class inputs"""

    name = input("Ship Name: ")
    sclass = input(f"\nShip Class (see docs for list): ").upper()
    size = [s['size'] for s in sclass_details if s['sclass'] == sclass]
    tam = [s['tam'] for s in sclass_details if s['sclass'] == sclass]
    armor_roll = [s['armor_roll'] for s in sclass_details if s['sclass'] == sclass]
    mdpa = [s['mdpa'] for s in sclass_details if s['sclass'] == sclass]
    return Ship(name, sclass, size, tam, armor_roll, mdpa)

def build_outer_hull():
    outer_hull_strength = int(input(f"\nOuter Hull Strength (1-Light, 2-Average, 3-Heavy, 4-Ultra Heavy): "))
    ship.outer_hull(outer_hull_strength)
    if mass_check_ui() == True:
        if input("Try again... Y/N? ").upper() == 'Y':
            build_outer_hull()

def build_inner_hull():
    inner_hull_strength = int(input(f"\nInner Hull Strength (1-Light, 2-Average, 3-Heavy, 4-Ultra Heavy): "))
    ship.inner_hull(inner_hull_strength) 
    if mass_check_ui() == True:
        if input("Try again... Y/N? ").upper() == 'Y':
            build_inner_hull()

def build_propulsion():
    thrust_points = int(input(f"\nThrust Points (number): "))
    ship.propulsion(thrust_points)
    if mass_check_ui() == True:
        if input("Try again... Y/N? ").upper() == 'Y':
            build_propulsion()

def build_equipment():
    equipment_list = list(map(int, input("\nEquipment (1-None, 2-Long Range Sensors, 3-Agile Thrusters, 4-Enhanced Engineering, 5-Advanced Fire Control, 6-Target Designator) separated by a comma: ").split(',')))
    ship.equipment(*equipment_list)
    if mass_check_ui() == True:
        if input("Try again... Y/N? ").upper() == 'Y':
            build_equipment()

def build_crew_quality():
    crew_quality = int(input(f"\nCrew Quality (1-Recruit, 2-Regular, 3-Veteran): "))
    ship.set_quality(crew_quality)

def mass_check_ui() -> bool:
    total_mass, mass_delta, tam_exceeded = ship.track_mass()
    if tam_exceeded == True:
        print(f"Mass exceeded! Mass overage: {mass_delta}")
    else:
        print(f"Current Mass: {total_mass}. Mass Remaining: {mass_delta}")
    return tam_exceeded

def show_ship():
    ship.track_mass()
    ship.track_base_pv()
    print(f"\n**YOUR SHIP**\nShip Name: {ship.name}\nClass: {ship.sclass}\nSize: {ship.size[0]}\nTotal Availble Mass: {ship.tam[0]}\nArmor: {ship.armor_roll[0]}\nMax Damage Per Arc: {ship.mdpa[0]}")
    print(f"\nOuter Hull Mass: {ship.outer_hull_mass}")
    print(f"Outer Hull PV: {ship.outer_hull_pv}")
    print(f"Critical Threshold: {ship.critical_threshold}")
    print(f"\nInner Hull Mass: {ship.inner_hull_mass}")
    print(f"Inner Hull PV: {ship.inner_hull_pv}")
    print(f"\nThrust Points: {ship.thrust_points}")
    print(f"Max Thrust: {ship.max_thrust}")
    print(f"Propulsion Mass: {ship.propulsion_mass}")
    print(f"Propulsion PV: {ship.propulsion_pv}")
    print(f"\nSelected equipment: {', '.join(ship.equipment_names)}")
    print(f"Total equipment mass: {ship.total_equipment_mass}")
    print(f"Total equipment PV: {ship.total_equipment_pv}")
    print(f"\nTotal Mass: {ship.total_mass}")
    print(f"Total Base PV: {ship.total_base_pv}")
    print(f"\nCrew Quality: {ship.crew_quality}")
    print(f"Max Stress: {ship.max_stress}")
    print(f"Final PV: {ship.final_pv}")

if __name__ == "__main__":    
    ship = build_base_ship()
    
    build_outer_hull()
    build_inner_hull()
    build_propulsion()
    build_equipment()
    build_crew_quality()
    show_ship()

    # ship.fixed_cost()
    # print(f"\nFixed Cost (Fuel, Crew) Mass: {ship.fixed_cost_mass}")
    # print(f"Fixed Cost (Fuel, Crew) PV: {ship.fixed_cost_pv}")