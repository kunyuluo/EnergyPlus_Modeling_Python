import eppy
from Obj_Structure import Obj_Tree
from eppy.modeleditor import IDF
from eppy import hvacbuilder
from Helper import delete_hvac_objs
from Helper import SomeFields, flattencopy
from HVACSystem.PlantLoop import PlantLoop
from HVACSystem.AirLoop import AirLoop
from HVACSystem.PlantLoopComponents import PlantLoopComponent
from HVACSystem.AirLoopComponents import AirLoopComponent
from HVACSystem.SetpointManager import SetpointManager
from HVACSystem.PerformanceCurves import PerformanceCurve
from HVACSystem.ZoneEquipments import ZoneEquipment

idd_file = 'Data/Energy+.idd'
try:
    IDF.setiddname(idd_file)
except eppy.modeleditor.IDDAlreadySetError as e:
    pass

# file_path = 'Data/CIB-Office.idf'
file_path = 'Data/TestOffice.idf'

my_model = IDF(file_path)
# my_model = IDF(file_path)
# my_model.printidf()

all_objs = my_model.idfobjects
# print(all_objs.keys())
# bldg = all_objs['BUILDING'][0]
# print(bldg.Name)
# print(bldg.North_Axis)

# zones = all_objs['Zone']
# print(zones)
# print(len(zones))
# zone_names = []
# for zone in zones:
#     name = zone.Name
#     # name = zone.Name.split(' ')[0]
#     zone_names.append(name)
# print(zone_names)

# Get all setpoint managers:
#####################################################################
# all_spms = all_objs['SetpointManager:MixedAir'.upper()]
# print(all_spms)

# Deleting existing defined objects:
#####################################################################
delete_hvac_objs(my_model)

# all_plantloop = all_objs['Chiller:Electric:EIR'.upper()]
# print(all_plantloop)

# Creating new plant loop:
#####################################################################
# pipe1 = PlantLoopComponent.pipe(my_model, name='pipe1')
# pipe2 = PlantLoopComponent.pipe(my_model, name='pipe2')
# pipe3 = PlantLoopComponent.pipe(my_model, name='pipe3')
# pipe4 = PlantLoopComponent.pipe(my_model, name='pipe4')
# spm = SetpointManager.scheduled(my_model, name='spm')
#
# newplantloop = PlantLoop.water_loop(
#     my_model,
#     name='Test Chilled Water Loop',
#     supply_inlet_branches=pipe1,
#     supply_branches=[[pipe2], [pipe3]],
#     demand_branches=pipe4,
#     setpoint_manager=spm)
#
# # print(spm)
# print(newplantloop)

preheat_coil = AirLoopComponent.heating_coil_electric(my_model, 'Preheat Coil')
hx = AirLoopComponent.heat_exchanger_air_to_air(my_model, 'HX')
clg_coil = AirLoopComponent.cooling_coil_water(my_model, 'Cooling Coil')
htg_coil = AirLoopComponent.heating_coil_water(my_model, 'Heating Coil')
fan = AirLoopComponent.fan_variable_speed(my_model, 'Fan', fan_curve_coeff=PerformanceCurve.fan_curve_set())
sizing = AirLoopComponent.sizing(my_model)
zones = ['Office_1', 'Office_2']
loop = AirLoop.air_loop_hvac(
    my_model,
    name='VAV System',
    outdoor_air_stream_comp=[preheat_coil, hx],
    supply_branches=[clg_coil, htg_coil],
    supply_fan=fan,
    zones=zones,
    sizing=sizing,)
print(loop)

# zones = ['Office_1']
# zone_group = ZoneEquipment.zone_equipment_group(my_model, zones=zones, air_terminal_type=3, zone_hvac_type=2)
# print(zone_group)

object = my_model.newidfobject('ZoneHVAC:FourPipeFanCoil'.upper())
print(object.fieldnames)

# Save to a new file:
#####################################################################
# my_model.saveas('Data/TestOffice_empty.idf')
