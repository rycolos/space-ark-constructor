import streamlit as st
import build_data
from ShipClass import ShipClass
import json, jsonschema

def build_base_ship(name, sclass) -> ShipClass:
    """Instantiate base ship from name and ship class inputs"""

    size = [s['size'] for s in build_data.sclass_details if s['sclass'] == sclass]
    tam = [s['tam'] for s in build_data.sclass_details if s['sclass'] == sclass]
    armor_roll = [s['armor_roll'] for s in build_data.sclass_details if s['sclass'] == sclass]
    mdpa = [s['mdpa'] for s in build_data.sclass_details if s['sclass'] == sclass]
    return ShipClass(name, sclass, size[0], tam[0], armor_roll[0], mdpa[0])

def build_armor():
    pass

st.set_page_config(layout="wide")
st.title('Space Ark Constructor')

build_col, spacer, view_col = st.columns(3)

name = build_col.text_input("Ship Name")
sclass = build_col.selectbox('Ship Class', [s['sclass'] for s in build_data.sclass_details])

if sclass:
    ship = build_base_ship(name, sclass)
    if "ship" not in st.session_state:
        st.session_state.ship = ship

crew_quality_input = build_col.selectbox('Crew Quality', [s['name'] for s in build_data.crew_quality_details])
if crew_quality_input:
    crew_quality_int = [s['id'] for s in build_data.crew_quality_details if s['name'] == crew_quality_input]
    ship.set_quality(crew_quality_int[0])
    # build_col.write(ship.pv_factor[0])
    # build_col.write(ship.total_base_pv)
    # build_col.write(ship.final_pv) #why isn't this working???

ohs_input = build_col.selectbox('Outer Hull Strength', [s['name'] for s in build_data.outer_strength_details])
if ohs_input:
    ohs_int = [s['id'] for s in build_data.outer_strength_details if s['name'] == ohs_input]
    ship.outer_hull(ohs_int[0])
    ship.track_mass()
    ship.track_base_pv()

ihs_input = build_col.selectbox('Inner Hull Strength', [s['name'] for s in build_data.inner_strength_details])
if ihs_input:
    ihs_int = [s['id'] for s in build_data.inner_strength_details if s['name'] == ihs_input]
    ship.inner_hull(ihs_int[0])
    ship.track_mass()
    ship.track_base_pv()

tp_input = build_col.number_input('Thrust Points', min_value=0)
if tp_input:
    ship.propulsion(tp_input)
    ship.track_mass()
    ship.track_base_pv()

col1, col2, col3, col4 = st.columns(4)
ship.track_base_pv()
ship.track_mass()
col1.metric(label='Current Mass', value=ship.total_mass)
col2.metric(label='Mass Remaining', value=ship.mass_delta)
col3.metric(label='Base PV', value=ship.total_base_pv)
col4.metric(label='Final PV', value=ship.final_pv)

view_col.write(f"""
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
            """)

st.write(st.session_state)


# import_button = st.button("Import Ship")
# if import_button:
#     pass

# export_button = st.button("Export Ship")
# if export_button:
#     pass

# view_button = st.button("View Ship")
# if view_button:
#     pass