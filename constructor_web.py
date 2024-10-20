import streamlit as st
import build_data
from ShipClass import ShipClass
import json, jsonschema, os
from datetime import datetime
from html2image import Html2Image

SCHEMA_FILE = 'import_schema.json'

def build_base_ship(name, sclass) -> ShipClass:
    """
    Instantiate base ship from name and ship class inputs
    """
    size = [s['size'] for s in build_data.sclass_details if s['sclass'] == sclass]
    tam = [s['tam'] for s in build_data.sclass_details if s['sclass'] == sclass]
    armor_roll = [s['armor_roll'] for s in build_data.sclass_details if s['sclass'] == sclass]
    mdpa = [s['mdpa'] for s in build_data.sclass_details if s['sclass'] == sclass]
    return ShipClass(name, sclass, size[0], tam[0], armor_roll[0], mdpa[0])

def configure_page() -> None:
    """
    Apply basic page configuration
    """ 
    title = 'Space Ark Constructor'
    st.set_page_config(page_title=title, page_icon=':ringed_planet:', layout='wide')
    st.title(title)
    construct_ship, import_ship = st.tabs(["Construct Ship", "Import Ship"])
    return construct_ship, import_ship

# def front_weapon_stat(weap_key):
#     """
#     Display weapon stat for live view
#     """ 
#     if weap_key != []:
#         front_weapon_stat = ('/n'.join(f'{weapon["name"]} -- A/D: {weapon["attack"]}/{weapon["damage"]} -- R: {weapon["range"]} -- S: {weapon["special"]}' for weapon in build_data.weapon_details if weapon['name'] == weap_key[-1]))
#         build_col3.info(front_weapon_stat, icon=":material/info:")

# def rear_weapon_stat(weap_key):   
#     """
#     Display weapon stat for live view
#     """          
#     if weap_key != []:
#         rear_weapon_stat = ('/n'.join(f'{weapon["name"]} -- A/D: {weapon["attack"]}/{weapon["damage"]} -- R: {weapon["range"]} -- S: {weapon["special"]}' for weapon in build_data.weapon_details if weapon['name'] == weap_key[-1]))
#         build_col3.info(rear_weapon_stat, icon=":material/info:")

# def right_weapon_stat(weap_key):
#     """
#     Display weapon stat for live view
#     """ 
#     if weap_key != []:
#         right_weapon_stat = ('/n'.join(f'{weapon["name"]} -- A/D: {weapon["attack"]}/{weapon["damage"]} -- R: {weapon["range"]} -- S: {weapon["special"]}' for weapon in build_data.weapon_details if weapon['name'] == weap_key[-1]))
#         build_col3.info(right_weapon_stat, icon=":material/info:")

# def left_weapon_stat(weap_key): 
#     """
#     Display weapon stat for live view
#     """           
#     if weap_key != []:
#         left_weapon_stat = ('/n'.join(f'{weapon["name"]} -- A/D: {weapon["attack"]}/{weapon["damage"]} -- R: {weapon["range"]} -- S: {weapon["special"]}' for weapon in build_data.weapon_details if weapon['name'] == weap_key[-1]))
#         build_col3.info(left_weapon_stat, icon=":material/info:")

# def equipment_stat(equip_key):
#     """
#     Display equipment stat for live view
#     """
#     if equip_key != []:
#         equipment_stat = (f'{[s['description'] for s in build_data.equipment_details if s['name'] == equip_key[-1]][0]}')
#         build_col3.info(equipment_stat, icon=":material/info:")

def validate_json(ship_json: str) -> list:
    """
    Validate ship is valid JSON and validate against schema template
    """
    with open(SCHEMA_FILE, 'r', encoding='utf-8') as schema_file:
        schema = json.load(schema_file)
    validator = jsonschema.Draft7Validator(schema)
    error_list = list(validator.iter_errors(ship_json))  #get individual validation errors
    return error_list

def load_ship_details_json(ship_json: str) -> ShipClass:
    """
    Parse ship details from JSON file
    """
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
    ship.outer_hull_strength_str = ship_json["armor"]["outer_hull"]["strength"]  
    ship.outer_hull_mass = ship_json["armor"]["outer_hull"]["mass"]  
    ship.outer_hull_pv = ship_json["armor"]["outer_hull"]["pv"]  
    ship.inner_hull_strength_str = ship_json["armor"]["inner_hull"]["strength"]  
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

def ship_core(st_element, name_key, sclass_key, name_loaded_value, sclass_loaded_value):
    with st_element.expander(label='**Ship Core**', expanded=True):
        name = st.text_input(label="Ship Name", value=name_loaded_value)
        sclass = st.selectbox(label='Ship Class', key=sclass_key, index=sclass_loaded_value, options=[s['sclass'] for s in build_data.sclass_details])
        if sclass:
            constructed_ship_local = build_base_ship(name, sclass)
            st.session_state.constructed_ship_state = constructed_ship_local
    return constructed_ship_local

def armor(st_element, ohs_key, ihs_key, ohs_loaded_value, ihs_loaded_value, st_ship, local_ship):
    with st_element.expander('**Armor**', expanded=True):
        ohs_input = st.selectbox(label='Outer Hull Strength', key=ohs_key, index=ohs_loaded_value, options=[s['name'] for s in build_data.outer_strength_details])
        if ohs_input:
            ohs_int = [s['id'] for s in build_data.outer_strength_details if s['name'] == ohs_input]
            local_ship.outer_hull(ohs_int[0])
            local_ship.track_mass()
            local_ship.track_base_pv()
            st_ship = local_ship

        ihs_input = st.selectbox(label='Inner Hull Strength', key=ihs_key, index=ihs_loaded_value, options=[s['name'] for s in build_data.inner_strength_details])
        if ihs_input:
            ihs_int = [s['id'] for s in build_data.inner_strength_details if s['name'] == ihs_input]
            local_ship.inner_hull(ihs_int[0])
            local_ship.track_mass()
            local_ship.track_base_pv()
            st_ship = local_ship

def propulsion(st_element, tp_key, tp_loaded_value, st_ship, local_ship):
    with st_element.expander(label='**Propulsion**', expanded=True):
        tp_input = st.number_input(label='Thrust Points', key=tp_key, value=tp_loaded_value, min_value=0)
        if tp_input:
            local_ship.propulsion(tp_input)
            local_ship.track_mass()
            local_ship.track_base_pv()
            st_ship = local_ship

def crew_quality(st_element, cq_key, cq_loaded_value, st_ship, local_ship):
    with st_element.expander(label='**Crew Quality**', expanded=True):
        crew_quality_input = st.selectbox(label='Crew Quality', key=cq_key, index=cq_loaded_value, options=[s['name'] for s in build_data.crew_quality_details])
        if crew_quality_input:
            crew_quality_int = [s['id'] for s in build_data.crew_quality_details if s['name'] == crew_quality_input]
            local_ship.set_quality(crew_quality_int[0])
            st_ship = local_ship

def equipment(st_element, equip_key, equip_loaded_value, st_ship, local_ship):
    with st_element.expander(label='**Equipment**', expanded=True):
        equipment_input = st.multiselect(label='Equipment', key=equip_key, default=equip_loaded_value, options=[s['name'] for s in build_data.equipment_details])
        if equipment_input:            
            equipment_name_to_id = {item["name"]: item["id"] for item in build_data.equipment_details}
            equip_int_list = [equipment_name_to_id[name] for name in equipment_input]
            local_ship.equipment(*equip_int_list)
            st.markdown(f'**Total Equipment Mass:** {local_ship.total_equipment_mass}, **Total Equipment PV:** {local_ship.total_equipment_pv}')
            local_ship.track_mass()
            local_ship.track_base_pv()
            st_ship = local_ship

def weapons(st_element, weap_key, weap_loaded_value, st_ship, local_ship):
    with st_element.expander(label='**Weapons**', expanded=True):
        front_arc_input = st.multiselect(label='Front Arc Weapons', key=weap_key+'-front-arc', default=weap_loaded_value[0], options=[s['name'] for s in build_data.weapon_details for i in range(4)])
        if front_arc_input:  
            local_ship.front_arc_weapons(*front_arc_input)
            st.markdown(f'**Arc Mass:** {local_ship.total_front_arc_mass} — **Arc PV:** {local_ship.total_front_arc_pv} — **Arc Damage:** {local_ship.total_front_arc_max_dmg}')
            local_ship.track_mass()
            local_ship.track_base_pv()
            st_ship = local_ship

        rear_arc_input = st.multiselect(label='Rear Arc Weapons', key=weap_key+'-rear-arc', default=weap_loaded_value[1], options=[s['name'] for s in build_data.weapon_details for i in range(4)])
        if rear_arc_input:
            local_ship.rear_arc_weapons(*rear_arc_input)
            st.markdown(f'**Arc Mass:** {local_ship.total_rear_arc_mass} — **Arc PV:** {local_ship.total_rear_arc_pv} — **Arc Damage:** {local_ship.total_rear_arc_max_dmg}')
            local_ship.track_mass()
            local_ship.track_base_pv()
            st_ship = local_ship

        right_arc_input = st.multiselect(label='Right Arc Weapons', key=weap_key+'-right-arc', default=weap_loaded_value[2], options=[s['name'] for s in build_data.weapon_details for i in range(4)])
        if right_arc_input:
            local_ship.right_arc_weapons(*right_arc_input)
            st.markdown(f'**Arc Mass:** {local_ship.total_right_arc_mass} — **Arc PV:** {local_ship.total_right_arc_pv} — **Arc Damage:** {local_ship.total_right_arc_max_dmg}')
            local_ship.track_mass()
            local_ship.track_base_pv()
            st_ship = local_ship

        left_arc_input = st.multiselect(label='Left Arc Weapons', key=weap_key+'-left-arc', default=weap_loaded_value[3], options=[s['name'] for s in build_data.weapon_details for i in range(4)])
        if left_arc_input:
            local_ship.left_arc_weapons(*left_arc_input)
            st.markdown(f'**Arc Mass:** {local_ship.total_left_arc_mass} — **Arc PV:** {local_ship.total_left_arc_pv} — **Arc Damage:** {local_ship.total_left_arc_max_dmg}')
            local_ship.track_mass()
            local_ship.track_base_pv()
            st_ship = local_ship

def build_game_cards(local_ship):
    oh_squares = ' □' * local_ship.outer_hull_mass 
    ih_squares = ' □' * local_ship.inner_hull_mass

    game_card_html = f"""
            <table>
                <tr>
                    <td><b>SHIP NAME</b></td>
                    <td>{local_ship.name}</td>
                    <td><b>CLASS</b></td>
                    <td>{local_ship.sclass}</td>
                    <td><b>SIZE</b></td>
                    <td>{local_ship.size}</td>
                </tr>
                <tr>
                    <td><b>ARMOR</b></td>
                    <td>{local_ship.armor_roll}</td>
                    <td><b>BASE PV</b></td>
                    <td>{local_ship.total_base_pv}</td>
                    <td><b>FINAL PV</b></td>
                    <td>{local_ship.final_pv}</td>
                </tr>
                <tr>
                    <td><b>CREW QUALITY</b></td>
                    <td>{local_ship.crew_quality_str}</td>
                    <td><b>MAX STRESS</b></td>
                    <td>{local_ship.max_stress}</td>
                    <td><b>CRITICAL THRESHOLD</b></td>
                    <td>{local_ship.critical_threshold}</td>
                </tr>
                <tr>
                    <td><b>THRUST POINTS</b></td>
                    <td>{local_ship.thrust_points}</td>
                    <td><b>MAX THRUST</b></td>
                    <td>{local_ship.max_thrust}</td>
                    <td></td>
                    <td></td>
                </tr>
                <tr>
                    <td colspan="6"><b>ARMOR</b></td>
                </tr>
                <tr>
                    <td>Outer Hull ({local_ship.outer_hull_mass})</td>
                    <td colspan="5">{oh_squares}</td>
                </tr>
                <tr>
                    <td>Inner Hull ({local_ship.inner_hull_mass})</td>
                    <td colspan="5">{ih_squares}</td>
                </tr>
                <tr>
                    <td colspan="6"><b>EQUIPMENT</b></td>
                </tr>
                <tr>
                    <td colspan="6">{''.join(f'{item['name']}<br>' for item in local_ship.equipment_list)}</td>
                </tr>
                <tr>
                    <td colspan="6"><b>WEAPONS</b></td>
                </tr>
                <tr>
                    <td colspan="6"><b>Front Arc</b></td>
                </tr>
                <tr>
                    <td colspan="6">{''.join(f'{weapon["name"]} -- A/D: {weapon["attack"]}/{weapon["damage"]} -- R: {weapon["range"]} -- S: {weapon["special"]}<br>' for weapon in local_ship.front_arc_weapon_list)}</td>
                </tr>
                <tr>
                    <td colspan="6"><b>Rear Arc</b></td>
                </tr>
                <tr>
                    <td colspan="6">{''.join(f'{weapon["name"]} -- A/D: {weapon["attack"]}/{weapon["damage"]} -- R: {weapon["range"]} -- S: {weapon["special"]}<br>' for weapon in local_ship.rear_arc_weapon_list)}</td>
                </tr>
                <tr>
                    <td colspan="6"><b>Right Arc</b></td>
                </tr>
                <tr>
                    <td colspan="6">{''.join(f'{weapon["name"]} -- A/D: {weapon["attack"]}/{weapon["damage"]} -- R: {weapon["range"]} -- S: {weapon["special"]}<br>' for weapon in local_ship.right_arc_weapon_list)}</td>
                </tr>
                <tr>
                    <td colspan="6"><b>Left Arc</b></td>
                </tr>
                <tr>
                    <td colspan="6">{''.join(f'{weapon["name"]} -- A/D: {weapon["attack"]}/{weapon["damage"]} -- R: {weapon["range"]} -- S: {weapon["special"]}<br>' for weapon in local_ship.left_arc_weapon_list)}</td>
                </tr>
                <tr>
                    <td colspan="6"><b>CRITICAL HITS</b></td>
                </tr>
                <tr rowspan="4">
                    <td colspan="3">
                        □ □ Engineering Hit
                        <br>□ Targeting Hit
                        <br>□ □ □ Crew Hit
                        <br>□ □ □ □ □ Engine Room Damage
                    </td>
                    <td colspan="3">
                        □ □ Major Weapon Damage ( F / RT / LT / R )
                        <br>□ □ □ □ Weapon Damage ( F / RT / LT / R )
                        <br>□ □ Side Thruster Damage
                        <br>□ □ Engines Disabled
                    </td>
                </tr>
            </table>
            """

    game_card_txt = (f"\nSHIP NAME: {local_ship.name}"
                    f"\nClass: {local_ship.sclass.capitalize()}    Size: {local_ship.size}    Armor: {local_ship.armor_roll}"
                    f"\nBase PV: {local_ship.total_base_pv}    Final PV: {local_ship.final_pv}    Crew Quality: {local_ship.crew_quality_str}"
                    f"\nMax Stress: {local_ship.max_stress}    Critical Threshold: {local_ship.critical_threshold}"
                    f"\nThrust Points: {local_ship.thrust_points}    Max Thrust: {local_ship.max_thrust}"
                    f"\n\nARMOR:"
                    f"\nOuter Hull Mass: {oh_squares} ({local_ship.outer_hull_mass})"
                    f"\nInner Hull Mass: {ih_squares} ({local_ship.inner_hull_mass})"
                    f"\n\nEQUIPMENT:"
                    f"\n{''.join(f'{item['name']} -- {item['description']}\n' for item in local_ship.equipment_list)}"
                    f"\nWEAPONS:"
                    f"\n***Front Arc***"
                    f"\n{''.join(f'Name: {weapon["name"]}\nAttack/Damage: {weapon["attack"]}/{weapon["damage"]}\nRange: {weapon["range"]}\nSpecial: {weapon["special"]}\n\n' for weapon in local_ship.front_arc_weapon_list)}"
                    f"\n***Rear Arc***"
                    f"\n{''.join(f'Name: {weapon["name"]}\nAttack/Damage: {weapon["attack"]}/{weapon["damage"]}\nRange: {weapon["range"]}\nSpecial: {weapon["special"]}\n\n' for weapon in local_ship.rear_arc_weapon_list)}"
                    f"\n***Right Arc***"
                    f"\n{''.join(f'Name: {weapon["name"]}\nAttack/Damage: {weapon["attack"]}/{weapon["damage"]}\nRange: {weapon["range"]}\nSpecial: {weapon["special"]}\n\n' for weapon in local_ship.right_arc_weapon_list)}"
                    f"\n***Left Arc***"
                    f"\n{''.join(f'Name: {weapon["name"]}\nAttack/Damage: {weapon["attack"]}/{weapon["damage"]}\nRange: {weapon["range"]}\nSpecial: {weapon["special"]}\n\n' for weapon in local_ship.left_arc_weapon_list)}"
                    f"\nCRITICAL HITS:"
                    f"\n□ □ Engineering Hit    □ □ Major Weapon Damage (F/RT/LT/R)"
                    f"\n□ Targeting Hit    □ □ □ □ Weapon Damage (F/RT/LT/R)"
                    f"\n□ □ □ Crew Hit    □ □ Side Thruster Damage"
                    f"\n□ □ □ □ □ Engine Room Damage    □ □ Engines Disabled"
                    )

    return game_card_html, game_card_txt

def init_session():
    if 'constructed_ship_state' not in st.session_state:
        st.session_state.constructed_ship_state = ShipClass
    if 'imported_ship_state' not in st.session_state:
        st.session_state.imported_ship_state = ShipClass
    if 'imported_ship_edit_state' not in st.session_state:
        st.session_state.imported_ship_edit_state = ShipClass

def error_tam_exceeded(st_element, local_ship):
    if local_ship.tam_exceeded:
        st_element.info(f'Mass overage of {abs(local_ship.mass_delta)}!', icon=":material/warning:")

def error_mdpa_exceeded(st_element, local_ship):
    arc_names = ['front', 'rear', 'right', 'left']
    for arc in arc_names:
        total_dmg = getattr(local_ship, f'total_{arc}_arc_max_dmg')
        if total_dmg > local_ship.mdpa:
            st_element.info(f'{arc.capitalize()} arc damage overage of {abs(local_ship.mdpa - total_dmg)}!', icon=":material/warning:")

if __name__ == "__main__":
    construct_ship, import_ship = configure_page()
    init_session()
    
    with construct_ship:
        build_col1, build_col2, build_col3 = st.columns(3)
        construct_metric_col1, construct_metric_col2 = build_col3.columns(2)

        #Build Fields
        constructed_ship_local = ship_core(st_element=build_col1, name_key='construct-name', 
            sclass_key='construct-sclass', name_loaded_value=None, sclass_loaded_value=0)

        armor(st_element=build_col1, ohs_key='construct-ohs', ihs_key='construct-ihs', ohs_loaded_value=None, 
            ihs_loaded_value=None, st_ship=st.session_state.constructed_ship_state, local_ship=constructed_ship_local)
        
        propulsion(st_element=build_col1, tp_key='construct-tp', tp_loaded_value=0,
            st_ship=st.session_state.constructed_ship_state, local_ship=constructed_ship_local)
        
        weapons(st_element=build_col2, weap_key='construct-weap', weap_loaded_value=[None, None, None, None], 
            st_ship=st.session_state.constructed_ship_state, local_ship=constructed_ship_local)
        
        equipment(st_element=build_col2, equip_key='construct-equip', equip_loaded_value=None, 
            st_ship=st.session_state.constructed_ship_state, local_ship=constructed_ship_local)
        
        crew_quality(st_element=build_col3, cq_key='construct-cq', cq_loaded_value=None,
            st_ship=st.session_state.constructed_ship_state, local_ship=constructed_ship_local)

        #real-time metrics, errors, calculated stats
        constructed_ship_local.track_base_pv()
        constructed_ship_local.track_mass()

        error_tam_exceeded(st_element=build_col3, local_ship=constructed_ship_local)

        error_mdpa_exceeded(st_element=build_col3, local_ship=constructed_ship_local)

        construct_metric_col1.metric(label='Current Mass', value=constructed_ship_local.total_mass)
        construct_metric_col1.metric(label='Mass Remaining', value=constructed_ship_local.mass_delta)
        construct_metric_col2.metric(label='Base PV', value=constructed_ship_local.total_base_pv)
        construct_metric_col2.metric(label='Final PV', value=constructed_ship_local.final_pv)

        build_col3.write(f"""
                    ### Calculated Stats: 
                    **Ship Size:** {constructed_ship_local.size}  
                    **Total Available Mass:** {constructed_ship_local.tam}  
                    **Max Damage Per Arc:** {constructed_ship_local.mdpa}  
                    **Armor Roll:** {constructed_ship_local.armor_roll}  
                    **Critical Threshold:** {constructed_ship_local.critical_threshold}  
                    **Max Thrust:** {constructed_ship_local.max_thrust}  
                    **Max Stress:** {constructed_ship_local.max_stress}  
                    """)

        #ship cards, export functions
        st.header("Ship Card")
        game_card_html, game_card_txt = build_game_cards(constructed_ship_local)
        st.markdown(game_card_html, unsafe_allow_html=True)
        
        #download ship image
        img_path_server = "tmp_images/"
        hti = Html2Image(output_path=img_path_server)
        hti.browser.flags = ['--default-background-color=ffffff', '--hide-scrollbars']
        img_download_fname = f"{constructed_ship_local.name}_image_{datetime.today().strftime('%Y%m%d')}.png"

        ship_image = st.button('Create Ship Card Image')
        if ship_image:
            hti.screenshot(html_str=game_card_html, save_as=img_download_fname, size=(400, 450), css_str=['body {font-family: verdana;}', 'table {font-size: 5px;}'])

            with open(img_path_server + img_download_fname, "rb") as file:
                btn = st.download_button(
                    label="Download Ship Card Image",
                    data=file,
                    file_name=img_download_fname,
                    mime="image/png",
                )
            os.remove(img_path_server + img_download_fname)

        #download ship txt
        txt_download_fname = f"{constructed_ship_local.name}_txt_{datetime.today().strftime('%Y%m%d')}"
        st.download_button(
            label="Download Ship Card (Text Only)",
            data=game_card_txt,
            file_name=txt_download_fname,
            mime="text/plain",
        )

        #download ship json
        constructed_ship_local.build_json_objects()
        ship_json = json.dumps(constructed_ship_local.ship_json_object, indent=4)
        st.download_button(
            label="Download JSON (For Import)",
            file_name=f"{constructed_ship_local.name}.json",
            mime="application/json",
            data=ship_json,
        )

        st.write(st.session_state.constructed_ship_state)

with import_ship:
    #import ship
    ship_loaded = False

    json_upload_f = st.file_uploader("Upload ship JSON file for import:")
    if json_upload_f is not None:
        try:
            loaded_ship_json = json.load(json_upload_f)
        except json.decoder.JSONDecodeError:
            st.write("Invalid JSON. Try again.")
        else:
            error_list = validate_json(loaded_ship_json)
            if error_list == []:
                ship_loaded = True #for edit display
                st.write('Ship imported successfully!')
                imported_ship_instance = load_ship_details_json(loaded_ship_json)
                st.session_state.imported_ship_state = imported_ship_instance
            else: 
                st.write(f"\nIMPORT ERRORS:")
                for error in error_list:
                    st.write(f"{error.message}")
    
    import_col1, import_col2, import_col3 = st.columns(3)
    
    if ship_loaded:
        imported_ship_local = ship_core(st_element=import_col1, name_key='import-name', sclass_key='import-sclass',
            name_loaded_value=imported_ship_instance.name,
            sclass_loaded_value=[sclass['id'] for sclass in build_data.sclass_details if sclass['sclass'] == imported_ship_instance.sclass][0])
        
        armor(st_element=import_col1, ohs_key='import-ohs', ihs_key='import-ihs',
            ohs_loaded_value=[strength['id'] for strength in build_data.outer_strength_details if strength['name'] == imported_ship_instance.outer_hull_strength_str][0],
            ihs_loaded_value=[strength['id'] for strength in build_data.inner_strength_details if strength['name'] == imported_ship_instance.inner_hull_strength_str][0],
            st_ship=st.session_state.imported_ship_edit_state, local_ship=imported_ship_local)
        
        propulsion(st_element=import_col1, tp_key='import-tp', tp_loaded_value=imported_ship_instance.thrust_points,
                st_ship=st.session_state.imported_ship_edit_state, local_ship=imported_ship_local)
        
        weapons(st_element=import_col2, weap_key='import-weap',
            weap_loaded_value=[list(weapon["name"] for weapon in imported_ship_instance.front_arc_weapon_list),
                    list(weapon["name"] for weapon in imported_ship_instance.rear_arc_weapon_list),
                    list(weapon["name"] for weapon in imported_ship_instance.right_arc_weapon_list),
                    list(weapon["name"] for weapon in imported_ship_instance.left_arc_weapon_list)], 
            st_ship=st.session_state.imported_ship_edit_state, local_ship=imported_ship_local)
        
        equipment(st_element=import_col2, equip_key='import-equip',
            equip_loaded_value=list(equipment["name"] for equipment in imported_ship_instance.equipment_list), 
            st_ship=st.session_state.imported_ship_edit_state, local_ship=imported_ship_local)

        crew_quality(st_element=import_col3, cq_key='import-cq',
            cq_loaded_value=[cq['id'] for cq in build_data.crew_quality_details if cq['name'] == imported_ship_instance.crew_quality_str][0],
            st_ship=st.session_state.imported_ship_edit_state, local_ship=imported_ship_local)

        st.session_state.imported_ship_edit_state = imported_ship_local

        #DEBUG
        st.write(loaded_ship_json)
        st.write(st.session_state)
        st.write(imported_ship_instance)
        st.write(imported_ship_local)
        st.write(st.session_state.imported_ship_state)
        st.write(st.session_state.imported_ship_edit_state)


