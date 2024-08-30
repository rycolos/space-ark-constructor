import streamlit as st
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

    build_col1, build_col2, build_col3 = st.columns(3)

    with build_col1.expander('**Ship Core**', expanded=True):
        name = st.text_input("Ship Name")
        sclass = st.selectbox('Ship Class', [s['sclass'] for s in build_data.sclass_details])
        if sclass:
            ship = build_base_ship(name, sclass)
            st.session_state.ship = ship

    with build_col1.expander('**Armor**', expanded=True):
        ohs_input = st.selectbox('Outer Hull Strength', [s['name'] for s in build_data.outer_strength_details])
        if ohs_input:
            ohs_int = [s['id'] for s in build_data.outer_strength_details if s['name'] == ohs_input]
            ship.outer_hull(ohs_int[0])
            ship.track_mass()
            ship.track_base_pv()
            st.session_state.ship = ship

        ihs_input = st.selectbox('Inner Hull Strength', [s['name'] for s in build_data.inner_strength_details])
        if ihs_input:
            ihs_int = [s['id'] for s in build_data.inner_strength_details if s['name'] == ihs_input]
            ship.inner_hull(ihs_int[0])
            ship.track_mass()
            ship.track_base_pv()
            st.session_state.ship = ship

    with build_col1.expander('**Propulsion**', expanded=True):
        tp_input = st.number_input('Thrust Points', min_value=0)
        if tp_input:
            ship.propulsion(tp_input)
            ship.track_mass()
            ship.track_base_pv()
            st.session_state.ship = ship

    with build_col2.expander('**Weapons**', expanded=True):
        front_arc_input = st.multiselect('Front Arc Weapons', [s['name'] for s in build_data.weapon_details])
        if front_arc_input:
            ship.front_arc_weapons(*front_arc_input)
            st.markdown(f'**Total Front Arc Mass:** {ship.total_front_arc_mass}, **Total Front Arc PV:** {ship.total_front_arc_pv}')
            ship.track_mass()
            ship.track_base_pv()
            st.session_state.ship = ship

        rear_arc_input = st.multiselect('Rear Arc Weapons', [s['name'] for s in build_data.weapon_details])
        if rear_arc_input:
            ship.rear_arc_weapons(*rear_arc_input)
            st.markdown(f'**Total Rear Arc Mass:** {ship.total_rear_arc_mass}, **Total Rear Arc PV:** {ship.total_rear_arc_pv}')
            ship.track_mass()
            ship.track_base_pv()
            st.session_state.ship = ship

        right_arc_input = st.multiselect('Right Arc Weapons', [s['name'] for s in build_data.weapon_details])
        if right_arc_input:
            ship.right_arc_weapons(*right_arc_input)
            st.markdown(f'**Total Right Arc Mass:** {ship.total_right_arc_mass}, **Total Right Arc PV:** {ship.total_right_arc_pv}')
            ship.track_mass()
            ship.track_base_pv()
            st.session_state.ship = ship

        left_arc_input = st.multiselect('Left Arc Weapons', [s['name'] for s in build_data.weapon_details])
        if left_arc_input:
            ship.left_arc_weapons(*left_arc_input)
            st.markdown(f'**Total Left Arc Mass:** {ship.total_left_arc_mass}, **Total Left Arc PV:** {ship.total_left_arc_pv}')
            ship.track_mass()
            ship.track_base_pv()
            st.session_state.ship = ship

    with build_col2.expander('**Equipment**', expanded=True):
        equipment_input = st.multiselect('Equipment', [s['name'] for s in build_data.equipment_details])
        if equipment_input:
            build_col3.write(f'{[s['description'] for s in build_data.equipment_details if s['name'] == equipment_input[-1]][0]}')
            equipment_name_to_id = {item["name"]: item["id"] for item in build_data.equipment_details}
            equip_int_list = [equipment_name_to_id[name] for name in equipment_input]
            ship.equipment(*equip_int_list)
            st.markdown(f'**Total Equipment Mass:** {ship.total_equipment_mass}, **Total Equipment PV:** {ship.total_equipment_pv}')
            ship.track_mass()
            ship.track_base_pv()
            st.session_state.ship = ship

    with build_col1.expander('**Crew Quality**', expanded=True):
        crew_quality_input = st.selectbox('Crew Quality', [s['name'] for s in build_data.crew_quality_details])
        if crew_quality_input:
            crew_quality_int = [s['id'] for s in build_data.crew_quality_details if s['name'] == crew_quality_input]
            ship.set_quality(crew_quality_int[0])
            st.session_state.ship = ship

    col1, col2, col3, col4 = st.columns(4)
    ship.track_base_pv()
    ship.track_mass()
    col1.metric(label='Current Mass', value=ship.total_mass)
    col2.metric(label='Mass Remaining', value=ship.mass_delta)
    col3.metric(label='Base PV', value=ship.total_base_pv)
    col4.metric(label='Final PV', value=ship.final_pv)

    build_col3.write(f"""
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
                **Front Arc Weapons:**  {front_arc_input}  
                **Rear Arc Weapons:**  {rear_arc_input}  
                **Right Arc Weapons:**  {right_arc_input}  
                **Left Arc Weapons:** {left_arc_input}  
                """)

#st.write(st.session_state)
#st.write(st.session_state.ship)

oh_squares = ' □' * ship.outer_hull_mass 
ih_squares = ' □' * ship.inner_hull_mass

game_card = f"""
<table>
    <tr>
        <td><b>SHIP NAME</b></td>
        <td>{ship.name}</td>
        <td><b>CLASS</b></td>
        <td>{ship.sclass}</td>
        <td><b>SIZE</b></td>
        <td>{ship.size}</td>
    </tr>
    <tr>
        <td><b>ARMOR</b></td>
        <td>{ship.armor_roll}</td>
        <td><b>BASE PV</b></td>
        <td>{ship.total_base_pv}</td>
        <td><b>FINAL PV</b></td>
        <td>{ship.final_pv}</td>
    </tr>
    <tr>
        <td><b>CREW QUALITY</b></td>
        <td>{ship.crew_quality_str}</td>
        <td><b>MAX STRESS</b></td>
        <td>{ship.max_stress}</td>
        <td><b>CRIT THRESH</b></td>
        <td>{ship.critical_threshold}</td>
    </tr>
    <tr>
        <td><b>THRUST POINTS</b></td>
        <td>{ship.thrust_points}</td>
        <td><b>MAX THRUST</b></td>
        <td>{ship.max_thrust}</td>
        <td></td>
        <td></td>
    </tr>
    <tr>
        <td colspan="6"><b>ARMOR</b></td>
    </tr>
    <tr>
        <td>Outer Hull ({ship.outer_hull_mass})</td>
        <td colspan="5">{oh_squares}</td>
    </tr>
    <tr>
        <td>Inner Hull ({ship.inner_hull_mass})</td>
        <td colspan="5">{ih_squares}</td>
    </tr>
    <tr>
        <td colspan="6"><b>EQUIPMENT</b></td>
    </tr>
    <tr>
        <td colspan="6">{''.join(f'{item['name']} -- {item['description']}\n\n' for item in ship.equipment_list)}</td>
    </tr>
    <tr>
        <td colspan="6"><b>WEAPONS</b></td>
    </tr>
    <tr>
        <td colspan="6"><b>Front Arc</b></td>
    </tr>
    <tr>
        <td colspan="6">{''.join(f'{weapon["name"]} -- A/D: {weapon["attack"]}/{weapon["damage"]} -- R: {weapon["range"]} -- S: {weapon["special"]}\n\n' for weapon in ship.front_arc_weapon_list)}</td>
    </tr>
    <tr>
        <td colspan="6"><b>Rear Arc</b></td>
    </tr>
    <tr>
        <td colspan="6">{''.join(f'{weapon["name"]} -- A/D: {weapon["attack"]}/{weapon["damage"]} -- R: {weapon["range"]} -- S: {weapon["special"]}\n\n' for weapon in ship.rear_arc_weapon_list)}</td>
    </tr>
    <tr>
        <td colspan="6"><b>Right Arc</b></td>
    </tr>
    <tr>
        <td colspan="6">{''.join(f'{weapon["name"]} -- A/D: {weapon["attack"]}/{weapon["damage"]} -- R: {weapon["range"]} -- S: {weapon["special"]}\n\n' for weapon in ship.right_arc_weapon_list)}</td>
    </tr>
    <tr>
        <td colspan="6"><b>Left Arc</b></td>
    </tr>
    <tr>
        <td colspan="6">{''.join(f'{weapon["name"]} -- A/D: {weapon["attack"]}/{weapon["damage"]} -- R: {weapon["range"]} -- S: {weapon["special"]}\n\n' for weapon in ship.left_arc_weapon_list)}</td>
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

st.markdown(game_card, unsafe_allow_html=True)

