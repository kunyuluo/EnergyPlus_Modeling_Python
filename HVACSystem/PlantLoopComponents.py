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
            sizing_option: int = None,
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
        sizing = idf.newidfobject('Sizing:Plant'.upper())

        if isinstance(plantloop, EpBunch):
            sizing['Plant_or_Condenser_Loop_Name'] = plantloop.Name
        elif isinstance(plantloop, str):
            sizing['Plant_or_Condenser_Loop_Name'] = plantloop
        else:
            raise TypeError('Invalid input type of plantloop.')

        sizing['Loop_Type'] = loop_types[loop_type]

        if loop_exit_temp is not None:
            sizing['Design_Loop_Exit_Temperature'] = loop_exit_temp
        if loop_temp_diff is not None:
            sizing['Loop_Design_Temperature_Difference'] = loop_temp_diff
        if zone_timesteps_in_averaging_window is not None:
            sizing['Zone_Timesteps_in_Averaging_Window'] = zone_timesteps_in_averaging_window

        sizing['Sizing_Option'] = sizing_options[sizing_option]
        sizing['Coincident_Sizing_Factor_Mode'] = sizing_factor_modes[coincident_sizing_factor_mode]

        return sizing

    @staticmethod
    def pipe(idf: IDF, name=None, pipe_type: int = 1):
        """
        -Pipe_type:
            1:Adiabatic 2:Indoor 3:Outdoor 4:Adiabatic:Steam 5: Underground
        """
        pipe_types = {1: "Pipe:Adiabatic", 2: "Pipe:Indoor", 3: "Pipe:Outdoor",
                      4: "Pipe:Adiabatic:Steam", 5: "Pipe:Underground"}

        name = f'Pipe_{pipe_types[pipe_type].split(":")[-1]}' if name is None else name
        pipe = idf.newidfobject(pipe_types[pipe_type].upper(), Name=name)
        pipe.Inlet_Node_Name = f'{name}_inlet'
        pipe.Outlet_Node_Name = f'{name}_outlet'

        component = {
            'object': pipe,
            'type': pipe_types[pipe_type]
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
            condenser_loop=None):

        """
        -Condenser_type: 1:AirCooled 2:WaterCooled 3:EvapCooled \n
        -Chiller_flow_mode: 1:NotModulated 2:LeavingSetpointModulated 3:ConstantFlow
        """

        condenser_types = {1: "AirCooled", 2: "WaterCooled", 3: "EvapCooled"}
        flow_modes = {1: "NotModulated", 2: "LeavingSetpointModulated", 3: "ConstantFlow"}

        name = f'Chiller {condenser_types[condenser_type]}' if name is None else name

        chiller = idf.newidfobject('Chiller:Electric:EIR'.upper(), Name=name)

        chiller['Condenser_Type'] = condenser_types[condenser_type]
        chiller['Reference_Capacity'] = capacity
        chiller['Reference_COP'] = cop
        chiller['Reference_Leaving_Chilled_Water_Temperature'] = leaving_chilled_water_temp
        chiller['Reference_Entering_Condenser_Water_Temperature'] = entering_condenser_water_temp
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
            chiller['Heat_Recovery_Inlet_High_Temperature_Limit_Schedule_Name'] = heat_recovery_inlet_high_temp_limit_schedule
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
                chiller['Electric_Input_to_Cooling_Output_Ratio_Function_of_Temperature_Curve_Name'] = cop_temperature_curve
            elif isinstance(cop_temperature_curve, EpBunch):
                chiller['Electric_Input_to_Cooling_Output_Ratio_Function_of_Temperature_Curve_Name'] = cop_temperature_curve.Name
            else:
                raise TypeError('cop_temperature_curve must be EpBunch or str')
        else:
            chiller['Electric_Input_to_Cooling_Output_Ratio_Function_of_Temperature_Curve_Name'] = curve_set[1].Name

        if cop_plr_curve is not None:
            if isinstance(cop_plr_curve, str):
                chiller['Electric_Input_to_Cooling_Output_Ratio_Function_of_Part_Load_Ratio_Curve_Name'] = cop_plr_curve
            elif isinstance(cop_plr_curve, EpBunch):
                chiller['Electric_Input_to_Cooling_Output_Ratio_Function_of_Part_Load_Ratio_Curve_Name'] = cop_plr_curve.Name
            else:
                raise TypeError('cop_plr_curve must be EpBunch or str')
        else:
            chiller['Electric_Input_to_Cooling_Output_Ratio_Function_of_Part_Load_Ratio_Curve_Name'] = curve_set[2].Name

        chiller['Chilled_Water_Inlet_Node_Name'] = f'{name} Chilled_Water_Inlet'
        chiller['Chilled_Water_Outlet_Node_Name'] = f'{name} Chilled_Water_Outlet'
        chiller['Condenser_Inlet_Node_Name'] = f'{name} Condenser_Water_Inlet'
        chiller['Condenser_Outlet_Node_Name'] = f'{name} Condenser_Water_Outlet'
        if design_heat_recovery_flow_rate is not None:
            chiller['Heat_Recovery_Inlet_Node_Name'] = f'{name} Heat_Recovery_Inlet'
            chiller['Heat_Recovery_Outlet_Node_Name'] = f'{name} Heat_Recovery_Outlet'

        chiller['EndUse_Subcategory'] = 'General'

        comp = {
            'object': chiller,
            'type': 'Chiller:Electric:EIR',
            'chilled_water_inlet': 'Chilled_Water_Inlet_Node_Name',
            'chilled_water_outlet': 'Chilled_Water_Outlet_Node_Name',
            'condenser_water_inlet': 'Condenser_Inlet_Node_Name',
            'condenser_water_outlet': 'Condenser_Outlet_Node_Name',
        }

        return comp

    @staticmethod
    def district_cooling(
            idf: IDF,
            name: str = None,
            nominal_capacity='Autosize',
            capacity_fraction_schedule: EpBunch | str = None):

        name = 'District Cooling' if name is None else name
        district = idf.newidfobject('DistrictCooling'.upper(), Name=name)

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
            'chilled_water_inlet': 'Chilled_Water_Inlet_Node_Name',
            'chilled_water_outlet': 'Chilled_Water_Outlet_Node_Name',
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
        district = idf.newidfobject('DistrictHeating'.upper(), Name=name)

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
            'hot_water_inlet': 'Hot_Water_Inlet_Node_Name',
            'hot_water_outlet': 'Hot_Water_Outlet_Node_Name',
        }

        return comp

    # ***************************************************************************************************
    # Distribution Equipments
    @staticmethod
    def pump_variable_speed(
            idf: IDF,
            name: str = None,
            design_head=None,
            design_max_flow_rate='Autosize',
            design_min_flow_rate=0,
            design_power='Autosize',
            motor_efficiency=0.9,
            fraction_of_motor_to_fluid=0,
            control_type: int = 1,
            vfd_control_type: int = 1,
            power_sizing_method: int = 1,
            power_per_flow_rate=348701.1,
            power_per_flow_rate_per_head=None,
            thermal_zone=None,
            skin_loss_radiative_fraction=0.5,
            design_min_flow_fraction=0,
            pump_curve_coeff=None):

        """
        -Control_type: 1:Intermittent 2:Continuous \n
        -VFD_control_type: 1:PressureSetPointControl 2:ManualControl \n
        -Power_sizing_method: 1:PowerPerFlowPerPressure 2:PowerPerFlow
        """

        control_types = {1: "Intermittent", 2: "Continuous"}
        vfd_control_types = {1: "PressureSetPointControl", 2: "ManualControl"}
        sizing_methods = {1: "PowerPerFlowPerPressure", 2: "PowerPerFlow"}

        name = 'Pump Variable Speed' if name is None else name
        pump = idf.newidfobject('Pump:VariableSpeed'.upper(), Name=name)

        pump['Design_Maximum_Flow_Rate'] = design_flow_rate
        pump['Design_Pump_Head'] = design_head

        pump['EndUse_Subcategory'] = 'General'

        return pump

    # @staticmethod
    # def pump_constant_speed(
    #         idf: IDF,
    #         name: str = None,
    #         rated_head=None,
    #         rated_flow_rate=None,
    #         rated_power=None,
    #         motor_efficiency=None,
    #         control_type: int = 1,
    #         power_sizing_method: int = 1,
    #         power_per_flow_rate=None,
    #         power_per_flow_rate_per_head=None,
    #         thermal_zone: openstudio.openstudiomodel.ThermalZone = None):
    #
    #     """
    #     -Control_type: 1:Intermittent 2:Continuous \n
    #     -Power_sizing_method: 1:PowerPerFlowPerPressure 2:PowerPerFlow
    #     """
    #
    #     control_types = {1: "Intermittent", 2: "Continuous"}
    #     sizing_methods = {1: "PowerPerFlowPerPressure", 2: "PowerPerFlow"}
    #
    #     pump = openstudio.openstudiomodel.PumpConstantSpeed(model)
    #
    #     if name is not None: pump.setName(name)
    #     if rated_head is not None: pump.setRatedPumpHead(rated_head)
    #
    #     if rated_flow_rate is not None:
    #         pump.setRatedFlowRate(rated_flow_rate)
    #     else:
    #         pump.autosizeRatedFlowRate()
    #
    #     if rated_power is not None:
    #         pump.setRatedPowerConsumption(rated_power)
    #     else:
    #         pump.autosizeRatedPowerConsumption()
    #
    #     if motor_efficiency is not None:
    #         pump.setMotorEfficiency(motor_efficiency)
    #     if control_type != 1:
    #         pump.setPumpControlType(control_types[control_type])
    #     if power_sizing_method != 1:
    #         pump.setDesignPowerSizingMethod(sizing_methods[power_sizing_method])
    #     if power_per_flow_rate is not None:
    #         pump.setDesignElectricPowerPerUnitFlowRate(power_per_flow_rate)
    #     if power_per_flow_rate_per_head is not None:
    #         pump.setDesignShaftPowerPerUnitFlowRatePerUnitHead(power_per_flow_rate_per_head)
    #
    #     if thermal_zone is not None:
    #         pump.setZone(thermal_zone)
    #
    #     return pump
    #
    # @staticmethod
    # def headered_pumps_variable_speed(
    #         idf: IDF,
    #         name: str = None,
    #         rated_flow_rate=None,
    #         number_of_pumps_in_bank: int = 2,
    #         rated_head=None,
    #         rated_power=None,
    #         motor_efficiency=None,
    #         fraction_motor_inefficiencies_to_fluid_stream=None,
    #         min_flow_rate_fraction=None,
    #         control_type: int = 1,
    #         pump_flow_schedule=None,
    #         power_sizing_method: int = 1,
    #         power_per_flow_rate=None,
    #         power_per_flow_rate_per_head=None,
    #         thermal_zone: openstudio.openstudiomodel.ThermalZone = None,
    #         skin_loss_radiative_fraction=None,
    #         pump_curve_coeff=None):
    #
    #     """
    #     -Control_type: 1:Intermittent 2:Continuous \n
    #     -Power_sizing_method: 1:PowerPerFlowPerPressure 2:PowerPerFlow
    #     """
    #
    #     control_types = {1: "Intermittent", 2: "Continuous"}
    #     sizing_methods = {1: "PowerPerFlowPerPressure", 2: "PowerPerFlow"}
    #
    #     pump = openstudio.openstudiomodel.HeaderedPumpsVariableSpeed(model)
    #
    #     if name is not None:
    #         pump.setName(name)
    #     if rated_head is not None:
    #         pump.setRatedPumpHead(rated_head)
    #
    #     if rated_flow_rate is not None:
    #         pump.setTotalRatedFlowRate(rated_flow_rate)
    #     else:
    #         pump.autosizeTotalRatedFlowRate()
    #
    #     pump.setNumberofPumpsinBank(number_of_pumps_in_bank)
    #
    #     if min_flow_rate_fraction is not None:
    #         pump.setMinimumFlowRateFraction(min_flow_rate_fraction)
    #
    #     if rated_power is not None:
    #         pump.setRatedPowerConsumption(rated_power)
    #     else:
    #         pump.autosizeRatedPowerConsumption()
    #
    #     if motor_efficiency is not None:
    #         pump.setMotorEfficiency(motor_efficiency)
    #     if fraction_motor_inefficiencies_to_fluid_stream is not None:
    #         pump.setFractionofMotorInefficienciestoFluidStream(fraction_motor_inefficiencies_to_fluid_stream)
    #     if control_type != 1:
    #         pump.setPumpControlType(control_types[control_type])
    #     if pump_flow_schedule is not None:
    #         pump.setPumpFlowRateSchedule(pump_flow_schedule)
    #     if power_sizing_method != 1:
    #         pump.setDesignPowerSizingMethod(sizing_methods[power_sizing_method])
    #     if power_per_flow_rate is not None:
    #         pump.setDesignElectricPowerPerUnitFlowRate(power_per_flow_rate)
    #     if power_per_flow_rate_per_head is not None:
    #         pump.setDesignShaftPowerPerUnitFlowRatePerUnitHead(power_per_flow_rate_per_head)
    #
    #     if thermal_zone is not None:
    #         pump.setThermalZone(thermal_zone)
    #     if skin_loss_radiative_fraction is not None:
    #         pump.setSkinLossRadiativeFraction(skin_loss_radiative_fraction)
    #
    #     if pump_curve_coeff is not None:
    #         if isinstance(pump_curve_coeff, list) and len(pump_curve_coeff) == 4:
    #             pump.setCoefficient1ofthePartLoadPerformanceCurve(pump_curve_coeff[0])
    #             pump.setCoefficient2ofthePartLoadPerformanceCurve(pump_curve_coeff[1])
    #             pump.setCoefficient3ofthePartLoadPerformanceCurve(pump_curve_coeff[2])
    #             pump.setCoefficient4ofthePartLoadPerformanceCurve(pump_curve_coeff[3])
    #
    #     return pump
    #
    # @staticmethod
    # def headered_pumps_constant_speed(
    #         idf: IDF,
    #         name: str = None,
    #         rated_flow_rate=None,
    #         number_of_pumps_in_bank: int = 2,
    #         rated_head=None,
    #         rated_power=None,
    #         motor_efficiency=None,
    #         fraction_motor_inefficiencies_to_fluid_stream=None,
    #         control_type: int = 1,
    #         pump_flow_schedule=None,
    #         power_sizing_method: int = 1,
    #         power_per_flow_rate=None,
    #         power_per_flow_rate_per_head=None,
    #         thermal_zone: openstudio.openstudiomodel.ThermalZone = None,
    #         skin_loss_radiative_fraction=None):
    #
    #     """
    #     -Control_type: 1:Intermittent 2:Continuous \n
    #     -Power_sizing_method: 1:PowerPerFlowPerPressure 2:PowerPerFlow
    #     """
    #
    #     control_types = {1: "Intermittent", 2: "Continuous"}
    #     sizing_methods = {1: "PowerPerFlowPerPressure", 2: "PowerPerFlow"}
    #
    #     pump = openstudio.openstudiomodel.HeaderedPumpsConstantSpeed(model)
    #
    #     if name is not None:
    #         pump.setName(name)
    #     if rated_head is not None:
    #         pump.setRatedPumpHead(rated_head)
    #
    #     if rated_flow_rate is not None:
    #         pump.setTotalRatedFlowRate(rated_flow_rate)
    #     else:
    #         pump.autosizeTotalRatedFlowRate()
    #
    #     pump.setNumberofPumpsinBank(number_of_pumps_in_bank)
    #
    #     if rated_power is not None:
    #         pump.setRatedPowerConsumption(rated_power)
    #     else:
    #         pump.autosizeRatedPowerConsumption()
    #
    #     if motor_efficiency is not None:
    #         pump.setMotorEfficiency(motor_efficiency)
    #     if fraction_motor_inefficiencies_to_fluid_stream is not None:
    #         pump.setFractionofMotorInefficienciestoFluidStream(fraction_motor_inefficiencies_to_fluid_stream)
    #     if control_type != 1:
    #         pump.setPumpControlType(control_types[control_type])
    #     if pump_flow_schedule is not None:
    #         pump.setPumpFlowRateSchedule(pump_flow_schedule)
    #     if power_sizing_method != 1:
    #         pump.setDesignPowerSizingMethod(sizing_methods[power_sizing_method])
    #     if power_per_flow_rate is not None:
    #         pump.setDesignElectricPowerPerUnitFlowRate(power_per_flow_rate)
    #     if power_per_flow_rate_per_head is not None:
    #         pump.setDesignShaftPowerPerUnitFlowRatePerUnitHead(power_per_flow_rate_per_head)
    #
    #     if thermal_zone is not None:
    #         pump.setThermalZone(thermal_zone)
    #     if skin_loss_radiative_fraction is not None:
    #         pump.setSkinLossRadiativeFraction(skin_loss_radiative_fraction)
    #
    #     return pump
