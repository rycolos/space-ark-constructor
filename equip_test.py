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

def equipment_curr(equipment_list):
    total_equipment_mass = 0
    tam = 30
    equipment_names = []

    for item in equipment_list:
        mass_factor = ([s['mass_factor'] for s in equipment_details if s['id'] == int(item)])
        total_equipment_mass += (tam * mass_factor[0])
        equipment_names.append([s['name'] for s in equipment_details if s['id'] == int(item)])
        equipment_description = ', '.join([item for items in equipment_names for item in items]) 
    return total_equipment_mass, equipment_names, equipment_description

def equipment_args(*args):
    total_equipment_mass = 0
    tam = 30
    equipment_names = []

    for item in args:
        #print(item)
        mass_factor = [s['mass_factor'] for s in equipment_details if s['id'] == item]
        total_equipment_mass += (tam * mass_factor[0])
        equipment_names.append([s['name'] for s in equipment_details if s['id'] == item])
        equipment_description = ', '.join([item for items in equipment_names for item in items]) 
    return total_equipment_mass, equipment_names, equipment_description

#equipment_list = [int(item) for item in input("Select equipment (1, 2, 3, 4) separated by a comma: ").split(',')]
# equipment_list = input("Select equipment (1, 2, 3, 4) separated by a comma: ")
# print(f"You input: {equipment_list}")
# print(type(equipment_list))

equipment_list2 = list(map(int, input("Select equipment (1, 2, 3, 4) separated by a comma: ").split(', ')))
print(f"You input: {equipment_list2}")
print(type(equipment_list2))
# total_equipment_mass, equipment_names, equipment_description = equipment_curr(equipment_list)

total_equipment_mass, equipment_names, equipment_description = equipment_args(*equipment_list2)
#total_equipment_mass, equipment_names, equipment_description = equipment_args(1, 2)

print(f"Total Equipment mass: {total_equipment_mass}")
print(f"Equipment names: {equipment_names}")
print(f"Equipment description: {equipment_description}")
#print(*equipment_names)

