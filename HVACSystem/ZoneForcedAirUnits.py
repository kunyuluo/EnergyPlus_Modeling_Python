from eppy.modeleditor import IDF
from eppy.bunch_subclass import EpBunch
import configs
from HVACSystem.AirLoopComponents import AirLoopComponent
from configs import *


class ZoneForcedAirUnit:
    @staticmethod
    def fan_coil_unit(
            idf: IDF,
            name: str = None,
            schedule: EpBunch | str = None,
            capacity_control_method: int = 0,
            heating_coil_type: int = 1,
            fan_pressure_rise=configs.fan_pressure_rise_default,
            max_supply_air_flow_rate=configs.autosize,
            low_speed_supply_air_flow_ratio=None,
            medium_speed_supply_air_flow_ratio=None,
            max_outdoor_air_flow_rate=configs.autosize,
            outdoor_air_schedule=None,
            max_cold_water_flow_rate=configs.autosize,
            min_cold_water_flow_rate=None,
            max_hot_water_flow_rate=configs.autosize,
            min_hot_water_flow_rate=None,
            supply_air_fan_operating_mode_schedule=None,
            min_supply_air_temp_cooling=configs.autosize,
            max_supply_air_temp_heating=configs.autosize):

        """
        -Options for "capacity_control_method":
            0:"ConstantFanVariableFlow",
            1:"VariableFanVariableFlow",
            2:"VariableFanConstantFlow",
            3:"CyclingFan",
            4:"MultiSpeedFan",
            5:"ASHRAE90VariableFan" \n

        -Heating coil type:
            1:Water,
            2:Electric
        """

        capacity_controls = {0: "ConstantFanVariableFlow", 1: "VariableFanVariableFlow", 2: "VariableFanConstantFlow",
                             3: "CyclingFan", 4: "MultiSpeedFan", 5: "ASHRAE90VariableFan"}

        fcu_assembly = []
        name = 'Four Pipe Fan Coil' if name is None else name
        fcu = idf.newidfobject('ZoneHVAC:FourPipeFanCoil', Name=name)

        if schedule is None:
            fcu['Availability_Schedule_Name'] = configs.schedule_always_on_hvac
        else:
            if isinstance(schedule, EpBunch):
                fcu['Availability_Schedule_Name'] = schedule.Name
            elif isinstance(schedule, str):
                fcu['Availability_Schedule_Name'] = schedule
            else:
                raise TypeError('Invalid type of schedule.')

        # Create a OA Mixer object:
        mixer_name = f'{name} OA Mixer'
        oa_mixer = idf.newidfobject('OutdoorAir:Mixer', Name=mixer_name)
        mixed_air_node_name = f'{mixer_name} Mixed Air Node'
        oa_node_name = f'{mixer_name} Outdoor Air Node'
        relief_air_node_name = f'{mixer_name} Relief Air Node'
        return_air_node_name = f'{mixer_name} Return Air Node'
        oa_mixer['Mixed_Air_Node_Name'] = mixed_air_node_name
        oa_mixer['Outdoor_Air_Stream_Node_Name'] = oa_node_name
        oa_mixer['Relief_Air_Stream_Node_Name'] = relief_air_node_name
        oa_mixer['Return_Air_Stream_Node_Name'] = return_air_node_name
        fcu_assembly.append(oa_mixer)

        # Create OutdoorAir NodeList:
        oa_nodelist = idf.newidfobject('OutdoorAir:NodeList')
        oa_nodelist['Node_or_NodeList_Name_1'] = oa_node_name
        fcu_assembly.append(oa_nodelist)

        # Create a fan object based on control method:
        match capacity_control_method:
            case 0:
                fan_name = f'{name} Const Speed Fan'
                fan = AirLoopComponent.fan_constant_speed(idf, name=fan_name, pressure_rise=fan_pressure_rise)
            case 1 | 2:
                fan_name = f'{name} Var Speed Fan'
                fan = AirLoopComponent.fan_variable_speed(idf, name=fan_name, pressure_rise=fan_pressure_rise)
            case 3 | 4 | 5 | _:
                fan_name = f'{name} On Off Fan'
                fan = AirLoopComponent.fan_on_off(idf, name=fan_name, pressure_rise=fan_pressure_rise)
        fan['object'][fan['air_inlet_field']] = mixed_air_node_name
        fan_outlet_node_name = f'{fan_name} Fan Outlet Node'
        fan['object'][fan['air_outlet_field']] = fan_outlet_node_name
        fcu_assembly.append(fan['object'])

        # Create a cooling coil object:
        clg_coil_name = f'{name} Cooling Coil'
        cooling_coil = AirLoopComponent.cooling_coil_water(idf, name=clg_coil_name, need_controller=False)
        cooling_coil['object'][cooling_coil['air_inlet_field']] = fan_outlet_node_name
        clg_coil_outlet_node_name = f'{clg_coil_name} Coil Outlet Node'
        cooling_coil['object'][cooling_coil['air_outlet_field']] = clg_coil_outlet_node_name
        fcu_assembly.append(cooling_coil['object'])

        # Create a heating coil object based on control method:
        htg_coil_name = f'{name} Heating Coil'
        match heating_coil_type:
            case 1:
                heating_coil = AirLoopComponent.heating_coil_water(idf, name=htg_coil_name, need_controller=False)
            case 2 | _:
                heating_coil = AirLoopComponent.heating_coil_electric(idf, name=htg_coil_name)
        heating_coil['object'][heating_coil['air_inlet_field']] = clg_coil_outlet_node_name
        htg_coil_outlet_node_name = f'{htg_coil_name} Coil Outlet Node'
        heating_coil['object'][heating_coil['air_outlet_field']] = htg_coil_outlet_node_name
        fcu_assembly.append(heating_coil['object'])

        fcu['Air_Inlet_Node_Name'] = return_air_node_name
        fcu['Air_Outlet_Node_Name'] = htg_coil_outlet_node_name
        fcu['Outdoor_Air_Mixer_Object_Type'] = 'OutdoorAir:Mixer'
        fcu['Outdoor_Air_Mixer_Name'] = mixer_name
        fcu['Supply_Air_Fan_Object_Type'] = fan['type']
        fcu['Supply_Air_Fan_Name'] = fan_name
        fcu['Cooling_Coil_Object_Type'] = cooling_coil['type']
        fcu['Cooling_Coil_Name'] = clg_coil_name
        fcu['Heating_Coil_Object_Type'] = heating_coil['type']
        fcu['Heating_Coil_Name'] = htg_coil_name

        fcu['Capacity_Control_Method'] = capacity_controls[capacity_control_method]
        fcu['Maximum_Supply_Air_Flow_Rate'] = max_supply_air_flow_rate
        if low_speed_supply_air_flow_ratio is not None:
            fcu['Low_Speed_Supply_Air_Flow_Ratio'] = low_speed_supply_air_flow_ratio
        if medium_speed_supply_air_flow_ratio is not None:
            fcu['Medium_Speed_Supply_Air_Flow_Ratio'] = medium_speed_supply_air_flow_ratio
        fcu['Maximum_Outdoor_Air_Flow_Rate'] = max_outdoor_air_flow_rate
        if outdoor_air_schedule is not None:
            fcu['Outdoor_Air_Schedule_Name'] = outdoor_air_schedule
        fcu['Maximum_Cold_Water_Flow_Rate'] = max_cold_water_flow_rate
        if min_cold_water_flow_rate is not None:
            fcu['Minimum_Cold_Water_Flow_Rate'] = min_cold_water_flow_rate
        fcu['Maximum_Hot_Water_Flow_Rate'] = max_hot_water_flow_rate
        if min_hot_water_flow_rate is not None:
            fcu['Minimum_Hot_Water_Flow_Rate'] = min_hot_water_flow_rate
        if supply_air_fan_operating_mode_schedule is not None:
            fcu['Supply_Air_Fan_Operating_Mode_Schedule_Name'] = supply_air_fan_operating_mode_schedule
        fcu['Minimum_Supply_Air_Temperature_in_Cooling_Mode'] = min_supply_air_temp_cooling
        fcu['Maximum_Supply_Air_Temperature_in_Heating_Mode'] = max_supply_air_temp_heating
        fcu_assembly.append(fcu)

        component = {
            'object': fcu,
            'type': 'ZoneHVAC:FourPipeFanCoil',
            'cooling_coil': cooling_coil,
            'heating_coil': heating_coil,
            'fan': fan,
        }

        return component

    @staticmethod
    def vrf_terminal(
            idf: IDF,
            name: str = None,
            schedule=None,
            supply_air_flow_rate_cooling=configs.autosize,
            supply_air_flow_rate_no_cooling=configs.autosize,
            supply_air_flow_rate_heating=configs.autosize,
            supply_air_flow_rate_no_heating=configs.autosize,
            need_outdoor_air: bool = False,
            outdoor_air_flow_rate_cooling=configs.autosize,
            outdoor_air_flow_rate_heating=configs.autosize,
            outdoor_air_flow_rate_no_load=configs.autosize,
            supply_air_fan_schedule=None,
            supply_air_fan_placement: int = 1,
            supply_air_fan: dict = None,
            cooling_coil: dict = None,
            heating_coil: dict = None,
            supplemental_heating_coil: dict = None,
            terminal_on_parasitic_electric_energy: int | float = 30,
            terminal_off_parasitic_electric_energy: int | float = 20,
            heating_capacity_sizing_ratio=1,
            max_supply_air_temp_from_supplemental_heater=configs.autosize,
            max_outdoor_air_temp_for_supplemental_heater: int | float = 21,):
        """
        Fan Placement: 1.BlowThrough 2.DrawThrough
        """
        placements = {1: 'BlowThrough', 2: 'DrawThrough'}

        name = 'VRF Terminal' if name is None else name
        terminal = idf.newidfobject('ZoneHVAC:TerminalUnit:VariableRefrigerantFlow')
        terminal['Zone_Terminal_Unit_Name'] = name

        if schedule is None:
            terminal['Terminal_Unit_Availability_Schedule'] = configs.schedule_always_on_hvac
        else:
            if isinstance(schedule, EpBunch):
                terminal['Terminal_Unit_Availability_Schedule'] = schedule.Name
            elif isinstance(schedule, str):
                terminal['Terminal_Unit_Availability_Schedule'] = schedule
            else:
                raise TypeError('Invalid type of schedule.')

        terminal['Cooling_Supply_Air_Flow_Rate'] = supply_air_flow_rate_cooling
        terminal['No_Cooling_Supply_Air_Flow_Rate'] = supply_air_flow_rate_no_cooling
        terminal['Heating_Supply_Air_Flow_Rate'] = supply_air_flow_rate_heating
        terminal['No_Heating_Supply_Air_Flow_Rate'] = supply_air_flow_rate_no_heating
        if need_outdoor_air:
            terminal['Cooling_Outdoor_Air_Flow_Rate'] = outdoor_air_flow_rate_cooling
            terminal['Heating_Outdoor_Air_Flow_Rate'] = outdoor_air_flow_rate_heating
            terminal['No_Load_Outdoor_Air_Flow_Rate'] = outdoor_air_flow_rate_no_load
        else:
            terminal['Cooling_Outdoor_Air_Flow_Rate'] = 0
            terminal['Heating_Outdoor_Air_Flow_Rate'] = 0
            terminal['No_Load_Outdoor_Air_Flow_Rate'] = 0

        if supply_air_fan_schedule is None:
            terminal['Supply_Air_Fan_Operating_Mode_Schedule_Name'] = configs.schedule_always_on_hvac
        else:
            if isinstance(supply_air_fan_schedule, EpBunch):
                terminal['Supply_Air_Fan_Operating_Mode_Schedule_Name'] = supply_air_fan_schedule.Name
            elif isinstance(supply_air_fan_schedule, str):
                terminal['Supply_Air_Fan_Operating_Mode_Schedule_Name'] = supply_air_fan_schedule
            else:
                raise TypeError('Invalid type of supply_air_fan_schedule.')

        terminal['Supply_Air_Fan_Placement'] = placements[supply_air_fan_placement]

        # OutdoorAir Mixer object:
        mixer_name = f'{name} OA Mixer'
        oa_mixer = idf.newidfobject('OutdoorAir:Mixer', Name=mixer_name)
        mixed_air_node_name = f'{mixer_name} Mixed Air Node'
        oa_node_name = f'{mixer_name} Outdoor Air Node'
        relief_air_node_name = f'{mixer_name} Relief Air Node'
        return_air_node_name = f'{mixer_name} Return Air Node'
        oa_mixer['Mixed_Air_Node_Name'] = mixed_air_node_name
        oa_mixer['Outdoor_Air_Stream_Node_Name'] = oa_node_name
        oa_mixer['Relief_Air_Stream_Node_Name'] = relief_air_node_name
        oa_mixer['Return_Air_Stream_Node_Name'] = return_air_node_name

        # Node list:
        node_list = idf.newidfobject('OutdoorAir:NodeList')
        node_list['Node_or_NodeList_Name_1'] = oa_node_name

        terminal['Terminal_Unit_Air_Inlet_Node_Name'] = return_air_node_name
        terminal_air_out_node = f'{name} Terminal Air Outlet Node'
        terminal['Terminal_Unit_Air_Outlet_Node_Name'] = terminal_air_out_node

        # Cooling coil object:
        if cooling_coil is None:
            clg_coil_name = f'{name} Cooling Coil'
            cooling_coil = AirLoopComponent.cooling_coil_vrf(idf, clg_coil_name)
        terminal['Cooling_Coil_Object_Type'] = cooling_coil['type']
        terminal['Cooling_Coil_Object_Name'] = cooling_coil['object'].Name
        cooling_coil['object'][cooling_coil['air_inlet_field']] = mixed_air_node_name

        # Heating coil object:
        if heating_coil is None:
            htg_coil_name = f'{name} Cooling Coil'
            heating_coil = AirLoopComponent.heating_coil_vrf(idf, htg_coil_name)
        terminal['Heating_Coil_Object_Type'] = heating_coil['type']
        terminal['Heating_Coil_Object_Name'] = heating_coil['object'].Name
        heating_coil['object'][heating_coil['air_inlet_field']] =\
            cooling_coil['object'][cooling_coil['air_outlet_field']]

        # Supply air fan object:
        if supply_air_fan is None:
            fan_name = f'{name} Fan OnOff'
            supply_air_fan = AirLoopComponent.fan_on_off(idf, fan_name)
        terminal['Supply_Air_Fan_Object_Type'] = supply_air_fan['type']
        terminal['Supply_Air_Fan_Object_Name'] = supply_air_fan['object'].Name
        supply_air_fan['object'][supply_air_fan['air_inlet_field']] =\
            heating_coil['object'][heating_coil['air_outlet_field']]
        supply_air_fan['object'][supply_air_fan['air_outlet_field']] = terminal_air_out_node

        if supplemental_heating_coil is not None:
            terminal['Supplemental_Heating_Coil_Object_Type'] = supplemental_heating_coil['type']
            terminal['Supplemental_Heating_Coil_Name'] = supplemental_heating_coil['object'].Name

        terminal['Maximum_Supply_Air_Temperature_from_Supplemental_Heater'] =\
            max_supply_air_temp_from_supplemental_heater
        terminal['Maximum_Outdoor_DryBulb_Temperature_for_Supplemental_Heater_Operation'] =\
            max_outdoor_air_temp_for_supplemental_heater
        # terminal['Controlling_Zone_or_Thermostat_Location'] = zone_name
        terminal['Zone_Terminal_Unit_On_Parasitic_Electric_Energy_Use'] = terminal_on_parasitic_electric_energy
        terminal['Zone_Terminal_Unit_Off_Parasitic_Electric_Energy_Use'] = terminal_off_parasitic_electric_energy
        terminal['Rated_Heating_Capacity_Sizing_Ratio'] = heating_capacity_sizing_ratio

        component = {
            'object': terminal,
            'type': 'ZoneHVAC:TerminalUnit:VariableRefrigerantFlow',
            'cooling_coil': cooling_coil,
            'heating_coil': heating_coil,
            'fan': supply_air_fan,
        }

        return component

