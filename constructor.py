import build_data
from ShipClass import ShipClass

def build_base_ship() -> ShipClass:
    """Instantiate base ship from name and class inputs"""

    name = input("Ship Name: ")
    sclass = input(f"\nShip Class (see docs for list): ").upper()
    size = [s['size'] for s in build_data.sclass_details if s['sclass'] == sclass]
    tam = [s['tam'] for s in build_data.sclass_details if s['sclass'] == sclass]
    armor_roll = [s['armor_roll'] for s in build_data.sclass_details if s['sclass'] == sclass]
    mdpa = [s['mdpa'] for s in build_data.sclass_details if s['sclass'] == sclass]
    return ShipClass(name, sclass, size, tam, armor_roll, mdpa)

def build_outer_hull() -> None:
    outer_hull_strength = int(input(f"\nOuter Hull Strength (1-Light, 2-Average, 3-Heavy, 4-Ultra Heavy): "))
    ship.outer_hull(outer_hull_strength)
    if mass_check_ui() == True:
        if input("Try again... Y/N? ").upper() == 'Y':
            ship.outer_hull_mass = 0
            ship.outer_hull_pv = 0
            build_outer_hull()

def build_inner_hull() -> None:
    inner_hull_strength = int(input(f"\nInner Hull Strength (1-Light, 2-Average, 3-Heavy, 4-Ultra Heavy): "))
    ship.inner_hull(inner_hull_strength) 
    if mass_check_ui() == True:
        if input("Try again... Y/N? ").upper() == 'Y':
            ship.inner_hull_mass = 0
            ship.inner_hull_pv = 0
            build_inner_hull()

def build_propulsion() -> None:
    thrust_points = int(input(f"\nThrust Points (number): "))
    ship.propulsion(thrust_points)
    if mass_check_ui() == True:
        if input("Try again... Y/N? ").upper() == 'Y':
            ship.propulsion_mass = 0
            ship.propulsion_pv = 0
            build_propulsion()

def build_equipment() -> None:
    equipment_list = list(map(int, input("\nEquipment (1-None, 2-Long Range Sensors, 3-Agile Thrusters, 4-Enhanced Engineering, 5-Advanced Fire Control, 6-Target Designator) separated by a comma: ").split(',')))
    ship.equipment(*equipment_list)
    if mass_check_ui() == True:
        if input("Try again... Y/N? ").upper() == 'Y':
            ship.total_equipment_mass = 0
            ship.total_equipment_pv = 0
            build_equipment()

def build_crew_quality() -> None:
    crew_quality = int(input(f"\nCrew Quality (1-Recruit, 2-Regular, 3-Veteran): "))
    ship.set_quality(crew_quality)

def mass_check_ui() -> bool:
    total_mass, mass_delta, tam_exceeded = ship.track_mass()
    if tam_exceeded == True:
        print(f"Mass exceeded! Mass overage: {mass_delta}")
    else:
        print(f"Current Mass: {total_mass}. Mass Remaining: {mass_delta}")
    return tam_exceeded

def show_ship() -> None:
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