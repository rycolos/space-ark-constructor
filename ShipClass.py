import build_data
import math

class ShipClass:
    def __init__(self, name: str, sclass: str, size: str, tam: int, armor_roll: str, mdpa: int) -> None: 
        
        self.name = name 
        self.sclass = sclass
        self.size = size
        self.tam = tam
        self.armor_roll = armor_roll
        self.mdpa = mdpa

        self.front_arc_weapons_names = []
        self.total_front_arc_mass = 0
        self.total_front_arc_pv = 0
        self.total_front_arc_max_dmg = 0
        self.rear_arc_weapons_names = []
        self.total_rear_arc_mass = 0
        self.total_rear_arc_pv = 0
        self.total_rear_arc_max_dmg = 0
        self.right_arc_weapons_names = []
        self.total_right_arc_mass = 0
        self.total_right_arc_pv = 0
        self.total_right_arc_max_dmg = 0
        self.left_arc_weapons_names = []
        self.total_left_arc_mass = 0
        self.total_left_arc_pv = 0
        self.total_left_arc_max_dmg = 0

        self.crew_quality_str = ""
        self.equipment_names = []
        self.thrust_points = 0
        self.outer_hull_mass = 0
        self.inner_hull_mass = 0
        self.propulsion_mass = 0
        self.total_equipment_mass = 0
        self.outer_hull_pv = 0
        self.inner_hull_pv = 0
        self.propulsion_pv = 0
        self.total_equipment_pv = 0

    def outer_hull(self, outer_hull_strength: int) -> tuple[int, int, int]:
        """Calculate outer hull mass, PV, critical threshold"""

        mass_factor = [s['mass_factor'] for s in build_data.outer_strength_details if s['id'] == outer_hull_strength]
        self.outer_hull_mass = math.ceil(self.tam[0] * mass_factor[0])
        self.outer_hull_pv = math.ceil(self.outer_hull_mass * 3)
        self.critical_threshold = math.ceil(self.outer_hull_mass * .3)
        return self.outer_hull_mass, self.outer_hull_pv, self.critical_threshold
        
    def inner_hull(self, inner_hull_strength: int) -> tuple[int, int, int]:
        """Calculate inner hull mass, PV"""

        mass_factor = [s['mass_factor'] for s in build_data.inner_strength_details if s['id'] == inner_hull_strength]
        self.inner_hull_mass = math.ceil(self.tam[0] * mass_factor[0])
        self.inner_hull_pv = math.ceil(self.outer_hull_mass * 3)
        return self.inner_hull_mass, self.inner_hull_pv

    def propulsion(self, thrust_points: int) -> tuple[int, int, int, int]:
        """Calculate propulsion mass, pv, max_thrust"""
        self.thrust_points = thrust_points
        self.propulsion_mass = math.ceil(thrust_points * (self.tam[0] * .07))
        self.propulsion_pv = math.ceil(self.propulsion_mass * 2)
        self.max_thrust = math.ceil(thrust_points * 1.5)
        return self.thrust_points, self.propulsion_mass, self.propulsion_pv, self.max_thrust
    
    def front_arc_weapons(self, *weapons):
        """Calculate total mass, pv, and max damage for front arc weapons"""
        front_arc_mass = []
        front_arc_pv = []
        front_arc_max_dmg = []

        if weapons[0] == '': #check for empty input
            self.front_arc_weapons_names = []
            self.total_front_arc_mass = 0
            self.total_front_arc_pv = 0
            self.total_front_arc_max_dmg = 0
        else:
            for weapon in weapons:
                weapon_mass = [w["mass"] for w in build_data.weapon_details if w["name"] == weapon]
                front_arc_mass.append(weapon_mass[0])
                
                weapon_pv = [w["pv"] for w in build_data.weapon_details if w["name"] == weapon]
                front_arc_pv.append(weapon_pv[0])
                
                weapon_max_dmg = [w["max_dmg"] for w in build_data.weapon_details if w["name"] == weapon]
                front_arc_max_dmg.append(weapon_max_dmg[0])

                name = [w["name"] for w in build_data.weapon_details if w['name'] == weapon]
                self.front_arc_weapons_names.append(name[0])
            self.total_front_arc_mass = sum(front_arc_mass)
            self.total_front_arc_pv = sum(front_arc_pv)
            self.total_front_arc_max_dmg = sum(front_arc_max_dmg)
        return self.front_arc_weapons_names, self.total_front_arc_mass, self.total_front_arc_pv, self.total_front_arc_max_dmg

    def rear_arc_weapons(self, *weapons):
        """Calculate total mass, pv, and max damage for rear arc weapons"""
        rear_arc_mass = []
        rear_arc_pv = []
        rear_arc_max_dmg = []

        if weapons[0] == '': #check for empty input
            self.rear_arc_weapons_names = []
            self.total_rear_arc_mass = 0
            self.total_rear_arc_pv = 0
            self.total_rear_arc_max_dmg = 0
        else:
            for weapon in weapons:
                weapon_mass = [w["mass"] for w in build_data.weapon_details if w["name"] == weapon]
                rear_arc_mass.append(weapon_mass[0])
                
                weapon_pv = [w["pv"] for w in build_data.weapon_details if w["name"] == weapon]
                rear_arc_pv.append(weapon_pv[0])
                
                weapon_max_dmg = [w["max_dmg"] for w in build_data.weapon_details if w["name"] == weapon]
                rear_arc_max_dmg.append(weapon_max_dmg[0])

                name = [w["name"] for w in build_data.weapon_details if w['name'] == weapon]
                self.rear_arc_weapons_names.append(name[0])
            self.total_rear_arc_mass = sum(rear_arc_mass)
            self.total_rear_arc_pv = sum(rear_arc_pv)
            self.total_rear_arc_max_dmg = sum(rear_arc_max_dmg)
        return self.rear_arc_weapons_names, self.total_rear_arc_mass, self.total_rear_arc_pv, self.total_rear_arc_max_dmg

    def right_arc_weapons(self, *weapons):
        """Calculate total mass, pv, and max damage for right arc weapons"""
        right_arc_mass = []
        right_arc_pv = []
        right_arc_max_dmg = []

        if weapons[0] == '': #check for empty input
            self.right_arc_weapons_names = []
            self.total_right_arc_mass = 0
            self.total_right_arc_pv = 0
            self.total_right_arc_max_dmg = 0
        else:
            for weapon in weapons:
                weapon_mass = [w["mass"] for w in build_data.weapon_details if w["name"] == weapon]
                right_arc_mass.append(weapon_mass[0])
                
                weapon_pv = [w["pv"] for w in build_data.weapon_details if w["name"] == weapon]
                right_arc_pv.append(weapon_pv[0])
                
                weapon_max_dmg = [w["max_dmg"] for w in build_data.weapon_details if w["name"] == weapon]
                right_arc_max_dmg.append(weapon_max_dmg[0])

                name = [w["name"] for w in build_data.weapon_details if w['name'] == weapon]
                self.right_arc_weapons_names.append(name[0])
            self.total_right_arc_mass = sum(right_arc_mass)
            self.total_right_arc_pv = sum(right_arc_pv)
            self.total_right_arc_max_dmg = sum(right_arc_max_dmg)
        return self.right_arc_weapons_names, self.total_right_arc_mass, self.total_right_arc_pv, self.total_right_arc_max_dmg

    def left_arc_weapons(self, *weapons):
        """Calculate total mass, pv, and max damage for rear arc weapons"""
        left_arc_mass = []
        left_arc_pv = []
        left_arc_max_dmg = []

        if weapons[0] == '': #check for empty input
            self.left_arc_weapons_names = []
            self.total_left_arc_mass = 0
            self.total_left_arc_pv = 0
            self.total_left_arc_max_dmg = 0
        else:
            for weapon in weapons:
                weapon_mass = [w["mass"] for w in build_data.weapon_details if w["name"] == weapon]
                left_arc_mass.append(weapon_mass[0])
                
                weapon_pv = [w["pv"] for w in build_data.weapon_details if w["name"] == weapon]
                left_arc_pv.append(weapon_pv[0])
                
                weapon_max_dmg = [w["max_dmg"] for w in build_data.weapon_details if w["name"] == weapon]
                left_arc_max_dmg.append(weapon_max_dmg[0])

                name = [w["name"] for w in build_data.weapon_details if w['name'] == weapon]
                self.left_arc_weapons_names.append(name[0])
            self.total_left_arc_mass = sum(left_arc_mass)
            self.total_left_arc_pv = sum(left_arc_pv)
            self.total_left_arc_max_dmg = sum(left_arc_max_dmg)
        return self.left_arc_weapons_names, self.total_left_arc_mass, self.total_left_arc_pv, self.total_left_arc_max_dmg

    def equipment(self, *items) -> tuple[int, int, int, str]:
        """Calculate total equipment mass, total equipment pv and generate string list of equipment names"""
        all_item_mass = []
        all_item_pv = []
        for item in items:
            mass_factor = [s['mass_factor'] for s in build_data.equipment_details if s['id'] == item]
            item_mass = math.ceil(self.total_equipment_mass + (self.tam[0] * mass_factor[0]))
            all_item_mass.append(item_mass)
            
            pv_factor = [s['pv_factor'] for s in build_data.equipment_details if s['id'] == item]
            item_pv = math.ceil(self.total_equipment_pv + (self.total_equipment_mass * pv_factor[0]))
            all_item_pv.append(item_pv)
            
            name = [s["name"] for s in build_data.equipment_details if s['id'] == item]
            self.equipment_names.append(name[0])
        self.total_equipment_mass = sum(all_item_mass)
        self.total_equipment_pv = sum(all_item_pv)
        return self.total_equipment_mass, self.total_equipment_pv, self.equipment_names
    
    def set_quality(self, crew_quality: int) -> tuple[int, int]:
        """Calculate final PV and retrieve Max Stress"""
        self.crew_quality = crew_quality
        self.crew_quality_str = [s['name'] for s in build_data.crew_quality_details if s['id'] == crew_quality]
        self.track_base_pv()
        self.pv_factor = [s['pv_factor'] for s in build_data.crew_quality_details if s['id'] == crew_quality]
        self.final_pv = math.ceil(self.total_base_pv * self.pv_factor[0])
        self.max_stress = [s['max_stress'] for s in build_data.crew_quality_details if s['id'] == crew_quality]
        self.max_stress = self.max_stress[0]
        self.crew_quality_str = self.crew_quality_str[0]
        return self.crew_quality_str, self.final_pv, self.max_stress

    def track_mass(self) -> tuple[int, int, int]:
        """Calculate current mass, mass distance from TAM, and bool for if TAM exceeded"""
        self.total_mass = (self.outer_hull_mass + self.inner_hull_mass + self.propulsion_mass + self.total_equipment_mass
            + self.total_front_arc_mass + self.total_rear_arc_mass + self.total_right_arc_mass + self.total_left_arc_mass)
        self.mass_delta = self.tam[0] - self.total_mass
        self.tam_exceeded = self.mass_delta < 0
        return self.total_mass, self.mass_delta, self.tam_exceeded
    
    def track_max_dmg(self, arc_max_dmg: int) -> tuple[int, int, int]:
        """Calculate max dmg distance from MDPA, and bool for if MDPA exceeded"""
        self.max_dmg_delta = self.mdpa[0] - arc_max_dmg
        self.mdpa_exceeded = self.max_dmg_delta < 0
        return arc_max_dmg, self.max_dmg_delta, self.mdpa_exceeded
    
    def track_base_pv(self) -> int:
        """Calculate current base PV"""
        self.total_base_pv = (self.outer_hull_pv + self.inner_hull_pv + self.propulsion_pv + self.total_equipment_pv
            + self.total_front_arc_pv + self.total_rear_arc_pv + self.total_right_arc_pv + self.total_left_arc_pv)
        return self.total_base_pv
    
    def reset_all_stats(self) -> None:
        """Reset all input and calculated stats (except for name, class, and class-contingent stats)"""
        self.weapon_names = []
        self.equipment_names = []
        self.thrust_points = 0
        self.outer_hull_mass = 0
        self.inner_hull_mass = 0
        self.propulsion_mass = 0
        self.total_equipment_mass = 0
        self.outer_hull_pv = 0
        self.inner_hull_pv = 0
        self.propulsion_pv = 0
        self.total_equipment_pv = 0