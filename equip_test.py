equipment_details = [
    {
        "id": 1,
        "name": "Long Range Sensors",
        "mass_factor": .04,
        "pv_factor": 9
    },
    {
        "id": 2,
        "name": "Agile Thruster",
        "mass_factor": .05,
        "pv_factor": 9
    }
]

total_equipment_mass = 0
tam = 30
equipment = []
equipment = [item for item in input("Select equipment (1, 2, 3, 4) separated by a comma: ").split(',')]
print(equipment)
for item in equipment:
    print(item)
    mass_factor = ([s['mass_factor'] for s in equipment_details if s['id'] == int(item)])
    total_equipment_mass += (tam * mass_factor[0])
    print(f"Mass factor: {mass_factor}")

print(f"Total Equipment mass: {total_equipment_mass}")