sclass_details = [
    {
        "sclass": "Frigate", #ship class
        "size": "Small",
        "tam": 30, #total available mass
        "armor_roll": "3+",
        "mdpa": 9 #max damage per arc
    },
    {
        "sclass": "Destroyer",
        "size": "Small",
        "tam": 40,
        "armor_roll": "3+",
        "mdpa": 12
    }
]

equipment_details = [
    {
        "id": 0,
        "name": "None",
        "mass_factor": 0,
        "pv_factor": 0
    },
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

class Ship:
    def __init__(self, name, sclass, size, tam, armor_roll, mdpa): 
        
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

    def outer_hull(self, outer_hull_strength):
        mass_factor = [s['mass_factor'] for s in outer_strength_details if s['id'] == int(outer_hull_strength)]
        self.outer_hull_mass = round(self.tam[0] * mass_factor[0])
        self.outer_hull_pv = round(self.outer_hull_mass * 3)
        self.critical_threshold = round(self.outer_hull_mass * .3)
        return self.outer_hull_mass, self.outer_hull_pv, self.critical_threshold
        
    def inner_hull(self, inner_hull_strength):
        mass_factor = [s['mass_factor'] for s in inner_strength_details if s['id'] == int(inner_hull_strength)]
        self.inner_hull_mass = round(self.tam[0] * mass_factor[0])
        self.inner_hull_pv = round(self.outer_hull_mass * 3)
        return self.inner_hull_mass, self.inner_hull_pv

    def propulsion(self, thrust_points):
        self.thrust_points = thrust_points
        self.propulsion_mass = round(thrust_points * (self.tam[0] * .07))
        self.propulsion_pv = round(self.propulsion_mass * 2)
        self.max_thrust = round(thrust_points * 1.5)
        return self.thrust_points, self.propulsion_mass, self.propulsion_pv, self.max_thrust
    
    def weapons(self):
        #add mass check
        ...
    
    def equipment(self, equipment_list):
        for item in equipment_list:
            mass_factor = [s['mass_factor'] for s in equipment_details if s['id'] == int(item)]
            self.total_equipment_mass = round(ship.total_equipment_mass + (self.tam[0] * mass_factor[0]))
            pv_factor = [s['pv_factor'] for s in equipment_details if s['id'] == int(item)]
            self.total_equipment_pv = round(ship.total_equipment_pv + (self.total_equipment_mass * pv_factor[0]))
            
            self.equipment_names.append([s['name'] for s in equipment_details if s['id'] == int(item)])
            self.equipment_description = ', '.join([item for items in self.equipment_names for item in items])
        return self.total_equipment_mass, self.total_equipment_pv, self.equipment_description
    
    # def fixed_cost(self):
    #     self.fixed_cost_mass = round(self.tam[0] * .03)
    #     self.fixed_cost_pv = round(self.fixed_cost_mass * 2)
    #     return self.fixed_cost_mass, self.fixed_cost_pv
    
    def set_quality(self, crew_quality):
        self.crew_quality = crew_quality
        self.track_base_pv()
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

    def track_mass(self):
        self.total_mass = self.outer_hull_mass + self.inner_hull_mass + self.propulsion_mass + self.total_equipment_mass #+ self.fixed_cost_mass
        self.mass_delta = self.tam[0] - self.total_mass
        self.mass_exceeded = self.mass_delta < 0
        return self.total_mass, self.mass_delta, self.mass_exceeded
    
    def track_base_pv(self):
        self.total_base_pv = self.outer_hull_pv + self.inner_hull_pv + self.propulsion_pv + self.total_equipment_pv #+ self.fixed_cost_pv
        return self.total_base_pv

def build_base_ship():
    name = input("Ship Name: ")
    sclass = input(f"\nShip Class: ")
    size = [s['size'] for s in sclass_details if s['sclass'] == sclass]
    tam = [s['tam'] for s in sclass_details if s['sclass'] == sclass]
    armor_roll = [s['armor_roll'] for s in sclass_details if s['sclass'] == sclass]
    mdpa = [s['mdpa'] for s in sclass_details if s['sclass'] == sclass]
    return Ship(name, sclass, size, tam, armor_roll, mdpa)

if __name__ == "__main__":    
    ship = build_base_ship()
    
    outer_hull_strength = input(f"\nOuter Hull Strength (1-Light, 2-Average, 3-Heavy, 4-Ultra Heavy): ")
    ship.outer_hull(outer_hull_strength)
    print(ship.track_mass())

    inner_hull_strength = input(f"\nInner Hull Strength (1-Light, 2-Average, 3-Heavy, 4-Ultra Heavy): ")
    ship.inner_hull(inner_hull_strength)
    print(ship.track_mass())

    thrust_points = int(input(f"\nThrust Points: "))
    ship.propulsion(thrust_points)
    print(ship.track_mass())

    equipment_list = [item for item in
        input("\nEquipment (0-None, 1-Long Range Sensors, 2-Agile Thrusters, 3-Enhanced Engineering, 4-Advanced Fire Control, 5-Target Designator) separated by a comma: ").split(',')]
    ship.equipment(equipment_list)
    print(ship.track_mass())

    crew_quality = input(f"\nCrew Quality (Recruit, Regular, Veteran): ")
    ship.set_quality(crew_quality)

    ship.track_mass()
    ship.track_base_pv()

    #Print Ship Stats
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
    print(f"\nSelected equipment: {ship.equipment_description}")
    print(f"Total equipment mass: {ship.total_equipment_mass}")
    print(f"Total equipment PV: {ship.total_equipment_pv}")
    print(f"\nTotal Mass: {ship.total_mass}")
    print(f"Total Base PV: {ship.total_base_pv}")
    print(f"\nCrew Quality: {ship.crew_quality}")
    print(f"Max Stress: {ship.max_stress}")
    print(f"Final PV: {ship.final_pv}")

    # ship.fixed_cost()
    # print(f"\nFixed Cost (Fuel, Crew) Mass: {ship.fixed_cost_mass}")
    # print(f"Fixed Cost (Fuel, Crew) PV: {ship.fixed_cost_pv}")