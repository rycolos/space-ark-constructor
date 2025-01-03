import streamlit as st
import build_data
from ShipClass import ShipClass
import json, jsonschema
from datetime import datetime

SCHEMA_FILE = 'import_schema.json'

#INITIALIZE PAGE, SESSION
def configure_page() -> None:
    """
    Apply basic page configuration
    """ 
    title = 'Space Ark Constructor'
    st.set_page_config(page_title=title, page_icon=':ringed_planet:', layout='wide')
    st.title(title)
    construct_ship, import_ship, view_ship, help = st.tabs(["Construct Ship", "Import Ship", 'View Ship', 'Help'])
    
    #load and apply style for custom label sizes, custom header
    with open('style.css') as f:
        st.markdown(f"<style>{f.read()}</style>", unsafe_allow_html=True)
    
    return construct_ship, import_ship, view_ship, help

def init_session() -> None:
    """
    Initialize st session_state keys to empty ShipClass instances
    """
    if 'constructed_ship_state' not in st.session_state:
        st.session_state.constructed_ship_state = ShipClass
    if 'imported_ship_state' not in st.session_state:
        st.session_state.imported_ship_state = ShipClass
    if 'imported_ship_edit_state' not in st.session_state:
        st.session_state.imported_ship_edit_state = ShipClass

#ShipClass INSTANCE
def build_base_ship(name: str, sclass: str) -> ShipClass:
    """
    Instantiate base ship from name and ship class inputs
    """
    size = [s['size'] for s in build_data.sclass_details if s['sclass'] == sclass]
    tam = [s['tam'] for s in build_data.sclass_details if s['sclass'] == sclass]
    armor_roll = [s['armor_roll'] for s in build_data.sclass_details if s['sclass'] == sclass]
    mdpa = [s['mdpa'] for s in build_data.sclass_details if s['sclass'] == sclass]
    return ShipClass(name, sclass, size[0], tam[0], armor_roll[0], mdpa[0])

#BUILD UI
def ship_core(st_element: str, name_key: str, sclass_key: str, name_loaded_value: str, sclass_loaded_value: int) -> ShipClass:
    """
    Build UI for Ship Name, Class. Builds ShipClass instance constructed_ship_local
    """
    with st_element.expander(label='**Ship Core**', expanded=True):
        name = st.text_input(label="Ship Name", value=name_loaded_value, max_chars=32)
        sclass = st.selectbox(label='Ship Class', key=sclass_key, index=sclass_loaded_value, options=[s['sclass'] for s in build_data.sclass_details])
        if sclass:
            constructed_ship_local = build_base_ship(name, sclass)
            st.write(f'Armor Roll :green[{constructed_ship_local.armor_roll}]')
            st.session_state.constructed_ship_state = constructed_ship_local
    return constructed_ship_local

def armor(st_element: str, ohs_key: str, ihs_key: str, ohs_loaded_value: int, ihs_loaded_value: int, st_ship: ShipClass, local_ship: ShipClass) -> None:
    """
    Build UI for Ship Outer Hull, Inner Hull.
    st_ship should be st session_state ShipClass instance of constructed_ship_local ShipClass instance
    """
    with st_element.expander('**Armor**', expanded=True):
        ohs_input = st.selectbox(label='Outer Hull Strength', key=ohs_key, index=ohs_loaded_value, options=[s['name'] for s in build_data.outer_strength_details])
        if ohs_input:
            ohs_int = [s['id'] for s in build_data.outer_strength_details if s['name'] == ohs_input]
            local_ship.outer_hull(ohs_int[0])
            local_ship.track_mass()
            local_ship.track_base_pv()
            st_ship = local_ship
        st.write(f'Mass :green[{local_ship.outer_hull_mass}] — PV :green[{local_ship.outer_hull_pv}] — Critical Threshold :green[{local_ship.critical_threshold}]')

        ihs_input = st.selectbox(label='Inner Hull Strength', key=ihs_key, index=ihs_loaded_value, options=[s['name'] for s in build_data.inner_strength_details])
        if ihs_input:
            ihs_int = [s['id'] for s in build_data.inner_strength_details if s['name'] == ihs_input]
            local_ship.inner_hull(ihs_int[0])
            local_ship.track_mass()
            local_ship.track_base_pv()
            st_ship = local_ship
        st.write(f'Mass :green[{local_ship.inner_hull_mass}] — PV :green[{local_ship.inner_hull_pv}]')
        st.divider()
        st.write(f'Total Armor Mass :green[{local_ship.outer_hull_mass + local_ship.inner_hull_mass}] — Total Armor PV :green[{local_ship.outer_hull_pv + local_ship.inner_hull_pv}]')

def propulsion(st_element: str, tp_key: str, tp_loaded_value: str, st_ship: ShipClass, local_ship: ShipClass) -> None:
    """
    Build UI for Ship Propulsion
    st_ship should be st session_state ShipClass instance of constructed_ship_local ShipClass instance
    """
    with st_element.expander(label='**Propulsion**', expanded=True):
        tp_input = st.number_input(label='Thrust Points', key=tp_key, value=tp_loaded_value, min_value=0)
        if tp_input:
            local_ship.propulsion(tp_input)
            local_ship.track_mass()
            local_ship.track_base_pv()
            st_ship = local_ship
        st.write(f'Mass :green[{local_ship.propulsion_mass}] — PV :green[{local_ship.propulsion_pv}] — Max Thrust :green[{local_ship.max_thrust}]')

def crew_quality(st_element: str, cq_key: str, cq_loaded_value: int, st_ship: ShipClass, local_ship: ShipClass) -> None:
    """
    Build UI for Ship Crew Quality
    st_ship should be st session_state ShipClass instance of constructed_ship_local ShipClass instance
    """
    with st_element.expander(label='**Crew Quality**', expanded=True):
        crew_quality_input = st.selectbox(label='Crew Quality', key=cq_key, index=cq_loaded_value, options=[s['name'] for s in build_data.crew_quality_details])
        if crew_quality_input:
            crew_quality_int = [s['id'] for s in build_data.crew_quality_details if s['name'] == crew_quality_input]
            local_ship.set_quality(crew_quality_int[0])
            st_ship = local_ship
        st.write(f'Max Stress :green[{local_ship.max_stress}]')

def equipment(st_element: str, equip_key: str, equip_loaded_value: str, st_ship: ShipClass, local_ship: ShipClass) -> None:
    """
    Build UI for Ship Equipment
    st_ship should be st session_state ShipClass instance of constructed_ship_local ShipClass instance
    """
    with st_element.expander(label='**Equipment**', expanded=True):
        equipment_input = st.multiselect(label='Equipment', key=equip_key, default=equip_loaded_value, options=[s['name'] for s in build_data.equipment_details])
        if equipment_input:            
            equipment_name_to_id = {item["name"]: item["id"] for item in build_data.equipment_details}
            equip_int_list = [equipment_name_to_id[name] for name in equipment_input]
            local_ship.equipment(*equip_int_list)
            local_ship.track_mass()
            local_ship.track_base_pv()
            st_ship = local_ship
        st.write(f'Total Equipment Mass :green[{local_ship.total_equipment_mass}] — Total Equipment PV :green[{local_ship.total_equipment_pv}]')

def weapons(st_element: str, weap_key: str, weap_loaded_value: str, st_ship: ShipClass, local_ship: ShipClass) -> None:
    """
    Build UI for Ship Weapons
    st_ship should be st session_state ShipClass instance of constructed_ship_local ShipClass instance
    """
    with st_element.expander(label='**Weapons**', expanded=True):
        weapon_helper = f'<span style="font-size: .9em;">A weapon can be duplicated in a firing arc up to 4 times. Arc damage cannot exceed Max Damage Per Arc (:green[{local_ship.mdpa}]).</span>'
        st.markdown(weapon_helper, unsafe_allow_html=True)
        
        front_arc_input = st.multiselect(label='Front Arc Weapons', key=weap_key+'-front-arc', default=weap_loaded_value[0], options=[s['name'] for s in build_data.weapon_details for i in range(4)])
        if front_arc_input:  
            local_ship.front_arc_weapons(*front_arc_input)
            local_ship.track_mass()
            local_ship.track_base_pv()
            st_ship = local_ship
        st.write(f'Arc Mass :green[{local_ship.total_front_arc_mass}] — Arc PV :green[{local_ship.total_front_arc_pv}] — Arc Damage :green[{local_ship.total_front_arc_max_dmg}]')

        rear_arc_input = st.multiselect(label='Rear Arc Weapons', key=weap_key+'-rear-arc', default=weap_loaded_value[1], options=[s['name'] for s in build_data.weapon_details for i in range(4)])
        if rear_arc_input:
            local_ship.rear_arc_weapons(*rear_arc_input)
            local_ship.track_mass()
            local_ship.track_base_pv()
            st_ship = local_ship
        st.write(f'Arc Mass :green[{local_ship.total_rear_arc_mass}] — Arc PV :green[{local_ship.total_rear_arc_pv}] — Arc Damage :green[{local_ship.total_rear_arc_max_dmg}]')

        right_arc_input = st.multiselect(label='Right Arc Weapons', key=weap_key+'-right-arc', default=weap_loaded_value[2], options=[s['name'] for s in build_data.weapon_details for i in range(4)])
        if right_arc_input:
            local_ship.right_arc_weapons(*right_arc_input)
            local_ship.track_mass()
            local_ship.track_base_pv()
            st_ship = local_ship
        st.write(f'Arc Mass :green[{local_ship.total_right_arc_mass}] — Arc PV :green[{local_ship.total_right_arc_pv}] — Arc Damage :green[{local_ship.total_right_arc_max_dmg}]')

        left_arc_input = st.multiselect(label='Left Arc Weapons', key=weap_key+'-left-arc', default=weap_loaded_value[3], options=[s['name'] for s in build_data.weapon_details for i in range(4)])
        if left_arc_input:
            local_ship.left_arc_weapons(*left_arc_input)
            local_ship.track_mass()
            local_ship.track_base_pv()
            st_ship = local_ship
        st.write(f'Arc Mass :green[{local_ship.total_left_arc_mass}] — Arc PV :green[{local_ship.total_left_arc_pv}] — Arc Damage :green[{local_ship.total_left_arc_max_dmg}]')
        st.divider()
        st.write(f'Total Weapon Mass :green[{local_ship.total_front_arc_mass + local_ship.total_rear_arc_mass + local_ship.total_right_arc_mass + local_ship.total_left_arc_mass}] — Total Weapon PV :green[{local_ship.total_front_arc_pv + local_ship.total_rear_arc_pv + local_ship.total_right_arc_pv + local_ship.total_left_arc_pv}]')

#BUILD STAT DISPLAY, ERROR
def error_tam_exceeded(st_element: str, local_ship: ShipClass) -> None:
    """
    UI error message if TAM exceeded
    """
    if local_ship.tam_exceeded:
        st_element.error(f'Mass overage of {abs(local_ship.mass_delta)}!', icon=":material/warning:")

def error_mdpa_exceeded(st_element: str, local_ship: ShipClass) -> None:
    """
    UI error message if MDPA exceeded
    """
    arc_names = ['front', 'rear', 'right', 'left']
    for arc in arc_names:
        total_dmg = getattr(local_ship, f'total_{arc}_arc_max_dmg')
        if total_dmg > local_ship.mdpa:
            st_element.error(f'{arc.capitalize()} Arc damage overage of {abs(local_ship.mdpa - total_dmg)}!', icon=":material/warning:")

def live_metrics(st_element: str, local_ship: ShipClass) -> None:
    """
    UI display metrics for Mass and PV calculations
    """
    #MASS
    mass_container = st_element.container(border=True)
    mass_container.write("### Ship Mass")
    mass_metric_col1, mass_metric_col2, mass_metric_col3 = mass_container.columns(3)
    mass_metric_col1.metric(label='Current', value=local_ship.total_mass)
    mass_metric_col2.metric(label='Available', value=local_ship.mass_delta)
    mass_metric_col3.metric(label='TAM', value=local_ship.tam)
    
    #PV
    pv_container = st_element.container(border=True)
    pv_container.write("### Point value")
    pv_metric_col1, pv_metric_col2 = pv_container.columns(2)
    pv_metric_col1.metric(label='Base PV', value=local_ship.total_base_pv)
    pv_metric_col2.metric(label='Final PV', value=local_ship.final_pv)

def build_game_cards(local_ship: ShipClass) -> tuple[str, str]:
    """
    Construct HTML and Txt versions of game card for presentation and export
    """
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
                    f"\n{''.join(f'{weapon["name"]} — A/D: {weapon["attack"]}/{weapon["damage"]} — R: {weapon["range"]} — S: {weapon["special"]}\n' for weapon in local_ship.front_arc_weapon_list)}"
                    f"\n***Rear Arc***"
                    f"\n{''.join(f'{weapon["name"]} — A/D: {weapon["attack"]}/{weapon["damage"]} — R: {weapon["range"]} — S: {weapon["special"]}\n' for weapon in local_ship.rear_arc_weapon_list)}"
                    f"\n***Right Arc***"
                    f"\n{''.join(f'{weapon["name"]} — A/D: {weapon["attack"]}/{weapon["damage"]} — R: {weapon["range"]} — S: {weapon["special"]}\n' for weapon in local_ship.right_arc_weapon_list)}"
                    f"\n***Left Arc***"
                    f"\n{''.join(f'{weapon["name"]} — A/D: {weapon["attack"]}/{weapon["damage"]} — R: {weapon["range"]} — S: {weapon["special"]}\n' for weapon in local_ship.left_arc_weapon_list)}"
                    f"\nCRITICAL HITS:"
                    f"\n□ □ Engineering Hit    □ □ Major Weapon Damage (F/RT/LT/R)"
                    f"\n□ Targeting Hit    □ □ □ □ Weapon Damage (F/RT/LT/R)"
                    f"\n□ □ □ Crew Hit    □ □ Side Thruster Damage"
                    f"\n□ □ □ □ □ Engine Room Damage    □ □ Engines Disabled"
                    )

    return game_card_html, game_card_txt

#EXPORT SHIP
def download_json(local_ship: ShipClass) -> None:
    """
    Build and export JSON of ship
    """
    json_download_fname = f"{local_ship.name}_json_{datetime.today().strftime('%Y%m%d')}.json"
    local_ship.build_json_objects()
    ship_json = json.dumps(local_ship.ship_json_object, indent=4)
    st.download_button(
        label="Download JSON (For Import)",
        file_name=json_download_fname,
        mime="application/json",
        data=ship_json,
    )

def download_text(local_ship: ShipClass) -> None:
    """
    Export txt file of ship
    """
    txt_download_fname = f"{local_ship.name}_txt_{datetime.today().strftime('%Y%m%d')}"
    st.download_button(
        label="Download Ship Card (Txt)",
        data=game_card_txt,
        file_name=txt_download_fname,
        mime="text/plain",
    )

#IMPORT SHIP
def validate_json(ship_json: str) -> list:
    """
    Validate ship is valid JSON and validate against schema template
    """
    error_list = []
    with open(SCHEMA_FILE, 'r', encoding='utf-8') as schema_file:
        try:
            schema = json.load(schema_file)
        except json.decoder.JSONDecodeError:
            st.write("Invalid JSON schema validation file.")
            error_list = ['error validating schema']
        else:
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


if __name__ == "__main__":
    construct_ship, import_ship, view_ship, help = configure_page()
    init_session()

    with construct_ship:
        build_col1, build_col2, build_col3 = st.columns(3)

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
        
        crew_quality(st_element=build_col3, cq_key='construct-cq', cq_loaded_value=1,
            st_ship=st.session_state.constructed_ship_state, local_ship=constructed_ship_local)

        #Metrics/Stats
        constructed_ship_local.track_base_pv()
        constructed_ship_local.track_mass()
        error_tam_exceeded(st_element=build_col3, local_ship=constructed_ship_local)
        error_mdpa_exceeded(st_element=build_col3, local_ship=constructed_ship_local)
        live_metrics(build_col3, constructed_ship_local)
    
    with import_ship:
        #Import
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
                    imported_ship_instance = load_ship_details_json(loaded_ship_json)
                    st.write('Ship imported successfully!')
                    st.session_state.imported_ship_state = imported_ship_instance
                elif error_list != ['error validating schema']: 
                    st.write(f"\nERRORS FOUND WHILE IMPORTING SHIP:")
                    for error in error_list:
                        st.write(f"{error.message}")
                else:
                    st.write(f"\nScehma validation error. Cannot import without error checking.")
        
        import_col1, import_col2, import_col3 = st.columns(3)
        
        if ship_loaded:
            #Builds Fields
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

            #Metrics/Stats
            imported_ship_local.track_base_pv()
            imported_ship_local.track_mass()
            error_tam_exceeded(st_element=import_col3, local_ship=imported_ship_local)
            error_mdpa_exceeded(st_element=import_col3, local_ship=imported_ship_local)
            live_metrics(import_col3, imported_ship_local)

            #DEBUG
            # st.write(loaded_ship_json)
            # st.write(st.session_state)
            # st.write(imported_ship_instance)
            # st.write(imported_ship_local)
            # st.write(st.session_state.imported_ship_state)
            # st.write(st.session_state.imported_ship_edit_state)

    with view_ship:
        #disable ship_view_selector if no ship is imported
        ship_view_selector_disabled = True
        
        if ship_loaded == True:
            ship_view_selector_disabled = False
        
        #if constructed ship hasn't been named and ship has been imported, default to view import ship
        selector_index = 0
        if ship_loaded == True and constructed_ship_local.name == None:
            selector_index = 1

        ship_view_selector = st.radio("Which ship do you want to view?", ['Constructed Ship', 'Imported Ship'], index=selector_index, disabled=ship_view_selector_disabled)
    
        match ship_view_selector:
            case 'Constructed Ship':
                #st.write(st.session_state.constructed_ship_state)
                game_card_html, game_card_txt = build_game_cards(constructed_ship_local)
                st.code(game_card_txt)
                download_text(constructed_ship_local)
                download_json(constructed_ship_local)
            
            case 'Imported Ship':
                #st.write(st.session_state.imported_ship_edit_state)
                game_card_html, game_card_txt = build_game_cards(imported_ship_local)
                st.code(game_card_txt)
                download_text(imported_ship_local)
                download_json(imported_ship_local)

    with help:
        help_col1, help_col2, help_col3 = st.columns(3)
        help_col1.markdown("""
            ### SPACE ARK
            *Space Ark is a game of space warship combat, pitting force against
            force in war of attrition for command of the frontier*  
            
            This ship constructor is meant to be used alongside the rulebook (sec. `SHIP DESIGN` and `WEAPONS AND EQUIPMENT`).  
            
            [Download the rulebook for free](https://ryanlaliberty.itch.io/space-ark)
            
            [Space Ark Constructor on GitHub](https://github.com/rycolos/space-ark-constructor)
            
            SPACE ARK and SPACE ARK CONSTRUCTOR are hobby projects and are thus mostly unsupported. If you encounter issues, please reach out via Itch
            or GitHub and I'll do my best to rectify as soon as I'm able.
            
            ### Construct a Ship
            You can use Space Ark Constructor to construct a brand new ship or import a ship previously exported via Space Ark Constructor.  
            
            Setting your ship Name and Class will dictate Total Available Mass to spend on Ship Design.  
            
            Reference the italicized text below the various Ship Design steps to see calculated statistics like Critical Threshold.    
            """)
        
        help_col2.markdown("""
            ### View/Export a Ship
            Once you've built (or imported) a ship and are ready to play, use the View Ship tab to see and export your ship's Stat Sheet.
            It shows your Constructed Ship by default, but you can select Imported Ship to see the Stat Sheet for your currently imported ship. 

            This screen displays your ship's Stat Sheet and allows export as a text file for gameplay purposes.

            If you want to import this ship later for further editing, export to JSON. This is the only way to save ships at this time!                
            """)
        
        help_col3.markdown("""
            ### Import a Ship
            Importing a ship requires a JSON file exported from the View Ship screen. Drag your file into the box or tap the box to browse for a file.
            
            Your file will be verified and then your ship loaded for editing below. Use the View Ship tab to view and export any changes to your Imported Ship.                  
            """)
        

