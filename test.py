import eppy
from Obj_Structure import Obj_Tree
from eppy.modeleditor import IDF
from eppy import hvacbuilder
from Helper import delete_hvac_objs
from Helper import SomeFields

idd_file = 'Data/Energy+.idd'
try:
    IDF.setiddname(idd_file)
except eppy.modeleditor.IDDAlreadySetError as e:
    pass

# file_path = 'Data/CIB-Office.idf'
file_path = 'Data/TestOffice.idf'

my_model = IDF(file_path)
# my_model.printidf()

all_objs = my_model.idfobjects
# print(all_objs.keys())
# bldg = all_objs['BUILDING'][0]
# print(bldg.Name)
# print(bldg.North_Axis)

# zones = all_objs['Sizing:System']
# print(zones)
# print(len(zones))

# Get all setpoint managers:
#####################################################################
# all_spms = all_objs['SetpointManager:MixedAir'.upper()]
# print(all_spms)

# Deleting existing defined objects:
#####################################################################
delete_hvac_objs(my_model)

# all_plantloop = all_objs['Chiller:Electric:EIR'.upper()]
# print(all_plantloop)

# Creating new object:
#####################################################################
# new_zone = my_model.newidfobject('Zone')
# print(new_zone)

# airloop = my_model.newidfobject('AirLoopHVAC')
# print(airloop)

# Creating new plant loop:
#####################################################################
loop_configs = {
    'Name': 'my_plant_loop',
    'Maximum_Loop_Temperature': 20,
}
newplantloop = my_model.newidfobject('PlantLoop', **loop_configs)
# print(newplantloop)
fields = SomeFields.p_fields
flnames = [field.replace(" ", "_") for field in fields]
fields1 = [field.replace("Plant Side", "Supply") for field in fields]
fields1 = [field.replace("Demand Side", "Demand") for field in fields1]
fields1 = [field[: field.find("Name") - 1] for field in fields1]
fields1 = [field.replace(" Node", "") for field in fields1]
fields1 = [field.replace(" List", "s") for field in fields1]

fieldnames = ["%s %s" % ('my_plant_loop', field) for field in fields1]

for fieldname, thefield in zip(fieldnames, flnames):
        newplantloop[thefield] = fieldname

print(newplantloop)

# make the branch lists for this plant loop
sbranchlist = my_model.newidfobject("BRANCHLIST", Name=newplantloop.Plant_Side_Branch_List_Name)
dbranchlist = my_model.newidfobject("BRANCHLIST", Name=newplantloop.Demand_Side_Branch_List_Name)

# add branch names to the branchlist


# # Get all plant loops:
# all_plantloop = all_objs['PlantLoop'.upper()]
# all_plantloop[1].Maximum_Loop_Temperature = 25
# print(all_plantloop)


# Save to a new file:
#####################################################################
# my_model.saveas('Data/TestOffice_empty.idf')
