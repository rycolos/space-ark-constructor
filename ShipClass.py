import build_data
import math

class InvalidStrengthError(Exception):
    """
    Raised when strength selection does not match possible identifier
    """
    
    def __init__(self, value):
        message = f"ERROR: Strength value {value} is not a valid selection."
        super().__init__(message)

class InvalidEquipmentError(Exception):
    """
    Raised when equipment selection does not match possible identifiers
    """
    
    def __init__(self, value):
        message = f"ERROR: Equipment value {value} is not a valid selection."
        super().__init__(message)

class InvalidWeaponError(Exception):
    """
    Raised when weapon selection does not match possible identifiers
    """
    
    def __init__(self, value):
        message = f"ERROR: Weapon item {value} is not a valid selection."
        super().__init__(message)

class InvalidCrewQualityError(Exception):
    """
    Raised when crew quality selection does not match possible identifiers
    """
    
    def __init__(self, value):
        message = f"ERROR: Crew quality value {value} is not a valid selection."
        super().__init__(message)

class ShipClass:
    """
    Define ship class
    """
    def __init__(self, name: str, sclass: str, size: str, tam: int, armor_roll: str, mdpa: int) -> None: 
        
        #init
        self.name = name 
        self.sclass = sclass
        self.size = size
        self.tam = tam
        self.armor_roll = armor_roll
        self.mdpa = mdpa

        #inputs
        self.outer_hull_strength = 0
        self.inner_hull_strength = 0
        self.thrust_points = 0

        #outputs
        self.outer_hull_mass = 0
        self.inner_hull_mass = 0
        self.propulsion_mass = 0
        self.total_front_arc_mass = 0
        self.total_front_arc_pv = 0
        self.total_front_arc_max_dmg = 0
        self.total_rear_arc_pv = 0
        self.total_rear_arc_max_dmg = 0
        self.total_rear_arc_mass = 0
        self.total_right_arc_mass = 0
        self.total_right_arc_pv = 0
        self.total_right_arc_max_dmg = 0
        self.total_left_arc_mass = 0
        self.total_left_arc_pv = 0
        self.total_left_arc_max_dmg = 0
        self.crew_quality_str = None
        self.outer_hull_strength_str = None
        self.inner_hull_strength_str = None
        self.outer_hull_pv = 0
        self.critical_threshold = 0
        self.inner_hull_pv = 0
        self.propulsion_pv = 0
        self.max_thrust = 0
        self.total_equipment_mass = 0
        self.total_equipment_pv = 0
        self.max_stress = 0
        self.final_pv = 0
        self.total_mass = 0
        self.mass_delta = 0
        self.total_base_pv = 0

        self.equipment_list = []
        self.front_arc_weapon_list = []
        self.rear_arc_weapon_list = []
        self.right_arc_weapon_list = []
        self.left_arc_weapon_list = []
        self.ship_json_object = {}

    #OUTER HULL
    """
    When outer_hull_strength is referenced,
    setter will test and set private var to value,
    and property returns private var from public ref 
    """
    @property
    def outer_hull_strength(self):
        return self._outer_hull_strength
    
    @outer_hull_strength.setter     #validate outer hull strength input as int, 1-4
    def outer_hull_strength(self, ohs_input: int):
        ohs_ids = [i['id'] for i in build_data.outer_strength_details]
        try:
            self._outer_hull_strength = int(ohs_input) #validate integer
        except ValueError:
            raise ValueError("Error: Strength value is not an integer")
        else:
            try:
                index = ohs_ids.index(int(ohs_input)) #if integer, validate valid value
            except ValueError:
                raise InvalidStrengthError(ohs_input)
            
    def outer_hull(self, ohs_input: int) -> tuple[int, int, int, int]:
        """
        Calculate outer hull mass, PV, critical threshold from strength integer ID selection
        """
        self.outer_hull_strength = ohs_input
        self.outer_hull_strength_str = [s['name'] for s in build_data.outer_strength_details if s['id'] == self.outer_hull_strength]
        mass_factor = [s['mass_factor'] for s in build_data.outer_strength_details if s['id'] == self.outer_hull_strength]
        self.outer_hull_mass = math.ceil(self.tam * mass_factor[0])
        self.outer_hull_pv = math.ceil(self.outer_hull_mass * 3)
        self.critical_threshold = math.ceil(self.outer_hull_mass * .3)
        return self.outer_hull_strength, self.outer_hull_strength_str, self.outer_hull_mass, self.outer_hull_pv, self.critical_threshold

    #INNER HULL
    """
    When inner_hull_strength is referenced,
    setter will test and set private var to value,
    and property returns private var from public ref 
    """
    @property
    def inner_hull_strength(self):
        return self._inner_hull_strength
    
    @inner_hull_strength.setter     #validate inner hull strength input
    def inner_hull_strength(self, ihs_input: int):
        ihs_ids = [i['id'] for i in build_data.inner_strength_details]
        try:
            self._inner_hull_strength = int(ihs_input) #validate integer
        except ValueError:
            raise ValueError("Error: Strength value is not an integer")
        else:
            try:
                index = ihs_ids.index(int(ihs_input)) #validate valid value
            except ValueError:
                raise InvalidStrengthError(ihs_input)
    
    def inner_hull(self, ihs_input: int) -> tuple[int, int, int, int]:
        """
        Calculate inner hull mass, PV from strength integer ID selection
        """
        self.inner_hull_strength = ihs_input
        self.inner_hull_strength_str = [s['name'] for s in build_data.inner_strength_details if s['id'] == self.inner_hull_strength]
        mass_factor = [s['mass_factor'] for s in build_data.inner_strength_details if s['id'] == self.inner_hull_strength]
        self.inner_hull_mass = math.ceil(self.tam * mass_factor[0])
        self.inner_hull_pv = math.ceil(self.outer_hull_mass * 3)
        return self.inner_hull_strength_str, self.inner_hull_strength, self.inner_hull_mass, self.inner_hull_pv

    #PROPULSION
    """
    When thrust_points is referenced,
    setter will test and set private var to value,
    and property returns private var from public ref 
    """
    @property
    def thrust_points(self):
        return self._thrust_points
    
    @thrust_points.setter     #validate thrust point input
    def thrust_points(self, tp_input: int):
        try:
            self._thrust_points = int(tp_input)
        except ValueError:
            raise ValueError("Error: Thrust Points value is not an integer")
    
    def propulsion(self, tp_input: int) -> tuple[int, int, int, int]:
        """
        Calculate propulsion mass, pv, max_thrust from thrust points input
        """
        self.thrust_points = tp_input
        self.propulsion_mass = math.ceil(self.thrust_points * (self.tam * .07))
        self.propulsion_pv = math.ceil(self.propulsion_mass * 2)
        self.max_thrust = math.ceil(self.thrust_points * 1.5)
        return self.thrust_points, self.max_thrust, self.propulsion_mass, self.propulsion_pv

    #WEAPONS
    def front_arc_weapons(self, *weapons: list) -> tuple[int, int, int]:
        """
        Add front arc weapon lookup data to weapons dict
        Calculate total arc mass, pv, max dmg for final ship calculations
        """
        if weapons[0] == '': #check for empty input
            self.total_front_arc_mass = 0
            self.total_front_arc_pv = 0
            self.total_front_arc_max_dmg = 0
        else:
            for weapon in weapons:
                try:
                    index = [i["name"] for i in build_data.weapon_details].index(weapon) #catch if item not in possible weapon names
                except ValueError:
                    raise InvalidWeaponError(weapon)
                
                weapon_item = [w for w in build_data.weapon_details if w["name"] == weapon]
                self.front_arc_weapon_list.append(weapon_item[0])
        self.total_front_arc_mass = sum([w["mass"] for w in self.front_arc_weapon_list])
        self.total_front_arc_pv = sum([w["pv"] for w in self.front_arc_weapon_list])
        self.total_front_arc_max_dmg = sum([w["max_dmg"] for w in self.front_arc_weapon_list])
    
        return self.total_front_arc_mass, self.total_front_arc_pv, self.total_front_arc_max_dmg

    def rear_arc_weapons(self, *weapons: list) -> tuple[int, int, int]:
        """
        Add rear arc weapon lookup data to weapons dict
        Calculate total arc mass, pv, max dmg for final ship calculations
        """
        if weapons[0] == '': #check for empty input
            self.total_rear_arc_mass = 0
            self.total_rear_arc_pv = 0
            self.total_rear_arc_max_dmg = 0
        else:
            for weapon in weapons:
                try:
                    index = [i["name"] for i in build_data.weapon_details].index(weapon) #catch if item not in possible weapon names
                except ValueError:
                    raise InvalidWeaponError(weapon)                
                
                weapon_item = [w for w in build_data.weapon_details if w["name"] == weapon]
                self.rear_arc_weapon_list.append(weapon_item[0])
        self.total_rear_arc_mass = sum([w["mass"] for w in self.rear_arc_weapon_list])
        self.total_rear_arc_pv = sum([w["pv"] for w in self.rear_arc_weapon_list])
        self.total_rear_arc_max_dmg = sum([w["max_dmg"] for w in self.rear_arc_weapon_list])
        return self.total_rear_arc_mass, self.total_rear_arc_pv, self.total_rear_arc_max_dmg

    def right_arc_weapons(self, *weapons: list) -> tuple[int, int, int]:
        """
        Add right arc weapon lookup data to weapons dict
        Calculate total arc mass, pv, max dmg for final ship calculations
        """        
        if weapons[0] == '': #check for empty input
            self.total_right_arc_mass = 0
            self.total_right_arc_pv = 0
            self.total_right_arc_max_dmg = 0
        else:
            for weapon in weapons:
                try:
                    index = [i["name"] for i in build_data.weapon_details].index(weapon) #catch if item not in possible weapon names
                except ValueError:
                    raise InvalidWeaponError(weapon)
                
                weapon_item = [w for w in build_data.weapon_details if w["name"] == weapon]
                self.right_arc_weapon_list.append(weapon_item[0])
        self.total_right_arc_mass = sum([w["mass"] for w in self.right_arc_weapon_list])
        self.total_right_arc_pv = sum([w["pv"] for w in self.right_arc_weapon_list])
        self.total_right_arc_max_dmg = sum([w["max_dmg"] for w in self.right_arc_weapon_list])
        return self.total_right_arc_mass, self.total_right_arc_pv, self.total_right_arc_max_dmg

    def left_arc_weapons(self, *weapons: list) -> tuple[int, int, int]:
        """
        Add left arc weapon lookup data to weapons dict
        Calculate total arc mass, pv, max dmg for final ship calculations
        """        
        if weapons[0] == '': #check for empty input
            self.total_left_arc_mass = 0
            self.total_left_arc_pv = 0
            self.total_left_arc_max_dmg = 0
        else:
            for weapon in weapons:
                try:
                    index = [i["name"] for i in build_data.weapon_details].index(weapon) #catch if item not in possible weapon names
                except ValueError:
                    raise InvalidWeaponError(weapon)

                weapon_item = [w for w in build_data.weapon_details if w["name"] == weapon]
                self.left_arc_weapon_list.append(weapon_item[0])
        self.total_left_arc_mass = sum([w["mass"] for w in self.left_arc_weapon_list])
        self.total_left_arc_pv = sum([w["pv"] for w in self.left_arc_weapon_list])
        self.total_left_arc_max_dmg = sum([w["max_dmg"] for w in self.left_arc_weapon_list])
        return self.total_left_arc_mass, self.total_left_arc_pv, self.total_left_arc_max_dmg
    
    #EQUIPMENT
    def equipment(self, *items: list) -> tuple[dict, int, int]:
        """
        Generate equipment dict that is a list with a dict per item, adding calculated item mass and pv
        Calculate total equipment mass, total equipment pv for final ship calculations
        """
        all_item_mass = []
        all_item_pv = []
        items_int = []

        for item in items: #catch if input is not an integer
            try:
                items_int.append(int(item))
            except ValueError:
                raise ValueError(f"ERROR: Equipment entry {item} is not an integer.")

        for item in items_int:
            try:
                index = [i['id'] for i in build_data.equipment_details].index(item) #catch if item not in possible equipment IDs
            except ValueError:
                raise InvalidEquipmentError(item)

            equipment_item = {"name": "", "description": "", "mass": None, "pv": None}

            name = [s["name"] for s in build_data.equipment_details if s['id'] == item]
            equipment_item["name"] = name[0]

            description = [s["description"] for s in build_data.equipment_details if s['id'] == item]
            equipment_item["description"] = description[0]

            mass_factor = [s['mass_factor'] for s in build_data.equipment_details if s['id'] == item]
            item_mass = math.ceil(self.total_equipment_mass + (self.tam * mass_factor[0]))
            equipment_item["mass"] = item_mass
            all_item_mass.append(item_mass)

            pv_factor = [s['pv_factor'] for s in build_data.equipment_details if s['id'] == item]
            item_pv = math.ceil(item_mass * pv_factor[0])
            equipment_item["pv"] = item_pv
            all_item_pv.append(item_pv)
            
            self.equipment_list.append(equipment_item)
        self.total_equipment_mass = sum(all_item_mass)
        self.total_equipment_pv = sum(all_item_pv)
        return self.total_equipment_mass, self.total_equipment_pv
    
    #CREW QUALITY
    """
    When crew_quality is referenced,
    setter will test and set private var to value,
    and property returns private var from public ref 
    """
    @property
    def crew_quality(self):
        return self._crew_quality
    
    @crew_quality.setter     #validate outer hull strength input as int, 1-4
    def crew_quality(self, cq_input: int):
        cq_ids = [i['id'] for i in build_data.crew_quality_details]
        try:
            self._crew_quality = int(cq_input) #validate integer
        except ValueError:
            raise ValueError("Error: Crew Quality value is not an integer")
        else:
            try:
                index = cq_ids.index(int(cq_input)) #if integer, validate valid value
            except ValueError:
                raise InvalidCrewQualityError(cq_input)

    def set_quality(self, cq_input: int) -> tuple[int, int]:
        """
        Calculate final PV and retrieve Max Stress from Crew Quality ID input
        """
        self.crew_quality = cq_input
        self.crew_quality_str = [s['name'] for s in build_data.crew_quality_details if s['id'] == self.crew_quality]
        self.track_base_pv()
        self.pv_factor = [s['pv_factor'] for s in build_data.crew_quality_details if s['id'] == self.crew_quality]
        self.final_pv = math.ceil(self.total_base_pv * self.pv_factor[0])
        self.max_stress = [s['max_stress'] for s in build_data.crew_quality_details if s['id'] == self.crew_quality]
        self.max_stress = self.max_stress[0]
        self.crew_quality_str = self.crew_quality_str[0]
        return self.crew_quality_str, self.final_pv, self.max_stress

    #HELPER FUNCTIONS
    def track_mass(self) -> tuple[int, int, int]:
        """
        Calculate current mass, mass distance from TAM, and bool for if TAM exceeded
        """
        self.total_mass = (self.outer_hull_mass + self.inner_hull_mass + self.propulsion_mass + self.total_equipment_mass
            + self.total_front_arc_mass + self.total_rear_arc_mass + self.total_right_arc_mass + self.total_left_arc_mass)
        self.mass_delta = self.tam - self.total_mass
        self.tam_exceeded = self.mass_delta < 0
        return self.total_mass, self.mass_delta, self.tam_exceeded
    
    def track_max_dmg(self, arc_max_dmg: int) -> tuple[int, int, int]:
        """
        Calculate max dmg distance from MDPA, and bool for if MDPA exceeded
        """
        self.max_dmg_delta = self.mdpa - arc_max_dmg
        self.mdpa_exceeded = self.max_dmg_delta < 0
        return arc_max_dmg, self.max_dmg_delta, self.mdpa_exceeded
    
    def track_base_pv(self) -> int:
        """
        Calculate current base PV
        """
        self.total_base_pv = (self.outer_hull_pv + self.inner_hull_pv + self.propulsion_pv + self.total_equipment_pv
            + self.total_front_arc_pv + self.total_rear_arc_pv + self.total_right_arc_pv + self.total_left_arc_pv)
        return self.total_base_pv
    
    def build_json_objects(self):
        """
        Construct JSON object of ship
        """
        self.ship_json_object = {
            "name": self.name,
            "ship_class": self.sclass,
            "size": self.size,
            "TAM": self.tam,
            "mass": self.total_mass,
            "armor_roll": self.armor_roll,
            "MDPA": self.mdpa,
            "crew_quality": self.crew_quality_str,
            "base_pv": self.total_base_pv,
            "final_pv": self.final_pv,
            "max_stress": self.max_stress,
            "armor": {
                "outer_hull": {
                    "strength": self.outer_hull_strength_str,
                    "mass": self.outer_hull_mass,
                    "pv": self.outer_hull_pv
                },
                "inner_hull": {
                    "strength": self.inner_hull_strength_str,
                    "mass": self.inner_hull_mass,
                    "pv": self.inner_hull_pv
                },
                "critical_threshold": self.critical_threshold
                },
            "propulsion": {
                "thrust_points": self.thrust_points,
                "max_thrust": self.max_thrust,
                "propulsion_mass": self.propulsion_mass,
                "propulsion_pv": self.propulsion_pv
            },
            "equipment": {
                "equipment_items": self.equipment_list,
                "total_equipment_mass": self.total_equipment_mass,
                "total_equipment_pv": self.total_equipment_pv
            },
            "weapons": {
                "front_arc_weapons": self.front_arc_weapon_list,
                "total_front_arc_mass": self.total_front_arc_mass,
                "total_front_arc_pv": self.total_front_arc_pv,
                "total_front_arc_max_dmg": self.total_front_arc_max_dmg,
                "rear_arc_weapons": self.rear_arc_weapon_list,
                "total_rear_arc_mass": self.total_rear_arc_mass,
                "total_rear_arc_pv": self.total_rear_arc_pv,
                "total_rear_arc_max_dmg": self.total_rear_arc_max_dmg,
                "right_arc_weapons": self.right_arc_weapon_list,
                "total_right_arc_mass": self.total_right_arc_mass,
                "total_right_arc_pv": self.total_right_arc_pv,
                "total_right_arc_max_dmg": self.total_right_arc_max_dmg,
                "left_arc_weapons": self.left_arc_weapon_list,
                "total_left_arc_mass": self.total_left_arc_mass,
                "total_left_arc_pv": self.total_left_arc_pv,
                "total_left_arc_max_dmg": self.total_left_arc_max_dmg
            }
        }

    def reset_all_stats(self) -> None:
        """
        Reset all input and calculated stats (except for name, class, and class-contingent stats)
        """

        self.total_front_arc_mass = 0
        self.total_front_arc_pv = 0
        self.total_front_arc_max_dmg = 0

        self.total_rear_arc_mass = 0
        self.total_rear_arc_pv = 0
        self.total_rear_arc_max_dmg = 0

        self.total_right_arc_mass = 0
        self.total_right_arc_pv = 0
        self.total_right_arc_max_dmg = 0

        self.total_left_arc_mass = 0
        self.total_left_arc_pv = 0
        self.total_left_arc_max_dmg = 0

        self.crew_quality_str = None
        
        self.propulsion_mass = 0
        self.propulsion_pv = 0
        self.thrust_points = 0
        self.max_thrust = 0

        self.outer_hull_mass = 0
        self.outer_hull_pv = 0
        self.critical_threshold = 0

        self.inner_hull_mass = 0
        self.inner_hull_pv = 0
        
        self.total_equipment_mass = 0
        self.total_equipment_pv = 0
        
        self.max_stress = 0
        self.final_pv = 0
        self.total_mass = 0

        self.equipment_list = []
        self.front_arc_weapon_list = []
        self.rear_arc_weapon_list = []
        self.right_arc_weapon_list = []
        self.left_arc_weapon_list = []
        self.ship_json_object = {}