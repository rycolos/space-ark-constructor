import build_data

class ShipClass:
    def __init__(self, name: str, sclass: str, size: str, tam: int, armor_roll: str, mdpa: int) -> None: 
        
        self.name = name 
        self.sclass = sclass
        self.size = size
        self.tam = tam
        self.armor_roll = armor_roll
        self.mdpa = mdpa

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
        self.outer_hull_mass = round(self.tam[0] * mass_factor[0])
        self.outer_hull_pv = round(self.outer_hull_mass * 3)
        self.critical_threshold = round(self.outer_hull_mass * .3)
        return self.outer_hull_mass, self.outer_hull_pv, self.critical_threshold
        
    def inner_hull(self, inner_hull_strength: int) -> tuple[int, int, int]:
        """Calculate inner hull mass, PV"""

        mass_factor = [s['mass_factor'] for s in build_data.inner_strength_details if s['id'] == inner_hull_strength]
        self.inner_hull_mass = round(self.tam[0] * mass_factor[0])
        self.inner_hull_pv = round(self.outer_hull_mass * 3)
        return self.inner_hull_mass, self.inner_hull_pv

    def propulsion(self, thrust_points: int) -> tuple[int, int, int, int]:
        """Calculate propulsion mass, pv, max_thrust"""
        self.thrust_points = thrust_points
        self.propulsion_mass = round(thrust_points * (self.tam[0] * .07))
        self.propulsion_pv = round(self.propulsion_mass * 2)
        self.max_thrust = round(thrust_points * 1.5)
        return self.thrust_points, self.propulsion_mass, self.propulsion_pv, self.max_thrust
    
    def weapons(self):
        #per arc - arc has weapon list (by id), total damage, total mass, total pv
            #check max damage
        #all weapons - total mass, total pv
            #check mass
        ...

    def equipment(self, *items) -> tuple[int, int, int, str]:
        """Calculate total equipment mass, total equipment pv and generate string list of equipment names"""
        all_item_mass = []
        all_item_pv = []
        for item in items:
            mass_factor = [s['mass_factor'] for s in build_data.equipment_details if s['id'] == item]
            item_mass = round(self.total_equipment_mass + (self.tam[0] * mass_factor[0]))
            all_item_mass.append(item_mass)
            
            pv_factor = [s['pv_factor'] for s in build_data.equipment_details if s['id'] == item]
            item_pv = round(self.total_equipment_pv + (self.total_equipment_mass * pv_factor[0]))
            all_item_pv.append(item_pv)
            
            name = [s["name"] for s in build_data.equipment_details if s['id'] == item]
            self.equipment_names.append(name[0])
        self.total_equipment_mass = sum(all_item_mass)
        self.total_equipment_pv = sum(all_item_pv)
        return self.total_equipment_mass, self.total_equipment_pv, self.equipment_names
    
    # def fixed_cost(self):
    #     self.fixed_cost_mass = round(self.tam[0] * .03)
    #     self.fixed_cost_pv = round(self.fixed_cost_mass * 2)
    #     return self.fixed_cost_mass, self.fixed_cost_pv
    
    def set_quality(self, crew_quality: int) -> tuple[int, int]:
        """Calculate final PV and retrieve Max Stress"""
        self.crew_quality = crew_quality
        self.track_base_pv()
        self.pv_factor = [s['pv_factor'] for s in build_data.crew_quality_details if s['id'] == crew_quality]
        self.final_pv = round(self.total_base_pv * self.pv_factor[0])
        self.max_stress = [s['max_stress'] for s in build_data.crew_quality_details if s['id'] == crew_quality]
        self.max_stress = self.max_stress[0]
        return self.final_pv, self.max_stress

    def track_mass(self) -> tuple[int, int, int]:
        """Calculate current mass, mass distance from TAM, and bool for if TAM exceeded"""
        self.total_mass = self.outer_hull_mass + self.inner_hull_mass + self.propulsion_mass + self.total_equipment_mass #+ self.fixed_cost_mass
        self.mass_delta = self.tam[0] - self.total_mass
        self.tam_exceeded = self.mass_delta < 0
        return self.total_mass, self.mass_delta, self.tam_exceeded
    
    def track_base_pv(self) -> int:
        """Calculate current base PV"""
        self.total_base_pv = self.outer_hull_pv + self.inner_hull_pv + self.propulsion_pv + self.total_equipment_pv #+ self.fixed_cost_pv
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