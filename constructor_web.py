import streamlit as st
import build_data
from ShipClass import ShipClass
import json, jsonschema, os
from datetime import datetime
import markdownify
from html2image import Html2Image

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
    # hide_st_style = """
    #         <style>
    #         footer {visibility: hidden;}
    #         header {visibility: hidden;}
    #         </style>
    #         """
    # st.markdown(hide_st_style, unsafe_allow_html=True)

def front_weapon_stat():
    if st.session_state.front_arc != []:
        front_weapon_stat = ('/n'.join(f'{weapon["name"]} -- A/D: {weapon["attack"]}/{weapon["damage"]} -- R: {weapon["range"]} -- S: {weapon["special"]}' for weapon in build_data.weapon_details if weapon['name'] == st.session_state.front_arc[-1]))
        build_col3.info(front_weapon_stat, icon=":material/info:")

def rear_weapon_stat():            
    if st.session_state.rear_arc != []:
        rear_weapon_stat = ('/n'.join(f'{weapon["name"]} -- A/D: {weapon["attack"]}/{weapon["damage"]} -- R: {weapon["range"]} -- S: {weapon["special"]}' for weapon in build_data.weapon_details if weapon['name'] == st.session_state.rear_arc[-1]))
        build_col3.info(rear_weapon_stat, icon=":material/info:")

def right_weapon_stat():
    if st.session_state.right_arc != []:
        right_weapon_stat = ('/n'.join(f'{weapon["name"]} -- A/D: {weapon["attack"]}/{weapon["damage"]} -- R: {weapon["range"]} -- S: {weapon["special"]}' for weapon in build_data.weapon_details if weapon['name'] == st.session_state.right_arc[-1]))
        build_col3.info(right_weapon_stat, icon=":material/info:")

def left_weapon_stat():            
    if st.session_state.left_arc != []:
        left_weapon_stat = ('/n'.join(f'{weapon["name"]} -- A/D: {weapon["attack"]}/{weapon["damage"]} -- R: {weapon["range"]} -- S: {weapon["special"]}' for weapon in build_data.weapon_details if weapon['name'] == st.session_state.left_arc[-1]))
        build_col3.info(left_weapon_stat, icon=":material/info:")

def equipment_stat():
    if st.session_state.equipment != []:
        equipment_stat = (f'{[s['description'] for s in build_data.equipment_details if s['name'] == st.session_state.equipment[-1]][0]}')
        build_col3.info(equipment_stat, icon=":material/info:")

if __name__ == "__main__":
    configure_page()

    build_col1, build_col2, build_col3 = st.columns(3)

    with build_col1.expander(label='**Ship Core**', expanded=True):
        name = st.text_input(label="Ship Name")
        sclass = st.selectbox(label='Ship Class', options=[s['sclass'] for s in build_data.sclass_details])
        if sclass:
            ship = build_base_ship(name, sclass)
            st.session_state.ship = ship

    with build_col1.expander('**Armor**', expanded=True):
        ohs_input = st.selectbox(label='Outer Hull Strength', options=[s['name'] for s in build_data.outer_strength_details])
        if ohs_input:
            ohs_int = [s['id'] for s in build_data.outer_strength_details if s['name'] == ohs_input]
            ship.outer_hull(ohs_int[0])
            ship.track_mass()
            ship.track_base_pv()
            st.session_state.ship = ship

        ihs_input = st.selectbox(label='Inner Hull Strength', options=[s['name'] for s in build_data.inner_strength_details])
        if ihs_input:
            ihs_int = [s['id'] for s in build_data.inner_strength_details if s['name'] == ihs_input]
            ship.inner_hull(ihs_int[0])
            ship.track_mass()
            ship.track_base_pv()
            st.session_state.ship = ship

    with build_col1.expander(label='**Propulsion**', expanded=True):
        tp_input = st.number_input(label='Thrust Points', min_value=0)
        if tp_input:
            ship.propulsion(tp_input)
            ship.track_mass()
            ship.track_base_pv()
            st.session_state.ship = ship

    with build_col2.expander(label='**Weapons**', expanded=True):
        front_arc_input = st.multiselect(label='Front Arc Weapons', key='front_arc', options=[s['name'] for s in build_data.weapon_details for i in range(4)], on_change=front_weapon_stat)
        if front_arc_input:  
            ship.front_arc_weapons(*front_arc_input)
            st.markdown(f'**Arc Mass:** {ship.total_front_arc_mass} — **Arc PV:** {ship.total_front_arc_pv} — **Arc Damage:** {ship.total_front_arc_max_dmg}')
            ship.track_mass()
            ship.track_base_pv()
            st.session_state.ship = ship

        rear_arc_input = st.multiselect(label='Rear Arc Weapons', key='rear_arc', options=[s['name'] for s in build_data.weapon_details for i in range(4)], on_change=rear_weapon_stat)
        if rear_arc_input:
            ship.rear_arc_weapons(*rear_arc_input)
            st.markdown(f'**Arc Mass:** {ship.total_rear_arc_mass} — **Arc PV:** {ship.total_rear_arc_pv} — **Arc Damage:** {ship.total_rear_arc_max_dmg}')
            ship.track_mass()
            ship.track_base_pv()
            st.session_state.ship = ship

        right_arc_input = st.multiselect(label='Right Arc Weapons', key='right_arc', options=[s['name'] for s in build_data.weapon_details for i in range(4)], on_change=right_weapon_stat)
        if right_arc_input:
            ship.right_arc_weapons(*right_arc_input)
            st.markdown(f'**Arc Mass:** {ship.total_right_arc_mass} — **Arc PV:** {ship.total_right_arc_pv} — **Arc Damage:** {ship.total_right_arc_max_dmg}')
            ship.track_mass()
            ship.track_base_pv()
            st.session_state.ship = ship

        left_arc_input = st.multiselect(label='Left Arc Weapons', key='left_arc', options=[s['name'] for s in build_data.weapon_details for i in range(4)], on_change=left_weapon_stat)
        if left_arc_input:
            ship.left_arc_weapons(*left_arc_input)
            st.markdown(f'**Arc Mass:** {ship.total_left_arc_mass} — **Arc PV:** {ship.total_left_arc_pv} — **Arc Damage:** {ship.total_left_arc_max_dmg}')
            ship.track_mass()
            ship.track_base_pv()
            st.session_state.ship = ship

    with build_col2.expander(label='**Equipment**', expanded=True):
        equipment_input = st.multiselect(label='Equipment', key='equipment', options=[s['name'] for s in build_data.equipment_details], on_change=equipment_stat)
        if equipment_input:            
            equipment_name_to_id = {item["name"]: item["id"] for item in build_data.equipment_details}
            equip_int_list = [equipment_name_to_id[name] for name in equipment_input]
            ship.equipment(*equip_int_list)
            st.markdown(f'**Total Equipment Mass:** {ship.total_equipment_mass}, **Total Equipment PV:** {ship.total_equipment_pv}')
            ship.track_mass()
            ship.track_base_pv()
            st.session_state.ship = ship

    with build_col1.expander(label='**Crew Quality**', expanded=True):
        crew_quality_input = st.selectbox(label='Crew Quality', options=[s['name'] for s in build_data.crew_quality_details])
        if crew_quality_input:
            crew_quality_int = [s['id'] for s in build_data.crew_quality_details if s['name'] == crew_quality_input]
            ship.set_quality(crew_quality_int[0])
            st.session_state.ship = ship

    metric_col1, metric_col2 = build_col3.columns(2)
    ship.track_base_pv()
    ship.track_mass()

    if ship.tam_exceeded:
        build_col3.info(f'Mass overage of {abs(ship.mass_delta)}!', icon=":material/warning:")

    if ship.total_front_arc_max_dmg > ship.mdpa:
        build_col3.info(f'Front arc damage overage of {abs(ship.mdpa - ship.total_front_arc_max_dmg)}!', icon=":material/warning:")
    
    if ship.total_rear_arc_max_dmg > ship.mdpa:
        build_col3.info(f'Rear arc damage overage of {abs(ship.mdpa - ship.total_rear_arc_max_dmg)}!', icon=":material/warning:")
    
    if ship.total_right_arc_max_dmg > ship.mdpa:
        build_col3.info(f'Right arc damage overage of {abs(ship.mdpa - ship.total_right_arc_max_dmg)}!', icon=":material/warning:")
    
    if ship.total_left_arc_max_dmg > ship.mdpa:
        build_col3.info(f'Left arc damage overage of {abs(ship.mdpa - ship.total_left_arc_max_dmg)}!', icon=":material/warning:")

    metric_col1.metric(label='Current Mass', value=ship.total_mass)
    metric_col1.metric(label='Mass Remaining', value=ship.mass_delta)
    metric_col2.metric(label='Base PV', value=ship.total_base_pv)
    metric_col2.metric(label='Final PV', value=ship.final_pv)

    build_col3.write(f"""
                ### Calculated Stats: 
                **Ship Size:** {ship.size}  
                **Total Available Mass:** {ship.tam}  
                **Max Damage Per Arc:** {ship.mdpa}  
                **Armor Roll:** {ship.armor_roll}  
                **Critical Threshold:** {ship.critical_threshold}  
                **Max Thrust:** {ship.max_thrust}  
                **Max Stress:** {ship.max_stress}  
                """)

#st.write(st.session_state)
#st.write(st.session_state.ship)

st.header("Ship Card")
oh_squares = ' □' * ship.outer_hull_mass 
ih_squares = ' □' * ship.inner_hull_mass

game_card_html = f"""
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
        <td><b>CRITICAL THRESHOLD</b></td>
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
        <td colspan="6">{''.join(f'{item['name']}<br>' for item in ship.equipment_list)}</td>
    </tr>
    <tr>
        <td colspan="6"><b>WEAPONS</b></td>
    </tr>
    <tr>
        <td colspan="6"><b>Front Arc</b></td>
    </tr>
    <tr>
        <td colspan="6">{''.join(f'{weapon["name"]} -- A/D: {weapon["attack"]}/{weapon["damage"]} -- R: {weapon["range"]} -- S: {weapon["special"]}<br>' for weapon in ship.front_arc_weapon_list)}</td>
    </tr>
    <tr>
        <td colspan="6"><b>Rear Arc</b></td>
    </tr>
    <tr>
        <td colspan="6">{''.join(f'{weapon["name"]} -- A/D: {weapon["attack"]}/{weapon["damage"]} -- R: {weapon["range"]} -- S: {weapon["special"]}<br>' for weapon in ship.rear_arc_weapon_list)}</td>
    </tr>
    <tr>
        <td colspan="6"><b>Right Arc</b></td>
    </tr>
    <tr>
        <td colspan="6">{''.join(f'{weapon["name"]} -- A/D: {weapon["attack"]}/{weapon["damage"]} -- R: {weapon["range"]} -- S: {weapon["special"]}<br>' for weapon in ship.right_arc_weapon_list)}</td>
    </tr>
    <tr>
        <td colspan="6"><b>Left Arc</b></td>
    </tr>
    <tr>
        <td colspan="6">{''.join(f'{weapon["name"]} -- A/D: {weapon["attack"]}/{weapon["damage"]} -- R: {weapon["range"]} -- S: {weapon["special"]}<br>' for weapon in ship.left_arc_weapon_list)}</td>
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

st.markdown(game_card_html, unsafe_allow_html=True)

game_card_txt = (f"\nSHIP NAME: {ship.name}"
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

#download ship image
img_path_server = "tmp_images/"
hti = Html2Image(output_path=img_path_server)
hti.browser.flags = ['--default-background-color=ffffff', '--hide-scrollbars']
img_download_fname = f"{ship.name}_image_{datetime.today().strftime('%Y%m%d')}.png"

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
txt_download_fname = f"{ship.name}_txt_{datetime.today().strftime('%Y%m%d')}"
st.download_button(
    label="Download Ship Card (Text Only)",
    data=game_card_txt,
    file_name=txt_download_fname,
    mime="text/plain",
)

#donwload ship json
ship.build_json_objects()
ship_json = json.dumps(ship.ship_json_object, indent=4)
st.download_button(
    label="Download JSON (For Import)",
    file_name=f"{ship.name}.json",
    mime="application/json",
    data=ship_json,
)