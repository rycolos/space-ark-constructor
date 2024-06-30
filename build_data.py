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
    }
)

equipment_details = (
    {
        "id": 1,
        "name": "None",
        "mass_factor": 0,
        "pv_factor": 0
    },
    {
        "id": 2,
        "name": "Long Range Sensors",
        "mass_factor": .04,
        "pv_factor": 9
    },
    {
        "id": 3,
        "name": "Agile Thrusters",
        "mass_factor": .05,
        "pv_factor": 9
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
        "name": "Light Laser",
        "max_dmg": 2,
        "mass": 2,
        "pv": 6
    },
    {
        "name": "Medium Laser",
        "max_dmg": 4,
        "mass": 4,
        "pv": 12
    }

)