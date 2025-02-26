import eppy
from eppy.modeleditor import IDF
from Helper import delete_hvac_objs, set_always_on, sort_zone_by_condition, sort_zone_by_name
from Helper import sort_zone_by_floor_1, sort_zone_by_floor_2, sort_zone_by_floor_4
from HVACSystem.AirLoop import AirLoop
from HVACSystem.VRF import VRF

# idd_file = 'Data/Energy+_v22.idd'
idd_file = 'Data/Energy+_v24.idd'
try:
    IDF.setiddname(idd_file)
except eppy.modeleditor.IDDAlreadySetError as e:
    pass

# file_path = 'Data/CIB-Office.idf'
# file_path = 'Data/TestOffice.idf'
# file_path = 'Data/SmallOffice_CentralDOAS.idf'
file_path = 'Data/RefBldgs/ASHRAE901_SchoolPrimary_STD2022_NewYork.idf'

my_model = IDF(file_path)
# my_model = IDF(file_path)
# my_model.printidf()

all_objs = my_model.idfobjects

# Get all thermal zones:
#####################################################################
# zones = get_all_targets(my_model, key='Zone')['field']
# print(len(zones))

zones = sort_zone_by_condition(my_model)
conditioned_zones = zones[0]['field']
unconditioned_zones = zones[1]['field']
print(conditioned_zones)
print(unconditioned_zones)

sorted_zones = sort_zone_by_floor_2(zones[0], display_field=True)
# sorted_zones = sort_zone_by_name(conditioned_zones)
print(sorted_zones)
# print(sorted_zones.keys())
# print(sorted_zones['A'])

# Deleting existing defined objects:
#####################################################################
delete_hvac_objs(my_model)

# Save to a new file:
#####################################################################
# my_model.saveas('Data/CIB-Office_new.idf')
