sclass_details = (
    {
        "sclass": "FRIGATE",
        "size": "Small",
        "tam": 30,
        "armor_roll": "3+",
        "mdpa": 9
    },
    {
        "sclass": "DESTROYER",
        "size": "Small",
        "tam": 40,
        "armor_roll": "3+",
        "mdpa": 12
    },
    {
        "sclass": "HEAVY DESTROYER",
        "size": "Medium",
        "tam": 50,
        "armor_roll": "4+",
        "mdpa": 15
    },
    {
        "sclass": "LIGHT CRUISER",
        "size": "Medium",
        "tam": 60,
        "armor_roll": "4+",
        "mdpa": 18
    },
    {
        "sclass": "CRUISER",
        "size": "Large",
        "tam": 70,
        "armor_roll": "4+",
        "mdpa": 21
    },
    {
        "sclass": "BATTLECRUISER",
        "size": "Large",
        "tam": 90,
        "armor_roll": "5+",
        "mdpa": 27
    },
    {
        "sclass": "BATTLESHIP",
        "size": "Large",
        "tam": 110,
        "armor_roll": "5+",
        "mdpa": 33
    },
    {
        "sclass": "DREADNOUGHT",
        "size": "Large",
        "tam": 130,
        "armor_roll": "5+",
        "mdpa": 39
    },
    {
        "sclass": "SUPER DREADNOUGHT",
        "size": "Large",
        "tam": 150,
        "armor_roll": "5+",
        "mdpa": 45
    }
)

equipment_details = (
    {
        "id": 1,
        "name": "None",
        "mass_factor": 0,
        "pv_factor": 0,
        "description": None
    },
    {
        "id": 2,
        "name": "Long Range Sensors",
        "mass_factor": .04,
        "pv_factor": 9,
        "description": "Range brackets increase by 2 hexes"
    },
    {
        "id": 3,
        "name": "Agile Thrusters",
        "mass_factor": .05,
        "pv_factor": 9,
        "description": "No minimum 1 hex forward move is required before making a facing change"
    },
    {
        "id": 4,
        "name": "Enhanced Engineering",
        "mass_factor": .05,
        "pv_factor": 10,
        "description": "Apply a -1 modifier on Damage Control rolls"
    },
    {
        "id": 5,
        "name": "Advanced Fire Control",
        "mass_factor": .05,
        "pv_factor": 10,
        "description": "Ignore To Hit modifiers for targeting additional ships"
    },
    {
        "id": 6,
        "name": "Target Designator",
        "mass_factor": .04,
        "pv_factor": 12,
        "description": "After this ship has successfully attacked a target, friendly ships that attack the same target get -1 on their To Hit rolls against that target on the same turn. Can only be used against one target per turn, per ship with this equipment"
    }
)

outer_strength_details = (
    {
        "id": 1,
        "name": "Light",
        "mass_factor": .2
    },
    {
        "id": 2,
        "name": "Average",
        "mass_factor": .25
    },
    {
        "id": 3,
        "name": "Heavy",
        "mass_factor": .3
    },
    {
        "id": 4,
        "name": "Ultra Heavy",
        "mass_factor": .35
    }
)

inner_strength_details = (
    {
        "id": 1,
        "name": "Light",
        "mass_factor": .05
    },
    {
        "id": 2,
        "name": "Average",
        "mass_factor": .1
    },
    {
        "id": 3,
        "name": "Heavy",
        "mass_factor": .15
    },
    {
        "id": 4,
        "name": "Ultra Heavy",
        "mass_factor": .20
    }
)

crew_quality_details = (
    {
        "id": 1,
        "name": "Recruit",
        "pv_factor": .8,
        "max_stress": 6 
    },
    {
        "id": 2,
        "name": "Regular",
        "pv_factor": 1,
        "max_stress": 7 
    },
    {
        "id": 3,
        "name": "Veteran",
        "pv_factor": 1.2,
        "max_stress": 8 
    }
)

weapon_details = (
    {
        "name": "LIGHT LASER",
        "max_dmg": 2,
        "mass": 2,
        "pv": 6,
        "attack": 3,
        "damage": 1,
        "range": "8/13/18/23",
        "special": None
    },
    {
        "name": "MEDIUM LASER",
        "max_dmg": 4,
        "mass": 4,
        "pv": 12,
        "attack": 3,
        "damage": 2,
        "range": "8/14/20/25",
        "special": None
    },
    {
        "name": "HEAVY LASER",
        "max_dmg": 6,
        "mass": 5,
        "pv": 15,
        "attack": 3,
        "damage": 3,
        "range": "9/15/21/27",
        "special": None
    },
    {
        "name": "PULSE LASER",
        "max_dmg": 8,
        "mass": 12,
        "pv": 36,
        "attack": 5,
        "damage": 2,
        "range": "8/14/20/25",
        "special": "RPT"
    },
    {
        "name": "LIGHT PPC",
        "max_dmg": 3,
        "mass": 4,
        "pv": 12,
        "attack": 4,
        "damage": 1,
        "range": "8/13/18/23",
        "special": "PEN1"
    },
    {
        "name": "MEDIUM PPC",
        "max_dmg": 6,
        "mass": 9,
        "pv": 27,
        "attack": 4,
        "damage": 2,
        "range": "8/14/20/25",
        "special": "PEN2"
    },
    {
        "name": "HEAVY PPC",
        "max_dmg": 9,
        "mass": 13,
        "pv": 39,
        "attack": 4,
        "damage": 3,
        "range": "9/15/21/27",
        "special": "PEN3"
    },
    {
        "name": "LIGHT NAVEL AUTOCANNON",
        "max_dmg": 8,
        "mass": 12,
        "pv": 36,
        "attack": 5,
        "damage": 2,
        "range": "8/13/18/23",
        "special": "RPT"
    },
    {
        "name": "MEDIUM NAVEL AUTOCANNON",
        "max_dmg": 12,
        "mass": 15,
        "pv": 45,
        "attack": 5,
        "damage": 3,
        "range": "8/11/16/21",
        "special": "RPT"
    },
    {
        "name": "HEAVY NAVEL AUTOCANNON",
        "max_dmg": 16,
        "mass": 18,
        "pv": 54,
        "attack": 5,
        "damage": 4,
        "range": "7/11/15/19",
        "special": "RPT"
    },
    {
        "name": "LIGHT GAUSS",
        "max_dmg": 12,
        "mass": 13,
        "pv": 39,
        "attack": 5,
        "damage": 3,
        "range": "8/14/20/25",
        "special": "PEN2"
    },
    {
        "name": "MEDIUM GAUSS",
        "max_dmg": 16,
        "mass": 18,
        "pv": 54,
        "attack": 5,
        "damage": 4,
        "range": "8/13/18/23",
        "special": "PEN3"
    },
    {
        "name": "HEAVY GAUSS",
        "max_dmg": 20,
        "mass": 23,
        "pv": 69,
        "attack": 5,
        "damage": 5,
        "range": "8/11/16/21",
        "special": "PEN4"
    },
    {
        "name": "NAVAL MASS DRIVER",
        "max_dmg": 28,
        "mass": 42,
        "pv": 126,
        "attack": 3,
        "damage": 15,
        "range": "7/10/14/17",
        "special": "AM2, MASS"
    },
    {
        "name": "MISSILE CLUSTER - SMALL",
        "max_dmg": 10,
        "mass": 8,
        "pv": 24,
        "attack": 6,
        "damage": 2,
        "range": "8/14/20/25",
        "special": "SCT, AM4"
    },
    {
        "name": "MISSILE CLUSTER - LARGE",
        "max_dmg": 15,
        "mass": 12,
        "pv": 36,
        "attack": 6,
        "damage": 3,
        "range": "9/15/21/27",
        "special": "SCT, AM4"
    },
    {
        "name": "MK49 GUIDED TORPEDO",
        "max_dmg": 12,
        "mass": 10,
        "pv": 30,
        "attack": 1,
        "damage": 12,
        "range": "9/15/21/27",
        "special": "GUI, AM4"
    }
)