from eppy.modeleditor import IDF
from eppy.bunch_subclass import EpBunch
from HVACSystem.PerformanceCurves import PerformanceCurve


class PlantLoopComponent:

    @staticmethod
    def sizing(
            idf: IDF,
            plantloop: EpBunch | str,
            loop_type: int = 1,
            loop_exit_temp=None,
            loop_temp_diff=None,
            sizing_option: int = 2,
            zone_timesteps_in_averaging_window=None,
            coincident_sizing_factor_mode: int = 1):
        """
        -Loop_type: 1:Cooling 2:Heating 3:Condenser 4:Steam \n

        -Sizing_option:
        1: Coincident
        2: NonCoincident
        (Default is NonCoincident) \n

        -Coincident_sizing_factor_mode: \n
        1: None \n
        2: GlobalCoolingSizingFactor \n
        3: GlobalHeatingSizingFactor \n
        4: LoopComponentSizingFactor
        """

        loop_types = {1: "Cooling", 2: "Heating", 3: "Condenser", 4: "Steam"}
        sizing_options = {1: "Coincident", 2: "NonCoincident"}
        sizing_factor_modes = {1: "None", 2: "GlobalCoolingSizingFactor",
                               3: "GlobalHeatingSizingFactor", 4: "LoopComponentSizingFactor"}
        sizing = idf.newidfobject('Sizing:Plant')

        if isinstance(plantloop, EpBunch):
            sizing['Plant_or_Condenser_Loop_Name'] = plantloop.Name
        elif isinstance(plantloop, str):
            sizing['Plant_or_Condenser_Loop_Name'] = plantloop
        else:
            raise TypeError('Invalid input type of plantloop.')

        sizing['Loop_Type'] = loop_types[loop_type]

        if loop_exit_temp is not None:
            sizing['Design_Loop_Exit_Temperature'] = loop_exit_temp
        else:
            match loop_type:
                case 1:
                    sizing['Design_Loop_Exit_Temperature'] = 7.0
                case 2:
                    sizing['Design_Loop_Exit_Temperature'] = 50
                case 3:
                    sizing['Design_Loop_Exit_Temperature'] = 30
                case 4:
                    sizing['Design_Loop_Exit_Temperature'] = 100
        if loop_temp_diff is not None:
            sizing['Loop_Design_Temperature_Difference'] = loop_temp_diff
        else:
            match loop_type:
                case 1:
                    sizing['Loop_Design_Temperature_Difference'] = 6
                case 2:
                    sizing['Loop_Design_Temperature_Difference'] = 50
                case 3:
                    sizing['Loop_Design_Temperature_Difference'] = 15
                case 4:
                    sizing['Loop_Design_Temperature_Difference'] = 50

        if zone_timesteps_in_averaging_window is not None:
            sizing['Zone_Timesteps_in_Averaging_Window'] = zone_timesteps_in_averaging_window

        sizing['Sizing_Option'] = sizing_options[sizing_option]
        sizing['Coincident_Sizing_Factor_Mode'] = sizing_factor_modes[coincident_sizing_factor_mode]

        return sizing

    # ***************************************************************************************************
    # Equipment Operation Schemes
    @staticmethod
    def equip_operation_schemes(
            idf: IDF,
            plant_name: str = None,
            scheme_types: list[int] = None,):
        """
        Scheme Object Type: \n
        1.PlantEquipmentOperation:Uncontrolled
        2.PlantEquipmentOperation:CoolingLoad
        3.PlantEquipmentOperation:HeatingLoad
        4.PlantEquipmentOperation:OutdoorDryBulb
        5.PlantEquipmentOperation:OutdoorWetBulb
        6.PlantEquipmentOperation:OutdoorRelativeHumidity
        7.PlantEquipmentOperation:OutdoorDewpoint
        8.PlantEquipmentOperation:OutdoorDryBulbDifference
        9.PlantEquipmentOperation:OutdoorWetBulbDifference
        10.PlantEquipmentOperation:OutdoorDewpointDifference
        11.PlantEquipmentOperation:ComponentSetpoint
        12.PlantEquipmentOperation:ThermalEnergyStorage
        13.PlantEquipmentOperation:UserDefined
        14.PlantEquipmentOperation:ChillerHeaterChangeover
        """
        object_types = {1: "PlantEquipmentOperation:Uncontrolled",
                        2: "PlantEquipmentOperation:CoolingLoad",
                        3: "PlantEquipmentOperation:HeatingLoad",
                        4: "PlantEquipmentOperation:OutdoorDryBulb",
                        5: "PlantEquipmentOperation:OutdoorWetBulb",
                        6: "PlantEquipmentOperation:OutdoorRelativeHumidity",
                        7: "PlantEquipmentOperation:OutdoorDewpoint",
                        8: "PlantEquipmentOperation:OutdoorDryBulbDifference",
                        9: "PlantEquipmentOperation:OutdoorWetBulbDifference",
                        10: "PlantEquipmentOperation:OutdoorDewpointDifference",
                        11: "PlantEquipmentOperation:ComponentSetpoint",
                        12: "PlantEquipmentOperation:ThermalEnergyStorage",
                        13: "PlantEquipmentOperation:UserDefined",
                        14: "PlantEquipmentOperation:ChillerHeaterChangeover"}

        plant_name = 'Plant Loop' if plant_name is None else plant_name
        scheme_name = f'{plant_name} Operation Schemes'
        scheme = idf.newidfobject('PlantEquipmentOperation:Schemes', Name=scheme_name)

    @staticmethod
    def pipe(idf: IDF, name=None, pipe_type: int = 1):
        """
        -Pipe_type:
            1:Adiabatic 2:Indoor 3:Outdoor 4:Adiabatic:Steam 5: Underground
        """
        pipe_types = {1: "Pipe:Adiabatic", 2: "Pipe:Indoor", 3: "Pipe:Outdoor",
                      4: "Pipe:Adiabatic:Steam", 5: "Pipe:Underground"}

        name = f'Pipe_{pipe_types[pipe_type].split(":")[-1]}' if name is None else name
        pipe = idf.newidfobject(pipe_types[pipe_type], Name=name)
        pipe.Inlet_Node_Name = f'{name}_inlet'
        pipe.Outlet_Node_Name = f'{name}_outlet'

        component = {
            'object': pipe,
            'type': pipe_types[pipe_type],
            'water_inlet_field': 'Inlet_Node_Name',
            'water_outlet_field': 'Outlet_Node_Name',
        }

        return component

    # ***************************************************************************************************
    # Cooling Equipments
    @staticmethod
    def chiller_electric(
            idf: IDF,
            name: str = None,
            condenser_type: int = 1,
            capacity='Autosize',
            cop=5.5,
            leaving_chilled_water_temp=6,
            entering_condenser_water_temp=29,
            chilled_water_flow_rate='Autosize',
            condenser_water_flow_rate='Autosize',
            min_part_load_ratio=0.1,
            max_part_load_ratio=1,
            optimal_part_load_ratio=1,
            min_unload_ratio=0.2,
            condenser_fan_power_ratio=0,
            compressor_by_condenser_fraction=1,
            leaving_chilled_water_low_limit=2,
            chiller_flow_mode: int = 2,
            sizing_factor=1,
            design_heat_recovery_flow_rate=None,
            condenser_heat_recovery_capacity_fraction=1,
            heat_recovery_inlet_high_temp_limit_schedule=None,
            heat_recovery_leaving_temp_node=None,
            basin_heat_capacity=0,
            basin_heater_setpoint_temp=10,
            basin_heater_schedule=None,
            capacity_temperature_curve: EpBunch | str = None,
            cop_temperature_curve: EpBunch | str = None,
            cop_plr_curve: EpBunch | str = None,
            condenser_loop=None,
            condenser_flow_control: int = 1,
            test_mode: bool = False):

        """
        -Condenser_type: 1:AirCooled 2:WaterCooled 3:EvapCooled \n
        -Chiller_flow_mode: 1:NotModulated 2:LeavingSetpointModulated 3:ConstantFlow
        -Condenser Flow Control: 1:ConstantFlow 2:ModulatedChillerPLR 3:ModulatedLoopPLR 4:ModulatedDeltaTemperature
        """

        condenser_types = {1: "AirCooled", 2: "WaterCooled", 3: "EvapCooled"}
        flow_modes = {1: "NotModulated", 2: "LeavingSetpointModulated", 3: "ConstantFlow"}
        chiller_assembly = []

        name = f'Chiller {condenser_types[condenser_type]}' if name is None else name

        chiller = idf.newidfobject('Chiller:Electric:EIR', Name=name)

        chiller['Condenser_Type'] = condenser_types[condenser_type]
        chiller['Reference_Capacity'] = capacity
        chiller['Reference_COP'] = cop
        chiller['Reference_Leaving_Chilled_Water_Temperature'] = leaving_chilled_water_temp
        chiller['Reference_Entering_Condenser_Fluid_Temperature'] = entering_condenser_water_temp
        chiller['Reference_Chilled_Water_Flow_Rate'] = chilled_water_flow_rate
        chiller['Reference_Condenser_Fluid_Flow_Rate'] = condenser_water_flow_rate
        chiller['Minimum_Part_Load_Ratio'] = min_part_load_ratio
        chiller['Maximum_Part_Load_Ratio'] = max_part_load_ratio
        chiller['Optimum_Part_Load_Ratio'] = optimal_part_load_ratio
        chiller['Minimum_Unloading_Ratio'] = min_unload_ratio
        chiller['Condenser_Fan_Power_Ratio'] = condenser_fan_power_ratio
        chiller['Fraction_of_Compressor_Electric_Consumption_Rejected_by_Condenser'] = compressor_by_condenser_fraction
        chiller['Leaving_Chilled_Water_Lower_Temperature_Limit'] = leaving_chilled_water_low_limit
        chiller['Chiller_Flow_Mode'] = flow_modes[chiller_flow_mode]
        chiller['Sizing_Factor'] = sizing_factor

        chiller['Condenser_Heat_Recovery_Relative_Capacity_Fraction'] = condenser_heat_recovery_capacity_fraction
        if design_heat_recovery_flow_rate is not None:
            chiller['Design_Heat_Recovery_Water_Flow_Rate'] = design_heat_recovery_flow_rate
        if heat_recovery_inlet_high_temp_limit_schedule is not None:
            chiller[
                'Heat_Recovery_Inlet_High_Temperature_Limit_Schedule_Name'] = heat_recovery_inlet_high_temp_limit_schedule
        if heat_recovery_leaving_temp_node is not None:
            chiller['Heat_Recovery_Leaving_Temperature_Setpoint_Node_Name'] = heat_recovery_leaving_temp_node

        chiller['Basin_Heater_Capacity'] = basin_heat_capacity
        chiller['Basin_Heater_Setpoint_Temperature'] = basin_heater_setpoint_temp
        if basin_heater_schedule is not None:
            chiller['Basin_Heater_Operating_Schedule_Name'] = basin_heater_schedule

        # Performance Curves:
        curve_set = PerformanceCurve.chiller_performance_curve_ashrae_baseline(idf, name=name)

        if capacity_temperature_curve is not None:
            if isinstance(capacity_temperature_curve, str):
                chiller['Cooling_Capacity_Function_of_Temperature_Curve_Name'] = capacity_temperature_curve
            elif isinstance(capacity_temperature_curve, EpBunch):
                chiller['Cooling_Capacity_Function_of_Temperature_Curve_Name'] = capacity_temperature_curve.Name
            else:
                raise TypeError('capacity_temperature_curve must be EpBunch or str')
        else:
            chiller['Cooling_Capacity_Function_of_Temperature_Curve_Name'] = curve_set[0].Name

        if cop_temperature_curve is not None:
            if isinstance(cop_temperature_curve, str):
                chiller[
                    'Electric_Input_to_Cooling_Output_Ratio_Function_of_Temperature_Curve_Name'] = cop_temperature_curve
            elif isinstance(cop_temperature_curve, EpBunch):
                chiller[
                    'Electric_Input_to_Cooling_Output_Ratio_Function_of_Temperature_Curve_Name'] = cop_temperature_curve.Name
            else:
                raise TypeError('cop_temperature_curve must be EpBunch or str')
        else:
            chiller['Electric_Input_to_Cooling_Output_Ratio_Function_of_Temperature_Curve_Name'] = curve_set[1].Name

        if cop_plr_curve is not None:
            if isinstance(cop_plr_curve, str):
                chiller['Electric_Input_to_Cooling_Output_Ratio_Function_of_Part_Load_Ratio_Curve_Name'] = cop_plr_curve
            elif isinstance(cop_plr_curve, EpBunch):
                chiller[
                    'Electric_Input_to_Cooling_Output_Ratio_Function_of_Part_Load_Ratio_Curve_Name'] = cop_plr_curve.Name
            else:
                raise TypeError('cop_plr_curve must be EpBunch or str')
        else:
            chiller['Electric_Input_to_Cooling_Output_Ratio_Function_of_Part_Load_Ratio_Curve_Name'] = curve_set[2].Name

        chiller['Chilled_Water_Inlet_Node_Name'] = f'{name} Chilled_Water_Inlet'
        chiller['Chilled_Water_Outlet_Node_Name'] = f'{name} Chilled_Water_Outlet'
        if condenser_type == 2:
            chiller['Condenser_Inlet_Node_Name'] = f'{name} Condenser_Water_Inlet'
            chiller['Condenser_Outlet_Node_Name'] = f'{name} Condenser_Water_Outlet'
        if design_heat_recovery_flow_rate is not None:
            chiller['Heat_Recovery_Inlet_Node_Name'] = f'{name} Heat_Recovery_Inlet'
            chiller['Heat_Recovery_Outlet_Node_Name'] = f'{name} Heat_Recovery_Outlet'

        chiller['EndUse_Subcategory'] = 'General'

        comp = {
            'object': chiller,
            'type': 'Chiller:Electric:EIR',
            'water_inlet_field': 'Chilled_Water_Inlet_Node_Name',
            'water_outlet_field': 'Chilled_Water_Outlet_Node_Name',
            'condenser_water_inlet_field': 'Condenser_Inlet_Node_Name',
            'condenser_water_outlet_field': 'Condenser_Outlet_Node_Name',
        }

        if test_mode:
            chiller_assembly.append(chiller)
            chiller_assembly.extend(curve_set)
            return chiller_assembly
        else:
            return comp

    @staticmethod
    def district_cooling(
            idf: IDF,
            name: str = None,
            nominal_capacity='Autosize',
            capacity_fraction_schedule: EpBunch | str = None):

        name = 'District Cooling' if name is None else name
        district = idf.newidfobject('DistrictCooling', Name=name)

        district['Nominal_Capacity'] = nominal_capacity

        if capacity_fraction_schedule is not None:
            if isinstance(capacity_fraction_schedule, str):
                district['Capacity_Fraction_Schedule_Name'] = capacity_fraction_schedule
            elif isinstance(capacity_fraction_schedule, EpBunch):
                district['Capacity_Fraction_Schedule_Name'] = capacity_fraction_schedule.Name
            else:
                raise TypeError('capacity_fraction_schedule must be EpBunch or str')

        district['Chilled_Water_Inlet_Node_Name'] = f'{name} Chilled_Water_Inlet'
        district['Chilled_Water_Outlet_Node_Name'] = f'{name} Chilled_Water_Outlet'

        comp = {
            'object': district,
            'type': 'DistrictCooling',
            'water_inlet_field': 'Chilled_Water_Inlet_Node_Name',
            'water_outlet_field': 'Chilled_Water_Outlet_Node_Name',
        }

        return comp

    # ***************************************************************************************************
    # Heating Equipments
    @staticmethod
    def district_heating(
            idf: IDF,
            name: str = None,
            nominal_capacity='Autosize',
            capacity_fraction_schedule: EpBunch | str = None):

        name = 'District Heating' if name is None else name
        district = idf.newidfobject('DistrictHeating', Name=name)

        district['Nominal_Capacity'] = nominal_capacity

        if capacity_fraction_schedule is not None:
            if isinstance(capacity_fraction_schedule, str):
                district['Capacity_Fraction_Schedule_Name'] = capacity_fraction_schedule
            elif isinstance(capacity_fraction_schedule, EpBunch):
                district['Capacity_Fraction_Schedule_Name'] = capacity_fraction_schedule.Name
            else:
                raise TypeError('capacity_fraction_schedule must be EpBunch or str')

        district['Hot_Water_Inlet_Node_Name'] = f'{name} Hot_Water_Inlet'
        district['Hot_Water_Outlet_Node_Name'] = f'{name} Hot_Water_Outlet'

        comp = {
            'object': district,
            'type': 'DistrictHeating',
            'water_inlet_field': 'Hot_Water_Inlet_Node_Name',
            'water_outlet_field': 'Hot_Water_Outlet_Node_Name',
        }

        return comp

    @staticmethod
    def district_heating_v24(
            idf: IDF,
            name: str = None,
            nominal_capacity='Autosize',
            capacity_fraction_schedule: EpBunch | str = None):

        name = 'District Heating' if name is None else name
        district = idf.newidfobject('DistrictHeating:Water', Name=name)

        district['Nominal_Capacity'] = nominal_capacity

        if capacity_fraction_schedule is not None:
            if isinstance(capacity_fraction_schedule, str):
                district['Capacity_Fraction_Schedule_Name'] = capacity_fraction_schedule
            elif isinstance(capacity_fraction_schedule, EpBunch):
                district['Capacity_Fraction_Schedule_Name'] = capacity_fraction_schedule.Name
            else:
                raise TypeError('capacity_fraction_schedule must be EpBunch or str')

        district['Hot_Water_Inlet_Node_Name'] = f'{name} Hot_Water_Inlet'
        district['Hot_Water_Outlet_Node_Name'] = f'{name} Hot_Water_Outlet'

        comp = {
            'object': district,
            'type': 'DistrictHeating:Water',
            'water_inlet_field': 'Hot_Water_Inlet_Node_Name',
            'water_outlet_field': 'Hot_Water_Outlet_Node_Name',
        }

        return comp

    # ***************************************************************************************************
    # Condenser Equipments
    @staticmethod
    def cooling_tower_single_speed(
            idf: IDF,
            name: str = None,
            design_water_flow_rate='Autosize',
            design_air_flow_rate='Autosize',
            fan_power_at_design_air_flow='Autosize',
            u_factor_area_at_design_air_flow='Autosize',
            air_flow_rate_in_free_convection='Autosize',
            air_flow_rate_in_free_convection_sizing_factor=0.1,
            u_factor_area_at_free_convection='Autosize',
            u_factor_area_at_free_convection_sizing_factor=0.1,
            performance_input_method: int = 1,
            heat_rejection_capacity_nominal_capacity_sizing_ratio=1.25,
            nominal_capacity=None,
            free_convection_capacity=0,
            free_convection_nominal_cap_sizing_factor=0.1,
            basin_heater_capacity=0,
            basin_heater_setpoint_temp=2,
            basin_heater_schedule=None,
            evaporation_loss_mode: int = 1,
            evaporation_loss_factor=0.2,
            drift_loss_percent=0.008,
            blowdown_calculation_mode: int = 1,
            blowdown_concentration_ratio=3,
            blowdown_markup_water_schedule=None,
            capacity_control: int = 1,
            number_of_cells=1,
            cell_control: int = 1,
            cell_min_water_flow_fraction=0.33,
            cell_max_water_flow_fraction=2.5,
            sizing_factor=1,
            design_inlet_air_dry_bulb_temp=35.0,
            design_inlet_air_wet_bulb_temp=25.6,
            design_approach_temp='Autosize',
            design_range_temp='Autosize'):

        """
        -Performance_input_method: 1:UFactorTimesAreaAndDesignWaterFlowRate 2:NominalCapacity
        -Evaporation_loss_mode: 1:LossFactor 2:SaturatedExit
        -Blowdown_calculation_mode: 1:ConcentrationRatio 2:ScheduledRate
        -Capacity_control: 1:FanCycling 2:FluidBypass
        -Cell_control: 1:MinimalCell 2:MaximalCell
        """

        performance_methods = {1: "UFactorTimesAreaAndDesignWaterFlowRate", 2: "NominalCapacity"}
        evap_loss_modes = {1: "LossFactor", 2: "SaturatedExit"}
        blowdown_modes = {1: "ConcentrationRatio", 2: "ScheduledRate"}
        capacity_controls = {1: "FanCycling", 2: "FluidBypass"}
        cell_controls = {1: "MinimalCell", 2: "MaximalCell"}

        name = 'Cooling Tower Single Speed' if name is None else name
        tower = idf.newidfobject('CoolingTower:SingleSpeed', Name=name)

        tower['Design_Water_Flow_Rate'] = design_water_flow_rate
        tower['Design_Air_Flow_Rate'] = design_air_flow_rate
        tower['Design_Fan_Power'] = fan_power_at_design_air_flow
        tower['Design_UFactor_Times_Area_Value'] = u_factor_area_at_design_air_flow
        tower['Free_Convection_Regime_Air_Flow_Rate'] = air_flow_rate_in_free_convection
        tower['Free_Convection_Regime_Air_Flow_Rate_Sizing_Factor'] = air_flow_rate_in_free_convection_sizing_factor
        tower['Free_Convection_Regime_UFactor_Times_Area_Value'] = u_factor_area_at_free_convection
        tower['Free_Convection_UFactor_Times_Area_Value_Sizing_Factor'] = u_factor_area_at_free_convection_sizing_factor
        tower['Performance_Input_Method'] = performance_methods[performance_input_method]
        tower['Heat_Rejection_Capacity_and_Nominal_Capacity_Sizing_Ratio'] = heat_rejection_capacity_nominal_capacity_sizing_ratio
        if nominal_capacity is not None:
            tower['Nominal_Capacity'] = nominal_capacity
        tower['Free_Convection_Capacity'] = free_convection_capacity
        tower['Free_Convection_Nominal_Capacity_Sizing_Factor'] = free_convection_nominal_cap_sizing_factor
        tower['Basin_Heater_Capacity'] = basin_heater_capacity
        tower['Basin_Heater_Setpoint_Temperature'] = basin_heater_setpoint_temp
        if basin_heater_schedule is not None:
            if isinstance(basin_heater_schedule, str):
                tower['Basin_Heater_Operating_Schedule_Name'] = basin_heater_schedule
            elif isinstance(basin_heater_schedule, EpBunch):
                tower['Basin_Heater_Operating_Schedule_Name'] = basin_heater_schedule.Name
            else:
                raise TypeError('basin_heater_schedule must be EpBunch or str')
        tower['Evaporation_Loss_Mode'] = evap_loss_modes[evaporation_loss_mode]
        tower['Evaporation_Loss_Factor'] = evaporation_loss_factor
        tower['Drift_Loss_Percent'] = drift_loss_percent
        tower['Blowdown_Calculation_Mode'] = blowdown_modes[blowdown_calculation_mode]
        tower['Blowdown_Concentration_Ratio'] = blowdown_concentration_ratio
        if blowdown_markup_water_schedule is not None:
            if isinstance(blowdown_markup_water_schedule, str):
                tower['Blowdown_Makeup_Water_Usage_Schedule_Name'] = blowdown_markup_water_schedule
            elif isinstance(blowdown_markup_water_schedule, EpBunch):
                tower['Blowdown_Makeup_Water_Usage_Schedule_Name'] = blowdown_markup_water_schedule.Name
            else:
                raise TypeError('blowdown_markup_water_schedule must be EpBunch or str')
        tower['Capacity_Control'] = capacity_controls[capacity_control]
        tower['Number_of_Cells'] = number_of_cells
        tower['Cell_Control'] = cell_controls[cell_control]
        tower['Cell_Minimum_Water_Flow_Rate_Fraction'] = cell_min_water_flow_fraction
        tower['Cell_Maximum_Water_Flow_Rate_Fraction'] = cell_max_water_flow_fraction
        tower['Sizing_Factor'] = sizing_factor
        tower['Design_Inlet_Air_DryBulb_Temperature'] = design_inlet_air_dry_bulb_temp
        tower['Design_Inlet_Air_WetBulb_Temperature'] = design_inlet_air_wet_bulb_temp
        tower['Design_Approach_Temperature'] = design_approach_temp
        tower['Design_Range_Temperature'] = design_range_temp

        tower['Water_Inlet_Node_Name'] = f'{name} Water_Inlet'
        tower['Water_Outlet_Node_Name'] = f'{name} Water_Outlet'

        comp = {
            'object': tower,
            'type': 'CoolingTower:SingleSpeed',
            'water_inlet_field': 'Water_Inlet_Node_Name',
            'water_outlet_field': 'Water_Outlet_Node_Name',
        }

        return comp

    # ***************************************************************************************************
    # Distribution Equipments
    @staticmethod
    def pump_variable_speed(
            idf: IDF,
            name: str = None,
            design_head=179352,
            design_max_flow_rate='Autosize',
            design_min_flow_rate=0,
            design_power='Autosize',
            motor_efficiency=0.9,
            fraction_of_motor_to_fluid=0,
            control_type: int = 1,
            vfd_control_type: int = None,
            pump_flow_rate_schedule: EpBunch | str = None,
            pump_rpm_schedule: EpBunch | str = None,
            min_rpm_schedule: EpBunch | str = None,
            max_pressure_schedule: EpBunch | str = None,
            min_pressure_schedule: EpBunch | str = None,
            impeller_diameter=None,
            power_sizing_method: int = 1,
            power_per_flow_rate=348701.1,
            power_per_flow_rate_per_head=1.282051282,
            thermal_zone=None,
            skin_loss_radiative_fraction=0.5,
            design_min_flow_fraction=0,
            pump_curve_coeff=PerformanceCurve.pump_curve_set(1)):
        """
        -Control_type: 1:Intermittent 2:Continuous \n
        -VFD_control_type: 1:PressureSetPointControl 2:ManualControl \n
        -Power_sizing_method: 1:PowerPerFlowPerPressure 2:PowerPerFlow
        """

        control_types = {1: "Intermittent", 2: "Continuous"}
        vfd_control_types = {1: "PressureSetPointControl", 2: "ManualControl"}
        sizing_methods = {1: "PowerPerFlowPerPressure", 2: "PowerPerFlow"}
        pump_assembly = []

        name = 'Pump Variable Speed' if name is None else name
        pump = idf.newidfobject('Pump:VariableSpeed', Name=name)

        pump['Design_Maximum_Flow_Rate'] = design_max_flow_rate
        pump['Design_Minimum_Flow_Rate'] = design_min_flow_rate
        pump['Design_Pump_Head'] = design_head
        pump['Design_Power_Consumption'] = design_power
        pump['Motor_Efficiency'] = motor_efficiency
        pump['Fraction_of_Motor_Inefficiencies_to_Fluid_Stream'] = fraction_of_motor_to_fluid
        pump['Pump_Control_Type'] = control_types[control_type]

        if pump_flow_rate_schedule is not None:
            if isinstance(pump_flow_rate_schedule, str):
                pump['Pump_Flow_Rate_Schedule_Name'] = pump_flow_rate_schedule
            elif isinstance(pump_flow_rate_schedule, EpBunch):
                pump['Pump_Flow_Rate_Schedule_Name'] = pump_flow_rate_schedule.Name
            else:
                raise TypeError('pump_flow_rate_schedule must be EpBunch or str')
        if max_pressure_schedule is not None:
            if isinstance(max_pressure_schedule, str):
                pump['Maximum_Flow_Rate_Schedule_Name'] = max_pressure_schedule
            elif isinstance(max_pressure_schedule, EpBunch):
                pump['Maximum_Flow_Rate_Schedule_Name'] = max_pressure_schedule.Name
            else:
                raise TypeError('max_pressure_schedule must be EpBunch or str')
        if min_pressure_schedule is not None:
            if isinstance(min_pressure_schedule, str):
                pump['Minimum_Flow_Rate_Schedule_Name'] = min_pressure_schedule
            elif isinstance(min_pressure_schedule, EpBunch):
                pump['Minimum_Flow_Rate_Schedule_Name'] = min_pressure_schedule.Name
            else:
                raise TypeError('min_pressure_schedule must be EpBunch or str')
        if pump_rpm_schedule is not None:
            if isinstance(pump_rpm_schedule, str):
                pump['Pump_RPM_Schedule_Name'] = pump_rpm_schedule
            elif isinstance(pump_rpm_schedule, EpBunch):
                pump['Pump_RPM_Schedule_Name'] = pump_rpm_schedule.Name
            else:
                raise TypeError('pump_rpm_schedule must be EpBunch or str')
        if min_rpm_schedule is not None:
            if isinstance(min_rpm_schedule, str):
                pump['Minimum_RPM_Schedule_Name'] = min_rpm_schedule
            elif isinstance(min_rpm_schedule, EpBunch):
                pump['Minimum_RPM_Schedule_Name'] = min_rpm_schedule.Name
            else:
                raise TypeError('min_rpm_schedule must be EpBunch or str')

        if impeller_diameter is not None:
            pump['Impeller_Diameter'] = impeller_diameter
        if vfd_control_type is not None:
            pump['VFD_Control_Type'] = vfd_control_types[vfd_control_type]

        if thermal_zone is not None:
            pump['Zone_Name'] = thermal_zone

        pump['Skin_Loss_Radiative_Fraction'] = skin_loss_radiative_fraction
        pump['Design_Power_Sizing_Method'] = sizing_methods[power_sizing_method]
        pump['Design_Electric_Power_per_Unit_Flow_Rate'] = power_per_flow_rate
        pump['Design_Shaft_Power_per_Unit_Flow_Rate_per_Unit_Head'] = power_per_flow_rate_per_head
        pump['Design_Minimum_Flow_Rate_Fraction'] = design_min_flow_fraction
        pump['EndUse_Subcategory'] = 'General'

        pump['Coefficient_1_of_the_Part_Load_Performance_Curve'] = pump_curve_coeff[0]
        pump['Coefficient_2_of_the_Part_Load_Performance_Curve'] = pump_curve_coeff[1]
        pump['Coefficient_3_of_the_Part_Load_Performance_Curve'] = pump_curve_coeff[2]
        pump['Coefficient_4_of_the_Part_Load_Performance_Curve'] = pump_curve_coeff[3]

        pump['Inlet_Node_Name'] = f'{name}_Water_Inlet'
        pump['Outlet_Node_Name'] = f'{name}_Water_Outlet'

        comp = {
            'object': pump,
            'type': 'Pump:VariableSpeed',
            'water_inlet_field': 'Inlet_Node_Name',
            'water_outlet_field': 'Outlet_Node_Name'
        }

        return comp

    @staticmethod
    def pump_constant_speed(
            idf: IDF,
            name: str = None,
            design_head=179352,
            design_max_flow_rate='Autosize',
            design_min_flow_rate=0,
            design_power='Autosize',
            motor_efficiency=0.9,
            fraction_of_motor_to_fluid=0,
            control_type: int = 1,
            pump_flow_rate_schedule: EpBunch | str = None,
            impeller_diameter=None,
            rotational_speed=None,
            power_sizing_method: int = 1,
            power_per_flow_rate=348701.1,
            power_per_flow_rate_per_head=1.282051282,
            thermal_zone=None):

        """
        -Control_type: 1:Intermittent 2:Continuous \n
        -Power_sizing_method: 1:PowerPerFlowPerPressure 2:PowerPerFlow
        """

        control_types = {1: "Intermittent", 2: "Continuous"}
        sizing_methods = {1: "PowerPerFlowPerPressure", 2: "PowerPerFlow"}

        name = 'Pump Constant Speed' if name is None else name
        pump = idf.newidfobject('Pump:ConstantSpeed', Name=name)

        pump['Design_Maximum_Flow_Rate'] = design_max_flow_rate
        pump['Design_Minimum_Flow_Rate'] = design_min_flow_rate
        pump['Design_Pump_Head'] = design_head
        pump['Design_Power_Consumption'] = design_power
        pump['Motor_Efficiency'] = motor_efficiency
        pump['Fraction_of_Motor_Inefficiencies_to_Fluid_Stream'] = fraction_of_motor_to_fluid
        pump['Pump_Control_Type'] = control_types[control_type]

        if pump_flow_rate_schedule is not None:
            if isinstance(pump_flow_rate_schedule, str):
                pump['Pump_Flow_Rate_Schedule_Name'] = pump_flow_rate_schedule
            elif isinstance(pump_flow_rate_schedule, EpBunch):
                pump['Pump_Flow_Rate_Schedule_Name'] = pump_flow_rate_schedule.Name
            else:
                raise TypeError('pump_flow_rate_schedule must be EpBunch or str')

        if impeller_diameter is not None:
            pump['Impeller_Diameter'] = impeller_diameter
        if rotational_speed is not None:
            pump['Rotational_Speed'] = rotational_speed
        if thermal_zone is not None:
            pump['Zone_Name'] = thermal_zone
        pump['Design_Power_Sizing_Method'] = sizing_methods[power_sizing_method]
        pump['Design_Electric_Power_per_Unit_Flow_Rate'] = power_per_flow_rate
        pump['Design_Shaft_Power_per_Unit_Flow_Rate_per_Unit_Head'] = power_per_flow_rate_per_head
        pump['EndUse_Subcategory'] = 'General'

        pump['Inlet_Node_Name'] = f'{name}_Water_Inlet'
        pump['Outlet_Node_Name'] = f'{name}_Water_Outlet'

        comp = {
            'object': pump,
            'type': 'Pump:ConstantSpeed',
            'water_inlet_field': 'Inlet_Node_Name',
            'water_outlet_field': 'Outlet_Node_Name'
        }

        return comp

    @staticmethod
    def headered_pumps_variable_speed(
            idf: IDF,
            name: str = None,
            total_design_flow_rate='Autosize',
            number_of_pumps_in_bank: int = 2,
            design_head=179352,
            design_power='Autosize',
            sequence_control_scheme='Sequential',
            motor_efficiency=0.9,
            fraction_of_motor_to_fluid=0,
            min_flow_rate_fraction=0,
            control_type: int = 1,
            pump_flow_rate_schedule: EpBunch | str = None,
            power_sizing_method: int = 1,
            power_per_flow_rate=348701.1,
            power_per_flow_rate_per_head=1.282051282,
            thermal_zone=None,
            skin_loss_radiative_fraction=0.5,
            pump_curve_coeff=PerformanceCurve.pump_curve_set(1)):

        """
        -Control_type: 1:Intermittent 2:Continuous \n
        -Power_sizing_method: 1:PowerPerFlowPerPressure 2:PowerPerFlow
        """

        control_types = {1: "Intermittent", 2: "Continuous"}
        sizing_methods = {1: "PowerPerFlowPerPressure", 2: "PowerPerFlow"}

        name = 'Headered Pumps Variable Speed' if name is None else name
        pump = idf.newidfobject('HeaderedPumps:VariableSpeed', Name=name)

        pump['Total_Design_Flow_Rate'] = total_design_flow_rate
        pump['Number_of_Pumps_in_Bank'] = number_of_pumps_in_bank
        pump['Flow_Sequencing_Control_Scheme'] = sequence_control_scheme
        pump['Design_Pump_Head'] = design_head
        pump['Design_Power_Consumption'] = design_power
        pump['Motor_Efficiency'] = motor_efficiency
        pump['Fraction_of_Motor_Inefficiencies_to_Fluid_Stream'] = fraction_of_motor_to_fluid
        pump['Minimum_Flow_Rate_Fraction'] = min_flow_rate_fraction
        pump['Pump_Control_Type'] = control_types[control_type]

        if pump_flow_rate_schedule is not None:
            if isinstance(pump_flow_rate_schedule, str):
                pump['Pump_Flow_Rate_Schedule_Name'] = pump_flow_rate_schedule
            elif isinstance(pump_flow_rate_schedule, EpBunch):
                pump['Pump_Flow_Rate_Schedule_Name'] = pump_flow_rate_schedule.Name
            else:
                raise TypeError('pump_flow_rate_schedule must be EpBunch or str')
        pump['Design_Power_Sizing_Method'] = sizing_methods[power_sizing_method]
        pump['Design_Electric_Power_per_Unit_Flow_Rate'] = power_per_flow_rate
        pump['Design_Shaft_Power_per_Unit_Flow_Rate_per_Unit_Head'] = power_per_flow_rate_per_head
        pump['Skin_Loss_Radiative_Fraction'] = skin_loss_radiative_fraction

        if thermal_zone is not None:
            pump['Zone_Name'] = thermal_zone

        pump['EndUse_Subcategory'] = 'General'

        pump['Coefficient_1_of_the_Part_Load_Performance_Curve'] = pump_curve_coeff[0]
        pump['Coefficient_2_of_the_Part_Load_Performance_Curve'] = pump_curve_coeff[1]
        pump['Coefficient_3_of_the_Part_Load_Performance_Curve'] = pump_curve_coeff[2]
        pump['Coefficient_4_of_the_Part_Load_Performance_Curve'] = pump_curve_coeff[3]

        pump['Inlet_Node_Name'] = f'{name}_Water_Inlet'
        pump['Outlet_Node_Name'] = f'{name}_Water_Outlet'

        comp = {
            'object': pump,
            'type': 'HeaderedPumps:VariableSpeed',
            'water_inlet_field': 'Inlet_Node_Name',
            'water_outlet_field': 'Outlet_Node_Name'
        }

        return comp

    @staticmethod
    def headered_pumps_constant_speed(
            idf: IDF,
            name: str = None,
            total_design_flow_rate='Autosize',
            number_of_pumps_in_bank: int = 2,
            design_head=179352,
            design_power='Autosize',
            sequence_control_scheme='Sequential',
            motor_efficiency=0.9,
            fraction_of_motor_to_fluid=0,
            control_type: int = 1,
            pump_flow_rate_schedule: EpBunch | str = None,
            power_sizing_method: int = 1,
            power_per_flow_rate=348701.1,
            power_per_flow_rate_per_head=1.282051282,
            thermal_zone=None,
            skin_loss_radiative_fraction=0.5):

        """
        -Control_type: 1:Intermittent 2:Continuous \n
        -Power_sizing_method: 1:PowerPerFlowPerPressure 2:PowerPerFlow
        """

        control_types = {1: "Intermittent", 2: "Continuous"}
        sizing_methods = {1: "PowerPerFlowPerPressure", 2: "PowerPerFlow"}

        pump = idf.newidfobject('HeaderedPumps:ConstantSpeed', Name=name)

        pump['Total_Design_Flow_Rate'] = total_design_flow_rate
        pump['Number_of_Pumps_in_Bank'] = number_of_pumps_in_bank
        pump['Flow_Sequencing_Control_Scheme'] = sequence_control_scheme
        pump['Design_Pump_Head'] = design_head
        pump['Design_Power_Consumption'] = design_power
        pump['Motor_Efficiency'] = motor_efficiency
        pump['Fraction_of_Motor_Inefficiencies_to_Fluid_Stream'] = fraction_of_motor_to_fluid
        pump['Pump_Control_Type'] = control_types[control_type]

        if pump_flow_rate_schedule is not None:
            if isinstance(pump_flow_rate_schedule, str):
                pump['Pump_Flow_Rate_Schedule_Name'] = pump_flow_rate_schedule
            elif isinstance(pump_flow_rate_schedule, EpBunch):
                pump['Pump_Flow_Rate_Schedule_Name'] = pump_flow_rate_schedule.Name
            else:
                raise TypeError('pump_flow_rate_schedule must be EpBunch or str')
        pump['Design_Power_Sizing_Method'] = sizing_methods[power_sizing_method]
        pump['Design_Electric_Power_per_Unit_Flow_Rate'] = power_per_flow_rate
        pump['Design_Shaft_Power_per_Unit_Flow_Rate_per_Unit_Head'] = power_per_flow_rate_per_head
        pump['Skin_Loss_Radiative_Fraction'] = skin_loss_radiative_fraction

        if thermal_zone is not None:
            pump['Zone_Name'] = thermal_zone

        pump['EndUse_Subcategory'] = 'General'

        pump['Inlet_Node_Name'] = f'{name}_Water_Inlet'
        pump['Outlet_Node_Name'] = f'{name}_Water_Outlet'

        comp = {
            'object': pump,
            'type': 'HeaderedPumps:ConstantSpeed',
            'water_inlet_field': 'Inlet_Node_Name',
            'water_outlet_field': 'Outlet_Node_Name'
        }

        return comp
