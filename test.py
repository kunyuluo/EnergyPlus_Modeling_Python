import eppy
from Obj_Structure import Obj_Tree
from eppy.modeleditor import IDF
from eppy import hvacbuilder
from Helper import delete_hvac_objs, get_all_zones
from Helper import SomeFields, flattencopy
from HVACSystem.PlantLoop import PlantLoop
from HVACSystem.AirLoop import AirLoop
from HVACSystem.PlantLoopComponents import PlantLoopComponent
from HVACSystem.AirLoopComponents import AirLoopComponent
from HVACSystem.SetpointManager import SetpointManager
from HVACSystem.PerformanceCurves import PerformanceCurve
from HVACSystem.ZoneEquipments import ZoneEquipment
from Schedules.Schedules import Schedule

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

# Get all thermal zones:
#####################################################################
zones = get_all_zones(my_model)
print(zones)

# Deleting existing defined objects:
#####################################################################
delete_hvac_objs(my_model)

# all_plantloop = all_objs['Chiller:Electric:EIR'.upper()]
# print(all_plantloop)

# Creating new plant loop:
#####################################################################
# pump = PlantLoopComponent.pump_variable_speed(my_model, name='Chw pump')
# chiller1 = PlantLoopComponent.chiller_electric(my_model, name='Chiller 1')
# chiller2 = PlantLoopComponent.chiller_electric(my_model, name='Chiller 2')
# pipe1 = PlantLoopComponent.pipe(my_model, name='pipe1')
# pipe2 = PlantLoopComponent.pipe(my_model, name='pipe2')
# chw_spm = SetpointManager.scheduled(my_model, name='Chilled Water Temperature', constant_value=12.8)
#
# newplantloop = PlantLoop.water_loop(
#     my_model,
#     name='Test Chilled Water Loop',
#     loop_type=1,
#     fluid_type=1,
#     supply_inlet_branches=pump,
#     supply_branches=[[chiller1], [chiller2]],
#     demand_branches=[pipe1, pipe2],
#     setpoint_manager=chw_spm)
#
# print(newplantloop)

preheat_coil = AirLoopComponent.heating_coil_electric(my_model, 'Preheat Coil')
hx = AirLoopComponent.heat_exchanger_air_to_air(my_model, 'HX')
clg_coil = AirLoopComponent.cooling_coil_water(my_model, 'AHU Cooling Coil')
htg_coil = AirLoopComponent.heating_coil_water(my_model, 'AHU Heating Coil')
fan = AirLoopComponent.fan_variable_speed(my_model, 'Fan', fan_curve_coeff=PerformanceCurve.fan_curve_set())
ahu_spm = SetpointManager.scheduled(my_model, name='AHU Setpoint Manager', constant_value=12.8)
sizing = AirLoopComponent.sizing(my_model)

loop = AirLoop.air_loop_hvac(
    my_model,
    name='VAV System',
    # outdoor_air_stream_comp=[preheat_coil, hx],
    heat_recovery=True,
    supply_branches=[clg_coil, htg_coil],
    supply_fan=fan,
    setpoint_manager=ahu_spm,
    zones=zones,
    sizing=sizing,
    zone_hvac_type=None)
print(loop)

# year = Schedule.year(
#     my_model,
#     name='Supply Air Temp Schedule',
#     constant_value=23,
#     numeric_type=1,
#     unit_type=2,
#     test_mode=True)
# print(year)

# object = my_model.newidfobject('AvailabilityManagerAssignmentList')
# print(object.fieldnames)

# Save to a new file:
#####################################################################
# my_model.saveas('Data/TestOffice_empty.idf')
