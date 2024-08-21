import build_data
from ShipClass import ShipClass
import json, jsonschema

MENU_ERROR = 'Invalid selection. Try again.'
SCHEMA_FILE = 'import_schema.json'

def build_base_ship() -> ShipClass:
    """Instantiate base ship from name and ship class inputs"""

    name = input("Ship Name: ")
    sclass = input(f"\nShip Class (see docs for list): ").upper()
    size = [s['size'] for s in build_data.sclass_details if s['sclass'] == sclass]
    tam = [s['tam'] for s in build_data.sclass_details if s['sclass'] == sclass]
    armor_roll = [s['armor_roll'] for s in build_data.sclass_details if s['sclass'] == sclass]
    mdpa = [s['mdpa'] for s in build_data.sclass_details if s['sclass'] == sclass]
    return ShipClass(name, sclass, size[0], tam[0], armor_roll[0], mdpa[0])

def rename_ship(ship: ShipClass) -> None:
    ship.name = input(f"\nCurrent name: {ship.name}. New name? ")

def build_outer_hull(ship: ShipClass) -> None:
    """Calculate outer hull outputs from strength input"""
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

def build_ship_build_stats(ship: ShipClass) -> None:
    """Calcualte final mass and final base pv and print ship details"""
    ship.track_mass()
    ship.track_base_pv()

    equipment_names = [i["name"] for i in ship.equipment_list]
    front_arc_weapon_names = [i["name"] for i in ship.front_arc_weapon_list]
    rear_arc_weapon_names = [i["name"] for i in ship.rear_arc_weapon_list]
    right_arc_weapon_names = [i["name"] for i in ship.right_arc_weapon_list]  
    left_arc_weapon_names = [i["name"] for i in ship.left_arc_weapon_list]

    build_stats = (
        f"\nSHIP NAME: {ship.name}"
        f"\nClass: {ship.sclass.capitalize()}    Size: {ship.size}    Armor: {ship.armor_roll}"
        f"\nCrew Quality: {ship.crew_quality_str}    Max Stress: {ship.max_stress}"
        f"\nTotal Availble Mass: {ship.tam}    Current Total Mass: {ship.total_mass}    Mass Available: {ship.mass_delta}"
        f"\nTotal Base PV: {ship.total_base_pv}    Final PV: {ship.final_pv}"
        f"\nMax Damage Per Arc: {ship.mdpa}    Critical Threshold: {ship.critical_threshold}"
        f"\n\nThrust Points: {ship.thrust_points}    Max Thrust: {ship.max_thrust}"
        f"\nPropulsion Mass: {ship.propulsion_mass}    Propulsion PV: {ship.propulsion_pv}"
        f"\n\nOuter Hull Mass: {ship.outer_hull_mass}    Outer Hull PV: {ship.outer_hull_pv}"
        f"\nInner Hull Mass: {ship.inner_hull_mass}    Inner Hull PV: {ship.inner_hull_pv}"
        f"\n\nEQUIPMENT"
        f"\nTotal Equipment Mass: {ship.total_equipment_mass}    Total Equipment PV: {ship.total_equipment_pv}"
        f"\nSelected Equipment: {', '.join(equipment_names)}"
        f"\n\nWEAPONS"
        f"\n\nTotal Front Arc Weapon Mass: {ship.total_front_arc_mass}    Total Front Arc Weapon PV: {ship.total_front_arc_pv}"
        f"\nTotal Front Arc Max Damage: {ship.total_front_arc_max_dmg}"
        f"\nFront Arc Weapons: {', '.join(front_arc_weapon_names)}"
        f"\n\nTotal Rear Arc Weapon Mass: {ship.total_rear_arc_mass}    Total Rear Arc Weapon PV: {ship.total_rear_arc_pv}"
        f"\nTotal Rear Arc Max Damage: {ship.total_rear_arc_max_dmg}"
        f"\nRear Arc Weapons: {', '.join(rear_arc_weapon_names)}"
        f"\n\nTotal Right Arc Weapon Mass: {ship.total_right_arc_mass}    Total Right Arc Weapon PV: {ship.total_right_arc_pv}"
        f"\nTotal Right Arc Max Damage: {ship.total_right_arc_max_dmg}"
        f"\nRight Arc Weapons: {', '.join(right_arc_weapon_names)}"
        f"\n\nTotal Left Arc Weapon Mass: {ship.total_left_arc_mass}    Total Left Arc Weapon PV: {ship.total_left_arc_pv}"
        f"\nTotal Left Arc Max Damage: {ship.total_left_arc_max_dmg}"
        f"\nLeft Arc Weapons: {', '.join(left_arc_weapon_names)}"
    )

    return build_stats

def build_ship_game_stats(ship: ShipClass) -> str:
    """Calcualte final mass and final base pv and print ship details"""
    ship.track_mass()
    ship.track_base_pv()

    #create a box symbol per mass point
    oh_squares = ' □' * ship.outer_hull_mass 
    ih_squares = ' □' * ship.inner_hull_mass

    game_card = (f"\nSHIP NAME: {ship.name}"
                f"\nClass: {ship.sclass.capitalize()}    Size: {ship.size}    Armor: {ship.armor_roll}"
                f"\nBase PV: {ship.total_base_pv}    Final PV: {ship.final_pv}    Crew Quality: {ship.crew_quality_str}"
                f"\nMax Stress: {ship.max_stress}    Critical Threshold: {ship.critical_threshold}"
                f"\nThrust Points: {ship.thrust_points}    Max Thrust: {ship.max_thrust}"
                f"\n\nARMOR:"
                f"\nOuter Hull Mass: {oh_squares} ({ship.outer_hull_mass})"
                f"\nInner Hull Mass: {ih_squares} ({ship.inner_hull_mass})"
                f"\n\nEQUIPMENT:"
                f"\n{''.join(f'{item['name']} -- {item['description']}\n' for item in ship.equipment_list)}"
                f"\nWEAPONS:"
                f"\n***Front Arc***"
                f"\n{''.join(f'Name: {weapon["name"]}\nAttack/Damage: {weapon["attack"]}/{weapon["damage"]}\nRange: {weapon["range"]}\nSpecial: {weapon["special"]}\n\n' for weapon in ship.front_arc_weapon_list)}"
                f"\n***Rear Arc***"
                f"\n{''.join(f'Name: {weapon["name"]}\nAttack/Damage: {weapon["attack"]}/{weapon["damage"]}\nRange: {weapon["range"]}\nSpecial: {weapon["special"]}\n\n' for weapon in ship.rear_arc_weapon_list)}"
                f"\n***Right Arc***"
                f"\n{''.join(f'Name: {weapon["name"]}\nAttack/Damage: {weapon["attack"]}/{weapon["damage"]}\nRange: {weapon["range"]}\nSpecial: {weapon["special"]}\n\n' for weapon in ship.right_arc_weapon_list)}"
                f"\n***Left Arc***"
                f"\n{''.join(f'Name: {weapon["name"]}\nAttack/Damage: {weapon["attack"]}/{weapon["damage"]}\nRange: {weapon["range"]}\nSpecial: {weapon["special"]}\n\n' for weapon in ship.left_arc_weapon_list)}"
                f"\nCRITICAL HITS:"
                f"\n□ □ Engineering Hit    □ □ Major Weapon Damage (F/RT/LT/R)"
                f"\n□ Targeting Hit    □ □ □ □ Weapon Damage (F/RT/LT/R)"
                f"\n□ □ □ Crew Hit    □ □ Side Thruster Damage"
                f"\n□ □ □ □ □ Engine Room Damage    □ □ Engines Disabled"
                )
    return game_card

def export_ship_txt(ship: ShipClass):
    game_card = build_ship_game_stats(ship)
    if input("\nExport ship to txt file? (Y/N): ").upper() == 'Y':
        with open(ship.name + '_export' + '.txt', 'w', encoding='utf-8') as f:
            f.write(game_card)
    else:
        pass    

def export_ship_json(ship: ShipClass):
    ship.build_json_objects()
    if input("\nExport ship to JSON? (Y/N): ").upper() == 'Y':
        with open(ship.name + '_export' + '.json', 'w', encoding='utf-8') as f:
            json.dump(ship.ship_json_object, f, ensure_ascii=False, indent=4)
    else:
        pass

def import_ship_json_file() -> None:
    if input("\nImport ship from JSON? (Y/N): ").upper() == 'Y':
        while True:
            file = input("\nFull file name in local directory: ")
            try:
                with open(file, 'r', encoding='utf-8') as f:
                    loaded_ship_json = json.load(f)
            except FileNotFoundError:
                if input("File not found. Try again... Y/N? ").upper() == 'N':
                    break
            except json.decoder.JSONDecodeError:
                if input("Invalid JSON. Try again... Y/N? ").upper() == 'N':
                    break
            else:
                error_list = validate_json(loaded_ship_json)
                if error_list == []:
                    print('Ship imported successfully!')
                    ship_instance = load_ship_details_json(loaded_ship_json)
                    import_submenu(ship_instance)
                else: 
                    print(f"\nIMPORT ERRORS:")
                    for error in error_list:
                        print(f"{error.message}")
                    if input(f"\nTry again... Y/N? ").upper() == 'N':
                        break
    else:
        pass

def validate_json(ship_json: str) -> list:
    with open(SCHEMA_FILE, 'r', encoding='utf-8') as schema_file:
        schema = json.load(schema_file)
    validator = jsonschema.Draft7Validator(schema)
    error_list = list(validator.iter_errors(ship_json))  #get individual validation errors
    return error_list

def load_ship_details_json(ship_json: str) -> ShipClass:
        #initialize instance
        ship = ShipClass(
                name = ship_json["name"], 
                sclass = ship_json["ship_class"], 
                size = ship_json["size"], 
                tam = ship_json["TAM"], 
                armor_roll = ship_json["armor_roll"], 
                mdpa = ship_json["MDPA"]
            )
        
        #parse details
        ship.crew_quality_str = ship_json["crew_quality"]
        ship.total_base_pv = ship_json["base_pv"]  
        ship.final_pv = ship_json["final_pv"]
        ship.max_stress = ship_json["max_stress"]   
        ship.outer_hull_mass = ship_json["armor"]["outer_hull"]["mass"]  
        ship.outer_hull_pv = ship_json["armor"]["outer_hull"]["pv"]  
        ship.inner_hull_mass = ship_json["armor"]["inner_hull"]["mass"]  
        ship.inner_hull_pv = ship_json["armor"]["inner_hull"]["pv"]  
        ship.critical_threshold = ship_json["armor"]["critical_threshold"]  
        ship.thrust_points = ship_json["propulsion"]["thrust_points"]
        ship.max_thrust = ship_json["propulsion"]["max_thrust"]
        ship.propulsion_mass = ship_json["propulsion"]["propulsion_mass"]
        ship.propulsion_pv = ship_json["propulsion"]["propulsion_pv"]
        ship.equipment_list = ship_json["equipment"]["equipment_items"]
        ship.total_equipment_mass = ship_json["equipment"]["total_equipment_mass"]
        ship.total_equipment_pv = ship_json["equipment"]["total_equipment_pv"]
        ship.front_arc_weapon_list = ship_json["weapons"]["front_arc_weapons"]
        ship.total_front_arc_mass = ship_json["weapons"]["total_front_arc_mass"]
        ship.total_front_arc_pv = ship_json["weapons"]["total_front_arc_pv"]
        ship.total_front_arc_max_dmg = ship_json["weapons"]["total_front_arc_max_dmg"]
        ship.rear_arc_weapon_list = ship_json["weapons"]["rear_arc_weapons"]
        ship.total_rear_arc_mass = ship_json["weapons"]["total_rear_arc_mass"]
        ship.total_rear_arc_pv = ship_json["weapons"]["total_rear_arc_pv"]
        ship.total_rear_arc_max_dmg = ship_json["weapons"]["total_rear_arc_max_dmg"]
        ship.right_arc_weapon_list = ship_json["weapons"]["right_arc_weapons"]
        ship.total_right_arc_mass = ship_json["weapons"]["total_right_arc_mass"]
        ship.total_right_arc_pv = ship_json["weapons"]["total_right_arc_pv"]
        ship.total_right_arc_max_dmg = ship_json["weapons"]["total_right_arc_max_dmg"]
        ship.left_arc_weapon_list = ship_json["weapons"]["left_arc_weapons"]
        ship.total_left_arc_mass = ship_json["weapons"]["total_left_arc_mass"]
        ship.total_left_arc_pv = ship_json["weapons"]["total_left_arc_pv"]
        ship.total_left_arc_max_dmg = ship_json["weapons"]["total_left_arc_max_dmg"]

        return ship

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
        command = input("\nCOMMAND (1-Armor, 2-Propulsion, 3-Equipment, 4-Weapons, 5-Crew Quality, 6-Check Mass, 7-View Build, 8-View Game Card, 9-Export, 10-Rename, 11-Reset, 12-Main Menu): ")
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
                print(build_ship_build_stats(ship))
            case "8": #view
                print(build_ship_game_stats(ship))
            case "9": #export
                export_menu(ship)
            case "10": #rename
                rename_ship(ship)
            case "11": #reset
                reset_stats(ship)
            case "12": #main menu
                main_menu()
            case _: #match any other entry
                print(MENU_ERROR)

def import_menu() -> None:
    run = True
    while run == True:
        command = input("\nCOMMAND (1-Import from JSON, 2-Main Menu: ")
        match command:
            case "1": #file
                import_ship_json_file()
            case "2": #main menu
                main_menu()
            case _: #match any other entry
                print(MENU_ERROR)

def import_submenu(ship: ShipClass) -> None:
    run = True
    while run == True:
        command = input("\nCOMMAND (1-View Build, 2-View Game Stats, 3-Edit, 4-Import New, 5-Main Menu: ")
        match command:
            case "1": #view
                print(build_ship_build_stats(ship))
            case "2": #view
                print(build_ship_game_stats(ship))
            case "3": #edit
                build_menu(ship)
            case "4": #import menu
                import_menu()
            case "5": #main menu
                main_menu()
            case _: #match any other entry
                print(MENU_ERROR)

def export_menu(ship: ShipClass) -> None:
    run = True
    while run == True:
        command = input("\nCOMMAND 1-Game Card (Txt), 2-Save ship (JSON), 3-Back (Build Menu), 4-Main Menu ")
        match command:
            case "1": #export txt
                export_ship_txt(ship)
            case "2": #export json
                export_ship_json(ship)
            case "3": #build menu
                build_menu(ship)
            case "4": #main menu
                main_menu()
            case _: #match any other entry
                print(MENU_ERROR)

if __name__ == "__main__":
    main_menu()