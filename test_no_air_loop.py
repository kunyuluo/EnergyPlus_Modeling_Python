import eppy
from eppy.modeleditor import IDF
from Helper import delete_hvac_objs, get_all_targets, set_always_on
from HVACSystem.AirLoop import AirLoop
from HVACSystem.VRF import VRF

# idd_file = 'Data/Energy+_v22.idd'
idd_file = 'Data/Energy+_v24.idd'
try:
    IDF.setiddname(idd_file)
except eppy.modeleditor.IDDAlreadySetError as e:
    pass

# file_path = 'Data/CIB-Office.idf'
file_path = 'Data/TestOffice.idf'
# file_path = 'Data/SmallOffice_CentralDOAS.idf'

my_model = IDF(file_path)
# my_model = IDF(file_path)
# my_model.printidf()

all_objs = my_model.idfobjects

# Get all thermal zones:
#####################################################################
zones = get_all_targets(my_model, key='Zone')['object']
# zones = zones[1:]
# print(zones)

schedule = set_always_on(my_model)
# print(schedule)

# Deleting existing defined objects:
#####################################################################
delete_hvac_objs(my_model)

# Zone HVAC Only (No Air Loop):
#####################################################################
loop = AirLoop.no_air_loop(
    my_model,
    zones=zones,
    vrf_system=True,
    zone_air_unit_type=None,
    zone_radiative_type=5)
print(loop['Loop'])
# all_clg_coils = loop['Cooling_Coils']
# all_htg_coils = loop['Heating_Coils']
all_vrf_terminals = loop['VRF_Terminals']
print(all_vrf_terminals)

vrf = VRF.vrf_system(my_model, name='My VRF System', terminals=all_vrf_terminals, test_mode=True)
# print(vrf)

# object = my_model.newidfobject('Coil:Heating:DX:VariableRefrigerantFlow')
# print(object.fieldnames)
# print(object)

# vrf = VRF.vrf_system(my_model, 'My VRF System', test_mode=True)
# print(vrf)

# Save to a new file:
#####################################################################
my_model.saveas('Data/TestOffice_new.idf')
