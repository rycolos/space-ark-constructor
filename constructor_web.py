import streamlit as st
from streamlit_option_menu import option_menu
import build_data
from ShipClass import ShipClass
import json, jsonschema

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
    title = 'Space Ark Constructor'
    st.set_page_config(page_title=title, page_icon=':ringed_planet:', layout='wide')
    st.title(title)
    hide_st_style = """
            <style>
            footer {visibility: hidden;}
            header {visibility: hidden;}
            </style>
            """
    st.markdown(hide_st_style, unsafe_allow_html=True)

if __name__ == "__main__":
    configure_page()

main_selected = option_menu(
    menu_title=None,
    options=['Build Ship', 'Import Ship', 'Export Ship'],
    orientation='horizontal'
)

if main_selected == 'Build Ship':
    build_col1, build_col2, build_col3 = st.columns(3)


    with build_col1.expander('Ship Core', expanded=True):
        name = st.text_input("Ship Name")
        sclass = st.selectbox('Ship Class', [s['sclass'] for s in build_data.sclass_details])
        if sclass:
            ship = build_base_ship(name, sclass)
            if "ship" not in st.session_state:
                st.session_state.ship = ship

    with build_col1.expander('Armor', expanded=True):
        ohs_input = st.selectbox('Outer Hull Strength', [s['name'] for s in build_data.outer_strength_details])
        if ohs_input:
            ohs_int = [s['id'] for s in build_data.outer_strength_details if s['name'] == ohs_input]
            ship.outer_hull(ohs_int[0])
            ship.track_mass()
            ship.track_base_pv()

        ihs_input = st.selectbox('Inner Hull Strength', [s['name'] for s in build_data.inner_strength_details])
        if ihs_input:
            ihs_int = [s['id'] for s in build_data.inner_strength_details if s['name'] == ihs_input]
            ship.inner_hull(ihs_int[0])
            ship.track_mass()
            ship.track_base_pv()

    with build_col1.expander('Propulsion', expanded=True):
        tp_input = st.number_input('Thrust Points', min_value=0)
        if tp_input:
            ship.propulsion(tp_input)
            ship.track_mass()
            ship.track_base_pv()


    with build_col2.expander('Weapons', expanded=True):
        front_arc_input = st.multiselect('Front Arc Weapons', [s['name'] for s in build_data.weapon_details])
        if front_arc_input:
            pass

        rear_arc_input = st.multiselect('Rear Arc Weapons', [s['name'] for s in build_data.weapon_details])
        if rear_arc_input:
            pass

        right_arc_input = st.multiselect('Right Arc Weapons', [s['name'] for s in build_data.weapon_details])
        if right_arc_input:
            pass

        left_arc_input = st.multiselect('Left Arc Weapons', [s['name'] for s in build_data.weapon_details])
        if left_arc_input:
            pass

    with build_col2.expander('Equipment', expanded=True):
        equipment_input = st.multiselect('Equipment', [s['name'] for s in build_data.equipment_details])
        if equipment_input:
            build_col3.write(f'{[s['description'] for s in build_data.equipment_details if s['name'] == equipment_input[-1]][0]}')
            name_to_id = {item["name"]: item["id"] for item in build_data.equipment_details}
            equip_int_list = [name_to_id[name] for name in equipment_input]
            ship.equipment(*equip_int_list)
            st.markdown(f'**Total Equipment Mass:** {ship.total_equipment_mass}, **Total Equipment PV:** {ship.total_equipment_pv}')
            ship.track_mass()
            ship.track_base_pv()

    crew_quality_input = build_col1.selectbox('Crew Quality', [s['name'] for s in build_data.crew_quality_details])
    if crew_quality_input:
        crew_quality_int = [s['id'] for s in build_data.crew_quality_details if s['name'] == crew_quality_input]
        ship.set_quality(crew_quality_int[0])

    col1, col2, col3, col4 = st.columns(4)
    ship.track_base_pv()
    ship.track_mass()
    col1.metric(label='Current Mass', value=ship.total_mass)
    col2.metric(label='Mass Remaining', value=ship.mass_delta)
    col3.metric(label='Base PV', value=ship.total_base_pv)
    col4.metric(label='Final PV', value=ship.final_pv)

    st.write(f"""
                **Ship Name:** {ship.name}  
                **Ship Class:** {ship.sclass}  
                **Ship Size:** {ship.size}  
                **Total Available Mass:** {ship.tam}  
                **Max Damage Per Arc:** {ship.mdpa}  
                **Armor Roll:** {ship.armor_roll}  
                **Outer Hull Mass:** {ship.outer_hull_mass}  
                **Inner Hull Mass:** {ship.inner_hull_mass}  
                **Critical Threshold:** {ship.critical_threshold}  
                **Thrust Points:** {ship.thrust_points}  
                **Max Thrust:** {ship.max_thrust}  
                **Max Stress:** {ship.max_stress}  
                **Equipment:** {equipment_input}    
                **Front Arc Weapons:**  
                **Rear Arc Weapons:**  
                **Right Arc Weapons:**  
                **Left Arc Weapons:** 
                """)

st.write(st.session_state)
