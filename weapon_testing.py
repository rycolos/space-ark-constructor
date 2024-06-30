import build_data

def front_weapons(*weapons):
    front_arc_weapons = ""
    front_arc_mass = []
    front_arc_pv = []
    front_arc_max_dmg = []

    if weapons[0] == '': #check for empty list
        front_arc_weapons = "None"
        total_front_arc_mass = 0
        total_front_arc_pv = 0
        total_front_arc_max_dmg = 0
    else:
        for weapon in weapons:
            weapon_mass = [w["mass"] for w in build_data.weapon_details if w["name"] == weapon]
            front_arc_mass.append(weapon_mass[0])
            
            weapon_pv = [w["pv"] for w in build_data.weapon_details if w["name"] == weapon]
            front_arc_pv.append(weapon_pv[0])
            
            weapon_max_dmg = [w["max_dmg"] for w in build_data.weapon_details if w["name"] == weapon]
            front_arc_max_dmg.append(weapon_max_dmg[0])
        total_front_arc_mass = sum(front_arc_mass)
        total_front_arc_pv = sum(front_arc_pv)
        total_front_arc_max_dmg = sum(front_arc_max_dmg)
        front_arc_weapons = ', '.join(weapons)
    return front_arc_weapons, total_front_arc_mass, total_front_arc_pv, total_front_arc_max_dmg

#UI
weapon_selection = True
while weapon_selection == True:
    arc = input(f"\nSelect arc (1-Front, 2-Rear, 3-Right, 4-Left) or E to exit: ")
    match arc:
        case "1":
            front_list = list(map(str, input("\nSelect Front Arc weapons as comma-separated names. Leave empty for None: ").split(', ')))
            front_arc_weapons, total_front_arc_mass, total_front_arc_pv, total_front_arc_max_dmg = front_weapons(*front_list)
            print(f"\nFront Arc Weapons: {front_arc_weapons}")
            print(f"Total Front Arc Mass: {total_front_arc_mass}")
            print(f"Total Front Arc PV: {total_front_arc_pv}")
            print(f"Total Front Arc Max Damage: {total_front_arc_max_dmg}")
        case "2":
            rear_list = list(map(str, input("Select Rear Arc weapons as comma-separated names: ").split(', ')))
            #rear_weapons(*rear_list)
        case "3":
            right_list = list(map(str, input("Select Right Arc weapons as comma-separated names: ").split(', ')))
            #right_weapons(*right_list)
        case "4":
            left_list = list(map(str, input("Select Left Arc weapons as comma-separated names: ").split(', ')))
            #left_weapons(*left_list)
        case "E":
            weapon_selection = False
#add mass check
#add max dmg check