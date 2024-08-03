import build_data
from ShipClass import ShipClass
from time import sleep
import json

MENU_ERROR = "Invalid selection. Try again."

def build_base_ship() -> ShipClass:
    """Instantiate base ship from name and ship class inputs"""

    name = input("Ship Name: ")
    sclass = input(f"\nShip Class (see docs for list): ").upper()
    size = [s['size'] for s in build_data.sclass_details if s['sclass'] == sclass]
    tam = [s['tam'] for s in build_data.sclass_details if s['sclass'] == sclass]
    armor_roll = [s['armor_roll'] for s in build_data.sclass_details if s['sclass'] == sclass]
    mdpa = [s['mdpa'] for s in build_data.sclass_details if s['sclass'] == sclass]
    return ShipClass(name, sclass, size[0], tam[0], armor_roll[0], mdpa[0])

def build_outer_hull(ship: ShipClass) -> None:
    """Calculate outer hull outputs from strength input"""
    #ohs_input = int(input(f"\nOuter Hull Strength (1-Light, 2-Average, 3-Heavy, 4-Ultra Heavy): "))
    while True:
        ohs_input = input(f"\nOuter Hull Strength (1-Light, 2-Average, 3-Heavy, 4-Ultra Heavy): ")
        try: #if no error raised in class, continue
            ship.outer_hull(ohs_input)
            if mass_check_ui(ship) == True:
                if input("Try again... Y/N? ").upper() == 'Y':
                    ship.outer_hull_mass = 0
                    ship.outer_hull_pv = 0
                    build_outer_hull(ship)
            break
        except Exception as e:
            print(e)

def build_inner_hull(ship: ShipClass) -> None:
    """Calculate inner hull outputs from strength input"""
    while True:
        ihs_input = input(f"\nInner Hull Strength (1-Light, 2-Average, 3-Heavy, 4-Ultra Heavy): ")
        try: #if no error raised in class, continue
            ship.inner_hull(ihs_input)
            if mass_check_ui(ship) == True:
                if input("Try again... Y/N? ").upper() == 'Y':
                    ship.inner_hull_mass = 0
                    ship.inner_hull_pv = 0
                    build_inner_hull(ship)
            break
        except Exception as e:
            print(e)

def build_propulsion(ship: ShipClass) -> None:
    """Calculate propulsion outputs from thrust points input"""
    while True:
        tp_input = input(f"\nThrust Points (number): ")
        try: #if no error raised in class, continue
            ship.propulsion(tp_input)
            if mass_check_ui(ship) == True:
                if input("Try again... Y/N? ").upper() == 'Y':
                    ship.propulsion_mass = 0
                    ship.propulsion_pv = 0
                    build_propulsion(ship)
            break
        except Exception as e:
            print(e)

def build_equipment(ship: ShipClass) -> None:
    """Calculate equipment outputs from list input, returns equipment name list from equipment object"""
    while True:
        equipment_list = list(map(str, input("\nEquipment (1-None, 2-Long Range Sensors, 3-Agile Thrusters, 4-Enhanced Engineering, 5-Advanced Fire Control, 6-Target Designator) separated by a comma: ").split(',')))
        try:
            ship.equipment(*equipment_list)
            if mass_check_ui(ship) == True:
                if input("Try again... Y/N? ").upper() == 'Y':
                    ship.total_equipment_mass = 0
                    ship.total_equipment_pv = 0
                    build_equipment(ship)
            break
        except Exception as e:
            print(e)

def build_weapons(ship: ShipClass) -> None:
    """Calculate per-arc weapon outputs from list input"""
    front_arc_weapon_names = []
    rear_arc_weapon_names = []
    right_arc_weapon_names = []
    left_arc_weapon_names = []

    print("\nWEAPON SELECTION:")
    while True:
        arc = input(f"\nSelect arc (1-Front, 2-Rear, 3-Right, 4-Left) or C to continue: ").upper()
        match arc:
            case "1":
                while True:
                    front_list = list(map(str, input("\nSelect Front Arc weapons as comma-separated names. Leave empty for None: ").upper().split(', ')))
                    if front_list == ['']: #empty input
                        front_arc_weapon_names = []
                        ship.total_front_arc_mass = 0
                        ship.total_front_arc_pv = 0
                        ship.total_front_arc_max_dmg = 0
                        print(f"\nFront Arc Weapons: None")
                        break
                    else:
                        try:
                            ship.front_arc_weapons(*front_list)
                            front_arc_weapon_names = [i["name"] for i in ship.front_arc_weapon_list]
                            print(f"\nFront Arc Weapons: {', '.join(front_arc_weapon_names)}")
                            if mass_check_ui(ship) == True:
                                if input("Try again... Y/N? ").upper() == 'Y':
                                    front_arc_weapon_names = []
                                    ship.total_front_arc_mass = 0
                                    ship.total_front_arc_pv = 0
                                    ship.total_front_arc_max_dmg = 0
                            if max_dmg_check_ui(ship, ship.total_front_arc_max_dmg) == True:
                                if input("Try again... Y/N? ").upper() == 'Y':
                                    front_arc_weapon_names = []
                                    ship.total_front_arc_mass = 0
                                    ship.total_front_arc_pv = 0
                                    ship.total_front_arc_max_dmg = 0
                            break
                        except Exception as e:
                            print(e)
            case "2":
                while True:
                    rear_list = list(map(str, input("Select Rear Arc weapons as comma-separated names. Leave empty for None: ").upper().split(', ')))
                    if rear_list == ['']: #empty input
                        rear_arc_weapon_names = []
                        ship.total_rear_arc_mass = 0
                        ship.total_rear_arc_pv = 0
                        ship.total_rear_arc_max_dmg = 0
                        print(f"\nRear Arc Weapons: None")
                        break
                    else:
                        try:
                            ship.rear_arc_weapons(*rear_list)
                            rear_arc_weapon_names = [i["name"] for i in ship.rear_arc_weapon_list]
                            print(f"\nRear Arc Weapons: {', '.join(rear_arc_weapon_names)}")
                            if mass_check_ui(ship) == True:
                                if input("Try again... Y/N? ").upper() == 'Y':
                                    rear_arc_weapon_names = []
                                    ship.total_rear_arc_mass = 0
                                    ship.total_rear_arc_pv = 0
                                    ship.total_rear_arc_max_dmg = 0
                            if max_dmg_check_ui(ship, ship.total_rear_arc_max_dmg) == True:
                                if input("Try again... Y/N? ").upper() == 'Y':
                                    rear_arc_weapon_names = []
                                    ship.total_rear_arc_mass = 0
                                    ship.total_rear_arc_pv = 0
                                    ship.total_rear_arc_max_dmg = 0
                            break
                        except Exception as e:
                            print(e)
            case "3":
                while True:
                    right_list = list(map(str, input("Select Right Arc weapons as comma-separated names. Leave empty for None: ").upper().split(', ')))
                    if right_list == ['']: #empty input
                        right_arc_weapon_names = []
                        ship.total_right_arc_mass = 0
                        ship.total_right_arc_pv = 0
                        ship.total_right_arc_max_dmg = 0
                        print(f"\nRight Arc Weapons: None")
                        break
                    else:
                        try:
                            ship.right_arc_weapons(*right_list)
                            right_arc_weapon_names = [i["name"] for i in ship.right_arc_weapon_list]
                            print(f"\nRight Arc Weapons: {', '.join(right_arc_weapon_names)}")
                            if mass_check_ui(ship) == True:
                                if input("Try again... Y/N? ").upper() == 'Y':
                                    right_arc_weapon_names = []
                                    ship.total_right_arc_mass = 0
                                    ship.total_right_arc_pv = 0
                                    ship.total_right_arc_max_dmg = 0
                            if max_dmg_check_ui(ship, ship.total_right_arc_max_dmg) == True:
                                if input("Try again... Y/N? ").upper() == 'Y':
                                    right_arc_weapon_names = []
                                    ship.total_right_arc_mass = 0
                                    ship.total_right_arc_pv = 0
                                    ship.total_right_arc_max_dmg = 0
                            break
                        except Exception as e:
                            print(e)
            case "4":                
                while True:
                    left_list = list(map(str, input("Select Left Arc weapons as comma-separated names. Leave empty for None: ").upper().split(', ')))
                    if left_list == ['']: #empty input
                        left_arc_weapon_names = []
                        ship.total_left_arc_mass = 0
                        ship.total_left_arc_pv = 0
                        ship.total_left_arc_max_dmg = 0
                        print(f"\nLeft Arc Weapons: None")
                        break
                    else:
                        try:
                            ship.left_arc_weapons(*left_list)
                            left_arc_weapon_names = [i["name"] for i in ship.left_arc_weapon_list]
                            print(f"\nLeft Arc Weapons: {', '.join(left_arc_weapon_names)}")
                            if mass_check_ui(ship) == True:
                                if input("Try again... Y/N? ").upper() == 'Y':
                                    left_arc_weapon_names = []
                                    ship.total_left_arc_mass = 0
                                    ship.total_left_arc_pv = 0
                                    ship.total_left_arc_max_dmg = 0
                            if max_dmg_check_ui(ship, ship.total_left_arc_max_dmg) == True:
                                if input("Try again... Y/N? ").upper() == 'Y':
                                    left_arc_weapon_names = []
                                    ship.total_left_arc_mass = 0
                                    ship.total_left_arc_pv = 0
                                    ship.total_left_arc_max_dmg = 0
                            break
                        except Exception as e:
                            print(e)
            case "C":
                break
            case _: #match any other entry
                print(MENU_ERROR)

def build_crew_quality(ship: ShipClass) -> None:
    """Calculate crew quality-driven outputs (final pv, max stress) from input"""
    crew_quality = int(input(f"\nCrew Quality (1-Recruit, 2-Regular, 3-Veteran): "))
    ship.set_quality(crew_quality)

def mass_check_ui(ship: ShipClass) -> bool:
    """Check if total mass exceeds Total Available Mass, return bool"""
    total_mass, mass_delta, tam_exceeded = ship.track_mass()
    if tam_exceeded == True:
        print(f"Mass exceeded! Mass overage: {mass_delta}")
    else:
        print(f"Current Mass: {total_mass}. Mass Remaining: {mass_delta}")
    return tam_exceeded

def max_dmg_check_ui(ship: ShipClass, arc: int) -> bool:
    """Check if total damage in given arc exceeds Max Damage Per Arc, return bool"""
    arc_max_dmg, max_dmg_delta, mdpa_exceeded = ship.track_max_dmg(arc)
    if mdpa_exceeded == True:
        print(f"Arc Max Damage exceeded! Max Damage overage: {max_dmg_delta}")
    else:
        print(f"Current Arc Max Damage: {arc_max_dmg}. Arc Max Damage Remaining: {max_dmg_delta}")
    return mdpa_exceeded

def reset_stats(ship: ShipClass):
    if input("\nReset all ship stats to class defaults? (Y/N): ").upper() == 'Y':
        ship.reset_all_stats()
    else:
        pass

def show_ship_build_stats(ship: ShipClass) -> None:
    """Calcualte final mass and final base pv and print ship details"""
    ship.track_mass()
    ship.track_base_pv()

    print(f"\n**SHIP BUILD STATS **\nShip Name: {ship.name}\nClass: {ship.sclass.capitalize()}\nSize: {ship.size}\nTotal Availble Mass: {ship.tam}\nArmor: {ship.armor_roll}\nMax Damage Per Arc: {ship.mdpa}")
    
    print(f"\nOuter Hull Mass: {ship.outer_hull_mass}")
    print(f"Outer Hull PV: {ship.outer_hull_pv}")
    print(f"Critical Threshold: {ship.critical_threshold}")
    
    print(f"\nInner Hull Mass: {ship.inner_hull_mass}")
    print(f"Inner Hull PV: {ship.inner_hull_pv}")
    
    print(f"\nThrust Points: {ship.thrust_points}")
    print(f"Max Thrust: {ship.max_thrust}")
    print(f"Propulsion Mass: {ship.propulsion_mass}")
    print(f"Propulsion PV: {ship.propulsion_pv}")
    
    equipment_names = [i["name"] for i in ship.equipment_list]
    print(f"\nSelected Equipment: {', '.join(equipment_names)}")
    print(f"Total Equipment Mass: {ship.total_equipment_mass}")
    print(f"Total Equipment PV: {ship.total_equipment_pv}")

    front_arc_weapon_names = [i["name"] for i in ship.front_arc_weapon_list]
    print(f"\nFront Arc Weapons: {', '.join(front_arc_weapon_names)}")
    print(f"Total Front Arc Weapon Mass: {ship.total_front_arc_mass}")
    print(f"Total Front Arc Weapon PV: {ship.total_front_arc_pv}")
    print(f"Total Front Arc Max Damage: {ship.total_front_arc_max_dmg}")

    rear_arc_weapon_names = [i["name"] for i in ship.rear_arc_weapon_list]
    print(f"\nRear Arc Weapons: {', '.join(rear_arc_weapon_names)}")
    print(f"Total Rear Arc Weapon Mass: {ship.total_rear_arc_mass}")
    print(f"Total Rear Arc Weapon PV: {ship.total_rear_arc_pv}")
    print(f"Total Rear Arc Max Damage: {ship.total_rear_arc_max_dmg}")

    right_arc_weapon_names = [i["name"] for i in ship.right_arc_weapon_list]   
    print(f"\nRight Arc Weapons: {', '.join(right_arc_weapon_names)}")
    print(f"Total Right Arc Weapon Mass: {ship.total_right_arc_mass}")
    print(f"Total Right Arc Weapon PV: {ship.total_right_arc_pv}")
    print(f"Total Right Arc Max Damage: {ship.total_right_arc_max_dmg}")

    left_arc_weapon_names = [i["name"] for i in ship.left_arc_weapon_list]
    print(f"\nLeft Arc Weapons: {', '.join(left_arc_weapon_names)}")
    print(f"Total Left Arc Weapon Mass: {ship.total_left_arc_mass}")
    print(f"Total Left Arc Weapon PV: {ship.total_left_arc_pv}")
    print(f"Total Left Arc Max Damage: {ship.total_left_arc_max_dmg}")

    print(f"\nTotal Mass: {ship.total_mass}")
    print(f"Total Mass Available: {ship.mass_delta}")
    print(f"Total Base PV: {ship.total_base_pv}")
    
    print(f"\nCrew Quality: {ship.crew_quality_str}")
    print(f"Max Stress: {ship.max_stress}")
    print(f"Final PV: {ship.final_pv}")

def show_ship_game_stats(ship: ShipClass) -> None:
    """Calcualte final mass and final base pv and print ship details"""
    ship.track_mass()
    ship.track_base_pv()
    
    print(f"\nSHIP NAME: {ship.name}\nClass: {ship.sclass.capitalize()}\nSize: {ship.size}\nArmor: {ship.armor_roll}")
    print(f"Base PV: {ship.total_base_pv}")
    print(f"Final PV: {ship.final_pv}")
    print(f"Crew Quality: {ship.crew_quality_str}")
    print(f"Max Stress: {ship.max_stress}")
    print(f"Critical Threshold: {ship.critical_threshold}")
    
    print(f"\nThrust Points: {ship.thrust_points}")
    print(f"Max Thrust: {ship.max_thrust}")
    
    oh_squares = ' □' * ship.outer_hull_mass
    print(f"\nOuter Hull Mass: {oh_squares} ({ship.outer_hull_mass})")
    ih_squares = ' □' * ship.inner_hull_mass
    print(f"Inner Hull Mass: {ih_squares} ({ship.inner_hull_mass})")

    print(f"\nEQUIPMENT: ")
    for item in ship.equipment_list:
        print(f"\n{item["name"]}")
        print(f"{item["description"]}")

    print(f"\nWEAPONS: ")
    print(f"\nFront Arc:")
    for weapon in ship.front_arc_weapon_list:
        print(f"\nName: {weapon["name"]}")
        print(f"Attack/Damage: {weapon["attack"]}/{weapon["damage"]}")
        print(f"Range: {weapon["range"]}")
        print(f"Special: {weapon["special"]}")
    
    print(f"\nRear Arc:")
    for weapon in ship.rear_arc_weapon_list:
        print(f"\nName: {weapon["name"]}")
        print(f"Attack/Damage: {weapon["attack"]}/{weapon["damage"]}")
        print(f"Range: {weapon["range"]}")
        print(f"Special: {weapon["special"]}")
    
    print(f"\nRight Arc:")
    for weapon in ship.right_arc_weapon_list:
        print(f"\nName: {weapon["name"]}")
        print(f"Attack/Damage: {weapon["attack"]}/{weapon["damage"]}")
        print(f"Range: {weapon["range"]}")
        print(f"Special: {weapon["special"]}")
    
    print(f"\nLeft Arc:")
    for weapon in ship.left_arc_weapon_list:
        print(f"\nName: {weapon["name"]}")
        print(f"Attack/Damage: {weapon["attack"]}/{weapon["damage"]}")
        print(f"Range: {weapon["range"]}")
        print(f"Special: {weapon["special"]}")

    print(f"\nCRITICAL HITS:")
    print("""
□ □ Engineering Hit
□ □ Major Weapon Damage (F/RT/LT/R)
□ Targeting Hit
□ □ □ □ Weapon Damage (F/RT/LT/R)
□ □ □ Crew Hit
□ □ Side Thruster Damage
□ □ □ □ □ Engine Room Damage
□ □ Engines Disabled
        """)

def export_ship_txt(ship: ShipClass):
    pass

def export_ship_json(ship: ShipClass):
    ship.build_json_objects()
    if input("\nExport ship to JSON? (Y/N): ").upper() == 'Y':
        filename = input("\nFile name: ")
        with open(filename + '.json', 'w', encoding='utf-8') as f:
            json.dump(ship.ship_json_object, f, ensure_ascii=False, indent=4)
    else:
        pass

def load_ship_base_json() -> ShipClass:
    if input("\nLoad ship from JSON? (Y/N): ").upper() == 'Y':
        file = input("\nFile name in local directory: ")
        with open(file, 'r', encoding='utf-8') as f:
            loaded_ship = json.load(f)
    else:
        pass
    return ShipClass(
                name = loaded_ship["name"], 
                sclass = loaded_ship["ship_class"], 
                size = loaded_ship["size"], 
                tam = loaded_ship["TAM"], 
                armor_roll = loaded_ship["armor_roll"], 
                mdpa = loaded_ship["MDPA"]), loaded_ship

def load_ship_details_json(ship: ShipClass, file: str) -> None:
        ship.crew_quality_str = file["crew_quality"]
        ship.total_base_pv = file["base_pv"]  
        ship.final_pv = file["final_pv"]
        ship.max_stress = file["max_stress"]   
        ship.outer_hull_mass = file["armor"]["outer_hull"]["mass"]  
        ship.outer_hull_pv = file["armor"]["outer_hull"]["pv"]  
        ship.inner_hull_mass = file["armor"]["inner_hull"]["mass"]  
        ship.inner_hull_pv = file["armor"]["inner_hull"]["pv"]  
        ship.critical_threshold = file["armor"]["critical_threshold"]  
        ship.thrust_points = file["propulsion"]["thrust_points"]
        ship.max_thrust = file["propulsion"]["max_thrust"]
        ship.propulsion_mass = file["propulsion"]["propulsion_mass"]
        ship.propulsion_pv = file["propulsion"]["propulsion_pv"]
        ship.equipment_list = file["equipment"]
        ship.front_arc_weapon_list = file["weapons"]["front_arc_weapons"]
        ship.rear_arc_weapon_list = file["weapons"]["rear_arc_weapons"]
        ship.right_arc_weapon_list = file["weapons"]["right_arc_weapons"]
        ship.left_arc_weapon_list = file["weapons"]["left_arc_weapons"]

def main_menu() -> None:
    run = True
    while run == True:
        command = input("\nCOMMAND (1-Build New Ship, 2-Import Ship, 3-Exit): ")
        match command:
            case "1": #build
                ship_instance = build_base_ship()
                build_menu(ship_instance)
            case "2": #import
                import_menu()
            case "3": #exit
                exit()
            case _: #match any other entry
                print(MENU_ERROR)

def build_menu(ship: ShipClass) -> None:
    run = True
    while run == True:
        command = input("\nCOMMAND (1-Armor, 2-Propulsion, 3-Equipment, 4-Weapons, 5-Crew Quality, 6-Check Mass, 7-View Build, 8-View Play, 9-Export, 10-Reset, 11-Main Menu): ")
        match command:
            case "1": #armor
                build_outer_hull(ship)
                build_inner_hull(ship)
            case "2": #propulsion
                build_propulsion(ship)
            case "3": #equipment
                build_equipment(ship)
            case "4": #weapons
                build_weapons(ship)
            case "5": #crew quality
                build_crew_quality(ship)
            case "6": #check mass
                mass_check_ui(ship)
            case "7": #view
                show_ship_build_stats(ship)
            case "8": #view
                show_ship_game_stats(ship)
            case "9": #export
                #export_ship_json(ship)
                export_menu(ship)
            case "10": #reset
                reset_stats(ship)
            case "11": #main menu
                main_menu()
            case _: #match any other entry
                print(MENU_ERROR)

def import_menu() -> None:
    run = True
    while run == True:
        command = input("\nCOMMAND (1-File, 2-View, 3-Edit, 4-Main Menu: ")
        match command:
            case "1": #file
                ship_instance, jsonf = load_ship_base_json()
                load_ship_details_json(ship_instance, jsonf)
            case "2": #view
                show_ship_build_stats(ship_instance)
            case "3": #edit
                build_menu(ship_instance)
            case "4": #main menu
                main_menu()
            case _: #match any other entry
                print(MENU_ERROR)

def export_menu(ship: ShipClass) -> None:
    run = True
    while run == True:
        command = input("\nCOMMAND (1-Play Card, 2-JSON, 3-Build Menu, 4-Main Menu ")
        match command:
            case "1": #play card
                export_ship_txt(ship)
            case "2": #json
                export_ship_json(ship)
            case "3": #edit
                build_menu(ship)
            case "4": #main menu
                main_menu()
            case _: #match any other entry
                print(MENU_ERROR)

if __name__ == "__main__":
    main_menu()