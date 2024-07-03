import build_data
from ShipClass import ShipClass
from time import sleep

def build_base_ship() -> ShipClass:
    """Instantiate base ship from name and ship class inputs"""

    name = input("Ship Name: ")
    sclass = input(f"\nShip Class (see docs for list): ").upper()
    size = [s['size'] for s in build_data.sclass_details if s['sclass'] == sclass]
    tam = [s['tam'] for s in build_data.sclass_details if s['sclass'] == sclass]
    armor_roll = [s['armor_roll'] for s in build_data.sclass_details if s['sclass'] == sclass]
    mdpa = [s['mdpa'] for s in build_data.sclass_details if s['sclass'] == sclass]
    return ShipClass(name, sclass, size, tam, armor_roll, mdpa)

def build_outer_hull() -> None:
    """Calculate outer hull outputs from strength input"""
    outer_hull_strength = int(input(f"\nOuter Hull Strength (1-Light, 2-Average, 3-Heavy, 4-Ultra Heavy): "))
    ship.outer_hull(outer_hull_strength)
    if mass_check_ui() == True:
        if input("Try again... Y/N? ").upper() == 'Y':
            ship.outer_hull_mass = 0
            ship.outer_hull_pv = 0
            build_outer_hull()

def build_inner_hull() -> None:
    """Calculate inner hull outputs from strength input"""
    inner_hull_strength = int(input(f"\nInner Hull Strength (1-Light, 2-Average, 3-Heavy, 4-Ultra Heavy): "))
    ship.inner_hull(inner_hull_strength) 
    if mass_check_ui() == True:
        if input("Try again... Y/N? ").upper() == 'Y':
            ship.inner_hull_mass = 0
            ship.inner_hull_pv = 0
            build_inner_hull()

def build_propulsion() -> None:
    """Calculate propulsion outputs from thrust points input"""
    thrust_points = int(input(f"\nThrust Points (number): "))
    ship.propulsion(thrust_points)
    if mass_check_ui() == True:
        if input("Try again... Y/N? ").upper() == 'Y':
            ship.propulsion_mass = 0
            ship.propulsion_pv = 0
            build_propulsion()

def build_equipment() -> None:
    """Calculate equipment outputs from list input"""
    equipment_list = list(map(int, input("\nEquipment (1-None, 2-Long Range Sensors, 3-Agile Thrusters, 4-Enhanced Engineering, 5-Advanced Fire Control, 6-Target Designator) separated by a comma: ").split(',')))
    ship.equipment(*equipment_list)
    if mass_check_ui() == True:
        if input("Try again... Y/N? ").upper() == 'Y':
            ship.total_equipment_mass = 0
            ship.total_equipment_pv = 0
            build_equipment()

def build_weapons() -> None:
    """Calculate per-arc weapon outputs from list input"""
    weapon_selection = True
    print("\nWEAPON SELECTION:")
    while weapon_selection == True:
        arc = input(f"\nSelect arc (1-Front, 2-Rear, 3-Right, 4-Left) or C to continue: ").upper()
        match arc:
            case "1":
                front_list = list(map(str, input("\nSelect Front Arc weapons as comma-separated names. Leave empty for None: ").upper().split(', ')))
                ship.front_arc_weapons(*front_list)
                print(f"\nFront Arc Weapons: {', '.join(ship.front_arc_weapons_names)}")
                if mass_check_ui() == True:
                    if input("Try again... Y/N? ").upper() == 'Y':
                        ship.front_arc_weapons_names = []
                        ship.total_front_arc_mass = 0
                        ship.total_front_arc_pv = 0
                        ship.total_front_arc_max_dmg = 0
                if max_dmg_check_ui(ship.total_front_arc_max_dmg) == True:
                    if input("Try again... Y/N? ").upper() == 'Y':
                        ship.front_arc_weapons_names = []
                        ship.total_front_arc_mass = 0
                        ship.total_front_arc_pv = 0
                        ship.total_front_arc_max_dmg = 0
            case "2":
                rear_list = list(map(str, input("Select Rear Arc weapons as comma-separated names. Leave empty for None: ").upper().split(', ')))
                ship.rear_arc_weapons(*rear_list)
                print(f"\nRear Arc Weapons: {', '.join(ship.rear_arc_weapons_names)}")
                if mass_check_ui() == True:
                    if input("Try again... Y/N? ").upper() == 'Y':
                        ship.rear_arc_weapons_names = []
                        ship.total_rear_arc_mass = 0
                        ship.total_rear_arc_pv = 0
                        ship.total_rear_arc_max_dmg = 0
                if max_dmg_check_ui(ship.total_rear_arc_max_dmg) == True:
                    if input("Try again... Y/N? ").upper() == 'Y':
                        ship.rear_arc_weapons_names = []
                        ship.total_rear_arc_mass = 0
                        ship.total_rear_arc_pv = 0
                        ship.total_rear_arc_max_dmg = 0
            case "3":
                right_list = list(map(str, input("Select Right Arc weapons as comma-separated names. Leave empty for None: ").upper().split(', ')))
                ship.right_arc_weapons(*right_list)
                print(f"\nRight Arc Weapons: {', '.join(ship.right_arc_weapons_names)}")
                if mass_check_ui() == True:
                    if input("Try again... Y/N? ").upper() == 'Y':
                        ship.right_arc_weapons_names = []
                        ship.total_right_arc_mass = 0
                        ship.total_right_arc_pv = 0
                        ship.total_right_arc_max_dmg = 0
                if max_dmg_check_ui(ship.total_right_arc_max_dmg) == True:
                    if input("Try again... Y/N? ").upper() == 'Y':
                        ship.right_arc_weapons_names = []
                        ship.total_right_arc_mass = 0
                        ship.total_right_arc_pv = 0
                        ship.total_right_arc_max_dmg = 0
            case "4":
                left_list = list(map(str, input("Select Left Arc weapons as comma-separated names. Leave empty for None: ").upper().split(', ')))
                ship.left_arc_weapons(*left_list)
                print(f"\nLeft Arc Weapons: {', '.join(ship.left_arc_weapons_names)}")
                if mass_check_ui() == True:
                    if input("Try again... Y/N? ").upper() == 'Y':
                        ship.left_arc_weapons_names = []
                        ship.total_left_arc_mass = 0
                        ship.total_left_arc_pv = 0
                        ship.total_left_arc_max_dmg = 0
                if max_dmg_check_ui(ship.total_left_arc_max_dmg) == True:
                    if input("Try again... Y/N? ").upper() == 'Y':
                        ship.left_arc_weapons_names = []
                        ship.total_left_arc_mass = 0
                        ship.total_left_arc_pv = 0
                        ship.total_left_arc_max_dmg = 0
            case "C":
                weapon_selection = False

def build_crew_quality() -> None:
    """Calculate crew quality-driven outputs (final pv, max stress) from input"""
    crew_quality = int(input(f"\nCrew Quality (1-Recruit, 2-Regular, 3-Veteran): "))
    ship.set_quality(crew_quality)

def mass_check_ui() -> bool:
    """Check if total mass exceeds Total Available Mass, return bool"""
    total_mass, mass_delta, tam_exceeded = ship.track_mass()
    if tam_exceeded == True:
        print(f"Mass exceeded! Mass overage: {mass_delta}")
    else:
        print(f"Current Mass: {total_mass}. Mass Remaining: {mass_delta}")
    return tam_exceeded

def max_dmg_check_ui(arc: int) -> bool:
    """Check if total damage in given arc exceeds Max Damage Per Arc, return bool"""
    arc_max_dmg, max_dmg_delta, mdpa_exceeded = ship.track_max_dmg(arc)
    if mdpa_exceeded == True:
        print(f"Arc Max Damage exceeded! Max Damage overage: {max_dmg_delta}")
    else:
        print(f"Current Arc Max Damage: {arc_max_dmg}. Arc Max Damage Remaining: {max_dmg_delta}")
    return mdpa_exceeded

def show_ship() -> None:
    """Calcualte final mass and final base pv and print ship details"""
    ship.track_mass()
    ship.track_base_pv()
    print("Building ship...")
    sleep(1)
    print(f"\n**SHIP BUILD STATS **\nShip Name: {ship.name}\nClass: {ship.sclass}\nSize: {ship.size[0]}\nTotal Availble Mass: {ship.tam[0]}\nArmor: {ship.armor_roll[0]}\nMax Damage Per Arc: {ship.mdpa[0]}")
    
    print(f"\nOuter Hull Mass: {ship.outer_hull_mass}")
    print(f"Outer Hull PV: {ship.outer_hull_pv}")
    print(f"Critical Threshold: {ship.critical_threshold}")
    
    print(f"\nInner Hull Mass: {ship.inner_hull_mass}")
    print(f"Inner Hull PV: {ship.inner_hull_pv}")
    
    print(f"\nThrust Points: {ship.thrust_points}")
    print(f"Max Thrust: {ship.max_thrust}")
    print(f"Propulsion Mass: {ship.propulsion_mass}")
    print(f"Propulsion PV: {ship.propulsion_pv}")
    
    print(f"\nSelected Equipment: {', '.join(ship.equipment_names)}")
    print(f"Total Equipment Mass: {ship.total_equipment_mass}")
    print(f"Total Equipment PV: {ship.total_equipment_pv}")

    print(f"\nFront Arc Weapons: {', '.join(ship.front_arc_weapons_names)}")
    print(f"Total Front Arc Weapon Mass: {ship.total_front_arc_mass}")
    print(f"Total Front Arc Weapon PV: {ship.total_front_arc_pv}")
    print(f"Total Front Arc Max Damage: {ship.total_front_arc_max_dmg}")

    print(f"\nRear Arc Weapons: {', '.join(ship.rear_arc_weapons_names)}")
    print(f"Total Rear Arc Weapon Mass: {ship.total_rear_arc_mass}")
    print(f"Total Rear Arc Weapon PV: {ship.total_rear_arc_pv}")
    print(f"Total Rear Arc Max Damage: {ship.total_rear_arc_max_dmg}")

    print(f"\nRight Arc Weapons: {', '.join(ship.right_arc_weapons_names)}")
    print(f"Total Right Arc Weapon Mass: {ship.total_right_arc_mass}")
    print(f"Total Right Arc Weapon PV: {ship.total_right_arc_pv}")
    print(f"Total Right Arc Max Damage: {ship.total_right_arc_max_dmg}")

    print(f"\nLeft Arc Weapons: {', '.join(ship.left_arc_weapons_names)}")
    print(f"Total Left Arc Weapon Mass: {ship.total_left_arc_mass}")
    print(f"Total Left Arc Weapon PV: {ship.total_left_arc_pv}")
    print(f"Total Left Arc Max Damage: {ship.total_left_arc_max_dmg}")

    print(f"\nTotal Mass: {ship.total_mass}")
    print(f"Total Base PV: {ship.total_base_pv}")
    
    print(f"\nCrew Quality: {ship.crew_quality_str}")
    print(f"Max Stress: {ship.max_stress}")
    print(f"Final PV: {ship.final_pv}")

if __name__ == "__main__":    
    ship = build_base_ship()
    
    build_outer_hull()
    build_inner_hull()
    build_propulsion()
    build_equipment()
    build_weapons()
    build_crew_quality()
    show_ship()