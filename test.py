import eppy
from eppy.modeleditor import IDF
from Helper import delete_hvac_objs, get_all_targets, set_always_on
from HVACSystem.PlantLoop import PlantLoop
from HVACSystem.AirLoop import AirLoop
from HVACSystem.PlantLoopComponents import PlantLoopComponent
from HVACSystem.AirLoopComponents import AirLoopComponent
from HVACSystem.SetpointManager import SetpointManager
from HVACSystem.PerformanceCurves import PerformanceCurve

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

# Creating new air loop:
#####################################################################
clg_coil = AirLoopComponent.cooling_coil_water(my_model, 'AHU Cooling Coil', control_variable=2)
htg_coil = AirLoopComponent.heating_coil_water(my_model, 'AHU Heating Coil')
fan = AirLoopComponent.fan_variable_speed(my_model, 'Fan', fan_curve_coeff=PerformanceCurve.fan_curve_set())
ahu_spm = SetpointManager.scheduled(my_model, name='AHU Setpoint Manager', constant_value=12.8)
# sizing = AirLoopComponent.sizing(my_model, doas=False)

loop = AirLoop.air_loop_hvac(
    my_model,
    name='DOAS System',
    doas=True,
    heat_recovery=True,
    supply_branches=[clg_coil, htg_coil],
    supply_fan=fan,
    setpoint_manager=ahu_spm,
    zones=zones,
    air_terminal_type=1,
    # sizing=sizing,
    zone_air_unit_type=2,
    zone_radiative_type=5)
print(loop['Loop'])
# print(clg_coil['object'])
# print(htg_coil['object'])
# print(fan['object'])
all_clg_coils = loop['Cooling_Coils']
all_htg_coils = loop['Heating_Coils']
# print(all_htg_coils)

# Creating new chilled water loop:
####################################################################
pump_chw = PlantLoopComponent.pump_variable_speed(my_model, name='Chw pump')
chiller1 = PlantLoopComponent.chiller_electric(my_model, name='Chiller 1', condenser_type=2, chiller_flow_mode=1)
chw_spm = SetpointManager.scheduled(my_model, name='Chilled Water Temp', constant_value=7)

chw_loop = PlantLoop.water_loop(
    my_model,
    name='Test Chilled Water Loop',
    loop_type=1,
    fluid_type=1,
    supply_inlet_branches=pump_chw,
    supply_branches=[chiller1],
    demand_branches=all_clg_coils,
    setpoint_manager=chw_spm)

# print(chw_loop)

# Creating new condenser water loop:
####################################################################
pump_cw = PlantLoopComponent.pump_variable_speed(my_model, name='CW pump')
tower = PlantLoopComponent.cooling_tower_single_speed(my_model, name='Cooling Tower 1')
cw_spm = SetpointManager.follow_outdoor_air_temp(my_model, name='Condenser Water Temperature', ashrae_default=True)

cw_loop = PlantLoop.water_loop(
    my_model,
    name='Test Condenser Water Loop',
    loop_type=3,
    fluid_type=1,
    supply_inlet_branches=pump_cw,
    supply_branches=[tower],
    demand_branches=[chiller1],
    setpoint_manager=cw_spm)

# print(cw_loop)

# Creating new hot water loop:
#####################################################################
pump_hw = PlantLoopComponent.pump_variable_speed(my_model, name='HW pump')
district = PlantLoopComponent.district_heating_v24(my_model, name='District Heating')
hw_spm = SetpointManager.scheduled(my_model, name='Hot Water Temperature', constant_value=60)

hw_loop = PlantLoop.water_loop(
    my_model,
    name='Test Hot Water Loop',
    loop_type=2,
    fluid_type=1,
    supply_inlet_branches=pump_hw,
    supply_branches=[district],
    demand_branches=all_htg_coils,
    setpoint_manager=hw_spm)

# print(hw_loop)

# object = my_model.newidfobject('Coil:Heating:DX:VariableRefrigerantFlow')
# print(object.fieldnames)
# print(object)

# vrf = VRF.vrf_system(my_model, 'My VRF System', test_mode=True)
# print(vrf)

# Save to a new file:
#####################################################################
my_model.saveas('Data/TestOffice_new.idf')
