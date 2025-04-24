import eppy
from eppy.modeleditor import IDF
from Helper import delete_hvac_objs, delete_ems_object, set_always_on, sort_zone_by_condition
from Helper import SortZoneByFloor
from HVACSystem.PlantLoop import PlantLoop
from HVACSystem.AirLoop import AirLoop
from HVACSystem.VRF import VRF
from HVACSystem.PlantLoopComponents import PlantLoopComponent
from HVACSystem.AirLoopComponents import AirLoopComponent
from HVACSystem.SetpointManager import SetpointManager
from HVACSystem.PerformanceCurves import PerformanceCurve
from Output.Output import Output
from configs import *

# idd_file = 'Data/Energy+_v22.idd'
idd_file = 'Data/Energy+_v24.idd'
try:
    IDF.setiddname(idd_file)
except eppy.modeleditor.IDDAlreadySetError as e:
    pass

bldg_type = 'OfficeLarge'
file_path = f'Data/RefBldgs/ASHRAE901_{bldg_type}_STD2022_NewYork.idf'
save_new = True

my_model = IDF(file_path)

# Get all thermal zones:
#####################################################################
zones = sort_zone_by_condition(my_model)
# conditioned_zones = zones[0]['field']
# unconditioned_zones = zones[1]['field']
# print(conditioned_zones)
# print(unconditioned_zones)
# print(len(conditioned_zones))

sorting_func_name = func_by_type[bldg_type]
sorting_func = getattr(SortZoneByFloor, sorting_func_name)
sorted_zones = sorting_func(zones[0], display_field=True)
# print(sorted_zones.keys())
# print(sorted_zones)

schedule = set_always_on(my_model)
# print(schedule)

# Deleting existing defined objects:
#####################################################################
delete_hvac_objs(my_model, keep_shw=False, keep_refrigeration=False)
delete_ems_object(my_model)

# Creating new air loop:
#####################################################################
all_clg_coils = []
all_htg_coils = []
# all_vrf_terminals = []
if len(sorted_zones.keys()) > 0:
    for flr in sorted_zones.keys():
        served_zones = sorted_zones[flr]

        clg_coil = AirLoopComponent.cooling_coil_water(my_model, f'AHU Cooling Coil {flr}', control_variable=2)
        htg_coil = AirLoopComponent.heating_coil_water(my_model, f'AHU Heating Coil {flr}')
        fan = AirLoopComponent.fan_variable_speed(my_model, f'Fan {flr}', fan_curve_coeff=PerformanceCurve.fan_curve_set())
        ahu_spm = SetpointManager.scheduled(my_model, name=f'AHU Setpoint Manager {flr}', constant_value=12.8)
        ahu_spm_dehum = SetpointManager.scheduled(my_model, name=f'AHU Setpoint Manager Dehum {flr}', constant_value=0.008)
        # sizing = AirLoopComponent.sizing(my_model, doas=False)

        loop = AirLoop.air_loop_hvac(
            my_model,
            name=f'DOAS System {flr}',
            doas=True,
            heat_recovery=False,
            supply_branches=[clg_coil, htg_coil],
            supply_fan=fan,
            setpoint_manager=ahu_spm,
            setpoint_manager_dehumidification=ahu_spm_dehum,
            zones=served_zones,
            air_terminal_type=4,
            # sizing=sizing,
            zone_air_unit_type=2,
            zone_radiative_type=None)

        # loop = AirLoop.no_air_loop(
        #     my_model,
        #     zones=served_zones,
        #     vrf_system=True,
        #     zone_air_unit_type=None)

        all_clg_coils.extend(loop['Cooling_Coils'])
        all_htg_coils.extend(loop['Heating_Coils'])

        # all_vrf_terminals = loop['VRF_Terminals']
        # vrf = VRF.vrf_system(my_model, name=f'VRF System {flr}', terminals=all_vrf_terminals, test_mode=True)

# print(all_clg_coils)
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
# district = PlantLoopComponent.district_heating(my_model, name='District Heating')
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

# Output Variables:
#####################################################################
output_vars = ['Chiller Electricity Rate', 'Chiller COP', 'Chiller Evaporator Cooling Rate']
var = Output.variable(my_model, variables=output_vars)

# Save to a new file:
#####################################################################
if save_new:
    my_model.saveas(f'Data/RefBldgs/ASHRAE901_{bldg_type}_STD2022_NewYork_test.idf')
    print('Oh Yeah! New Model Is Saved Successfully!')
