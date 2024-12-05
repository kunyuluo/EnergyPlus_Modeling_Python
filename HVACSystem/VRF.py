from eppy.modeleditor import IDF
from eppy.bunch_subclass import EpBunch
from HVACSystem.PerformanceCurves import PerformanceCurve
from HVACSystem.ZoneForcedAirUnits import ZoneForcedAirUnit
from configs import *


class VRF:
    @staticmethod
    def vrf_system(
            idf: IDF,
            name: str = None,
            schedule=None,
            cooling_capacity=autosize,
            cooling_cop=3.3,
            heating_capacity=autosize,
            heating_cop=3.5,
            heating_capacity_sizing_ratio=1,
            heating_performance_curve_temp_type: int = 1,
            min_part_load_ratio=0.15,
            master_thermostat_control_type: int = 1,
            heat_recovery: bool = False,
            number_of_compressor: int = 3,
            condenser_type: int = 1,
            fuel_type: int = 1,
            performance_curve_set=None,
            terminals: list[str] | list[EpBunch] | list[dict] = None,
            test_mode: bool = False):
        """
        -Heating Performance Curve Outdoor Temperature Type \n
        1.WetBulbTemperature 2.DryBulbTemperature \n

        -Master Thermostat Priority Control Type \n
        1.LoadPriority 2.ZonePriority 3.ThermostatOffsetPriority 4.MasterThermostatPriority 5.Scheduled \n

        -Defrost Strategy: 1.ReverseCycle 2.Resistive \n
        -Defrost Control: 1.Timed 2.OnDemand \n
        -Condenser Type: 1.AirCooled 2.EvaporativelyCooled 3.WaterCooled \n
        -Fuel Type: 1.Electricity, 2.NaturalGas, 3.Propane, 4.Diesel, 5.Gasoline, 6.FuelOilNo1, 7.FuelOilNo2, 8.OtherFuel1, 9.OtherFuel2
        """
        temp_types = {1: 'WetBulbTemperature', 2: 'DryBulbTemperature'}
        control_types = {1: 'LoadPriority', 2: 'ZonePriority', 3: 'ThermostatOffsetPriority',
                         4: 'MasterThermostatPriority', 5: 'Scheduled'}
        defrost_types = {1: 'ReverseCycle', 2: 'Resistive'}
        defrost_controls = {1: 'Timed', 2: 'OnDemand'}
        condenser_types = {1: 'AirCooled', 2: 'EvaporativelyCooled', 3: 'WaterCooled'}
        fuel_types = {1: 'Electricity', 2: 'NaturalGas', 3: 'Propane', 4: 'Diesel', 5: 'Gasoline', 6: 'FuelOilNo1',
                      7: 'FuelOilNo2', 8: 'OtherFuel1', 9: 'OtherFuel2'}

        vrf_assembly = []
        name = 'VRF System' if name is None else name
        vrf = idf.newidfobject('AirConditioner:VariableRefrigerantFlow')

        vrf['Heat_Pump_Name'] = name

        if schedule is None:
            vrf['Availability_Schedule_Name'] = schedule_always_on_hvac
        else:
            if isinstance(schedule, EpBunch):
                vrf['Availability_Schedule_Name'] = schedule.Name
            elif isinstance(schedule, str):
                vrf['Availability_Schedule_Name'] = schedule
            else:
                raise TypeError('Invalid type of schedule.')

        vrf['Gross_Rated_Total_Cooling_Capacity'] = cooling_capacity
        vrf['Gross_Rated_Cooling_COP'] = cooling_cop
        vrf['Minimum_Condenser_Inlet_Node_Temperature_in_Cooling_Mode'] = -6
        vrf['Maximum_Condenser_Inlet_Node_Temperature_in_Cooling_Mode'] = 43
        vrf['Gross_Rated_Heating_Capacity'] = heating_capacity
        vrf['Gross_Rated_Heating_COP'] = heating_cop
        vrf['Rated_Heating_Capacity_Sizing_Ratio'] = heating_capacity_sizing_ratio
        vrf['Minimum_Condenser_Inlet_Node_Temperature_in_Heating_Mode'] = -20
        vrf['Maximum_Condenser_Inlet_Node_Temperature_in_Heating_Mode'] = 16
        vrf['Heating_Performance_Curve_Outdoor_Temperature_Type'] = temp_types[heating_performance_curve_temp_type]
        vrf['Minimum_Heat_Pump_PartLoad_Ratio'] = min_part_load_ratio
        vrf['Master_Thermostat_Priority_Control_Type'] = control_types[master_thermostat_control_type]
        vrf['Heat_Pump_Waste_Heat_Recovery'] = 'Yes' if heat_recovery else 'No'
        vrf['Equivalent_Piping_Length_used_for_Piping_Correction_Factor_in_Cooling_Mode'] = 30
        vrf['Vertical_Height_used_for_Piping_Correction_Factor'] = 10
        vrf['Piping_Correction_Factor_for_Height_in_Cooling_Mode_Coefficient'] = -0.000386
        vrf['Equivalent_Piping_Length_used_for_Piping_Correction_Factor_in_Heating_Mode'] = 30
        vrf['Piping_Correction_Factor_for_Height_in_Heating_Mode_Coefficient'] = 0
        vrf['Crankcase_Heater_Power_per_Compressor'] = 15
        vrf['Number_of_Compressors'] = number_of_compressor
        vrf['Ratio_of_Compressor_Size_to_Total_Compressor_Capacity'] = 1 / number_of_compressor
        vrf['Maximum_Outdoor_DryBulb_Temperature_for_Crankcase_Heater'] = 7
        vrf['Defrost_Strategy'] = defrost_types[2]
        vrf['Defrost_Control'] = defrost_controls[1]
        vrf['Defrost_Time_Period_Fraction'] = 0.058333
        vrf['Resistive_Defrost_Heater_Capacity'] = 0
        vrf['Maximum_Outdoor_Drybulb_Temperature_for_Defrost_Operation'] = 7
        vrf['Condenser_Type'] = condenser_types[condenser_type]
        if condenser_type == 3:
            vrf['Condenser_Inlet_Node_Name'] = f'{name} Condenser Inlet'
            vrf['Condenser_Outlet_Node_Name'] = f'{name} Condenser Outlet'
            vrf['Water_Condenser_Volume_Flow_Rate'] = autosize
        vrf['Evaporative_Condenser_Effectiveness'] = 0.9
        vrf['Evaporative_Condenser_Air_Flow_Rate'] = autosize
        vrf['Evaporative_Condenser_Pump_Rated_Power_Consumption'] = autosize
        vrf['Basin_Heater_Capacity'] = 0
        vrf['Basin_Heater_Setpoint_Temperature'] = 2
        vrf['Fuel_Type'] = fuel_types[fuel_type]
        vrf['Minimum_Condenser_Inlet_Node_Temperature_in_Heat_Recovery_Mode'] = 0
        vrf['Maximum_Condenser_Inlet_Node_Temperature_in_Heat_Recovery_Mode'] = 20
        vrf['Initial_Heat_Recovery_Cooling_Capacity_Fraction'] = 0.5
        vrf['Heat_Recovery_Cooling_Capacity_Time_Constant'] = 0.083
        vrf['Initial_Heat_Recovery_Cooling_Energy_Fraction'] = 1
        vrf['Heat_Recovery_Cooling_Energy_Time_Constant'] = 0
        vrf['Initial_Heat_Recovery_Heating_Capacity_Fraction'] = 0.5
        vrf['Heat_Recovery_Heating_Capacity_Time_Constant'] = 0.083
        vrf['Initial_Heat_Recovery_Heating_Energy_Fraction'] = 0.5
        vrf['Heat_Recovery_Heating_Energy_Time_Constant'] = 0

        vrf_assembly.append(vrf)

        # Performance curves:
        if performance_curve_set is None:
            performance_curve_set = PerformanceCurve.vrf_performance_curve_set_1(idf)
        for key in performance_curve_set.keys():
            vrf[key] = performance_curve_set[key]['Name']
        for curve in performance_curve_set.values():
            vrf_assembly.append(curve)

        # Terminal units:
        terminal_list_name = f'{name} Terminal List'
        terminal_list = idf.newidfobject('ZoneTerminalUnitList')
        terminal_list['Zone_Terminal_Unit_List_Name'] = terminal_list_name
        terminals = [] if terminals is None else terminals
        if len(terminals) > 0:
            for i, terminal in enumerate(terminals):
                if isinstance(terminal, str):
                    terminal_list[f'Zone_Terminal_Unit_Name_{i + 1}'] = terminal
                elif isinstance(terminal, dict):
                    terminal_list[f'Zone_Terminal_Unit_Name_{i + 1}'] = terminal['object'].Name
                elif isinstance(terminal, EpBunch):
                    terminal_list[f'Zone_Terminal_Unit_Name_{i + 1}'] = terminal.Name
                else:
                    raise TypeError('Invalid type of terminal.')

        vrf['Zone_Terminal_Unit_List_Name'] = terminal_list_name
        vrf_assembly.append(terminal_list)

        comp = {
            'object': vrf,
            'type': 'AirConditioner:VariableRefrigerantFlow',
            'condenser_water_inlet_field': f'{name} Condenser Inlet' if condenser_type == 3 else None,
            'condenser_water_outlet_field': f'{name} Condenser Outlet' if condenser_type == 3 else None,
        }
        if test_mode:
            return vrf_assembly
        else:
            return comp
