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

equipment_details = [
    {
        "id": 1,
        "name": "Long Range Sensors",
        "mass_factor": .04,
        "pv_factor": 9
    },
    {
        "id": 2,
        "name": "Agile Thrusters",
        "mass_factor": .05,
        "pv_factor": 9
    }
]

strength_list = ['Light', 'Average', 'Heavy', 'Ultra Heavy']

class Ship:
    def __init__(self, name, sclass, size, tam, armor, outer_hull_strength, inner_hull_strength, thrust_points, crew_quality, equipment_list, equipment_names=None,
                outer_hull_mass=0, outer_hull_pv=0, critical=0, max_thrust=0, propulsion_mass=0, propulsion_pv=0,
                inner_hull_mass=0, inner_hull_pv=0, fixed_cost_mass=0, fixed_cost_pv=0, total_base_pv=0, total_mass=0, total_equipment_mass=0, total_equipment_pv=0):
        
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
        self.total_base_pv = total_base_pv
        self.total_mass = total_mass
        self.thrust_points = thrust_points
        self.max_thrust = max_thrust
        self.propulsion_mass = propulsion_mass
        self.propulsion_pv = propulsion_pv
        self.fixed_cost_mass = fixed_cost_mass
        self.fixed_cost_pv = fixed_cost_pv
        self.crew_quality = crew_quality
        self.equipment_list = equipment_list
        self.total_equipment_mass = total_equipment_mass
        self.total_equipment_pv = total_equipment_pv
        self.equipment_names = equipment_names

    def outer_hull(self):
        #add mass check
        match self.outer_hull_strength:
            case "Light":
                self.outer_hull_mass = round(self.tam[0] * .2)
                self.outer_hull_pv = round(self.outer_hull_mass * 3)
                print(self.track_mass())
                return self.outer_hull_mass, self.outer_hull_pv
            case "Average":
                self.outer_hull_mass = round(self.tam[0] * .25)
                self.outer_hull_pv = round(self.outer_hull_mass * 3)
                print(self.track_mass())
                return self.outer_hull_mass, self.outer_hull_pv
            case "Heavy":
                self.outer_hull_mass = round(self.tam[0] * .3)
                self.outer_hull_pv = round(self.outer_hull_mass * 3)
                print(self.track_mass())
                return self.outer_hull_mass, self.outer_hull_pv
            case "Ultra Heavy":
                self.outer_hull_mass = round(self.tam[0] * .35)
                self.outer_hull_pv = round(self.outer_hull_mass * 3)
                print(self.track_mass())
                return self.outer_hull_mass, self.outer_hull_pv
        

    def inner_hull(self):
        #add mass check
        match self.inner_hull_strength:
            case "Light":
                self.inner_hull_mass = round(self.tam[0] * .05)
                self.inner_hull_pv = round(self.inner_hull_mass * 3)
                print(self.track_mass())
                return self.inner_hull_mass, self.inner_hull_pv
            case "Average":
                self.inner_hull_mass = round(self.tam[0] * .1)
                self.inner_hull_pv = round(self.inner_hull_mass * 3)
                print(self.track_mass())
                return self.inner_hull_mass, self.inner_hull_pv
            case "Heavy":
                self.inner_hull_mass = round(self.tam[0] * .15)
                self.inner_hull_pv = round(self.inner_hull_mass * 3)
                print(self.track_mass())
                return self.inner_hull_mass, self.inner_hull_pv
            case "Ultra Heavy":
                self.inner_hull_mass = round(self.tam[0] * .2)
                self.inner_hull_pv = round(self.inner_hull_mass * 3)
                print(self.track_mass())
                return self.inner_hull_mass, self.inner_hull_pv

    def critical_treshold(self):
        self.critical = round(self.outer_hull_mass * .3)
        return self.critical

    def propulsion(self):
        #add mass check
        self.propulsion_mass = round(self.thrust_points * (self.tam[0] * .07))
        self.propulsion_pv = round(self.propulsion_mass * 2)
        self.max_thrust = round(self.thrust_points * 1.5)
        print(self.track_mass())
        return self.propulsion_mass, self.propulsion_pv, self.max_thrust
    
    def weapons(self):
        #add mass check
        ...
    
    def equipment(self):
        #add mass check
        self.equipment_names = []
        
        for item in self.equipment_list:
            mass_factor = [s['mass_factor'] for s in equipment_details if s['id'] == int(item)]
            self.total_equipment_mass = round(ship.total_equipment_mass + (self.tam[0] * mass_factor[0]))
            pv_factor = [s['pv_factor'] for s in equipment_details if s['id'] == int(item)]
            self.total_equipment_pv = round(ship.total_equipment_pv + (self.total_equipment_mass * pv_factor[0]))
            
            self.equipment_names.append([s['name'] for s in equipment_details if s['id'] == int(item)])
        return self.total_equipment_mass, self.equipment_names, self.total_equipment_pv
    
    def fixed_cost(self):
        self.fixed_cost_mass = round(self.tam[0] * .03)
        self.fixed_cost_pv = round(self.fixed_cost_mass * 2)
        return self.fixed_cost_mass, self.fixed_cost_pv
    
    def set_quality(self):
        match self.crew_quality:
            case "Recruit": 
                self.final_pv = round(self.total_base_pv * .8)
                self.max_stress = 6
                return self.final_pv, self.max_stress
            case "Regular": 
                self.final_pv = round(self.total_base_pv * 1)
                self.max_stress = 7
                return self.final_pv, self.max_stress
            case "Veteran": 
                self.final_pv = round(self.total_base_pv * 1.2)
                self.max_stress = 8
                return self.final_pv, self.max_stress

    def check_mass(self):
        ...

    def track_mass(self):
        self.total_mass = self.outer_hull_mass + self.inner_hull_mass + self.propulsion_mass + self.fixed_cost_mass + self.total_equipment_mass
        self.mass_delta = self.tam[0] - self.total_mass
        self.mass_exceeded = self.mass_delta < 0
        return self.total_mass, self.mass_delta, self.mass_exceeded
    
    def track_base_pv(self):
        self.total_base_pv = self.outer_hull_pv + self.inner_hull_pv + self.propulsion_pv + self.fixed_cost_pv + self.total_equipment_pv
        return self.total_base_pv

def build_base_ship():
    name = input("Name: ")

    sclass = input(f"\nClass: ")
    size = [s['size'] for s in sclass_details if s['sclass'] == sclass]
    tam = [s['tam'] for s in sclass_details if s['sclass'] == sclass]
    armor = [s['armor'] for s in sclass_details if s['sclass'] == sclass]

    outer_hull_strength = input(f"\nOuter Hull Strength (Light, Average, Heavy, Ultra Heavy): ")
    inner_hull_strength = input(f"\nInner Hull Strength (Light, Average, Heavy, Ultra Heavy): ")

    thrust_points = int(input(f"\nHow many thrust points? "))

    crew_quality = input(f"\nCrew Quality (Recruit, Regular, Veteran): ")

    equipment_list = []
    equipment_list = [item for item in
        input("\nSelect equipment (1-Long Range Sensors, 2-Agile Thrusters, 3-Enhanced Engineering, 4-Advanced Fire Control, 5-Target Designator) separated by a comma: ").split(',')]
    return Ship(name, sclass, size, tam, armor, outer_hull_strength, inner_hull_strength, thrust_points, crew_quality, equipment_list)

if __name__ == "__main__":    
    ship = build_base_ship()
    print(f"\n**Your ship**\nName: {ship.name}\nClass: {ship.sclass}\nSize: {ship.size[0]}\nTotal Availble Mass: {ship.tam[0]}\nArmor: {ship.armor[0]}")
    
    ship.outer_hull()
    print(f"\nOuter Hull Mass: {ship.outer_hull_mass}")
    print(f"Outer Hull PV: {ship.outer_hull_pv}")
    
    ship.inner_hull()
    print(f"\nInner Hull Mass: {ship.inner_hull_mass}")
    print(f"Inner Hull PV: {ship.inner_hull_pv}")

    ship.critical_treshold()
    print(f"\nCritical Threshold: {ship.critical}")

    ship.propulsion()
    print(f"\nThrust Points: {ship.thrust_points}")
    print(f"Max Thrust: {ship.max_thrust}")
    print(f"Propulsion Mass: {ship.propulsion_mass}")
    print(f"Propulsion PV: {ship.propulsion_pv}")

    ship.equipment()
    equipment_names = ', '.join([item for items in ship.equipment_names for item in items])
    print(f"\nSelected equipment: {equipment_names}")
    print(f"Total equipment mass: {ship.total_equipment_mass}")
    print(f"Total equipment PV: {ship.total_equipment_pv}")

    ship.fixed_cost()
    print(f"\nFixed Cost (Fuel, Crew) Mass: {ship.fixed_cost_mass}")
    print(f"Fixed Cost (Fuel, Crew) PV: {ship.fixed_cost_pv}")

    ship.track_mass()
    print(f"\nTotal Mass: {ship.total_mass}")

    ship.track_base_pv()
    print(f"\nTotal Base PV: {ship.total_base_pv}")

    ship.set_quality()
    print(f"\nCrew Quality: {ship.crew_quality}")
    print(f"Max Stress: {ship.max_stress}")
    print(f"Final PV: {ship.final_pv}")