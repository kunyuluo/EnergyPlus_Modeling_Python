from eppy.modeleditor import IDF
from eppy.bunch_subclass import EpBunch
from configs import *
from HVACSystem.Controllers import Controller
from HVACSystem.PerformanceCurves import PerformanceCurve
from HVACSystem.PerformanceTables import PerformanceTable


class AirLoopComponent:
    @staticmethod
    def sizing(
            idf: IDF,
            airloop: EpBunch | str = None,
            doas: bool = False,
            type_of_load: int = 1,
            design_outdoor_air_flow_rate=autosize,
            central_heating_max_flow_ratio=autosize,
            system_outdoor_air_method: int = 1,
            max_outdoor_air_fraction: float = 1.0,
            preheat_temp=7,
            preheat_humidity_ratio=0.008,
            precool_temp=12.8,
            precool_humidity_ratio=0.008,
            central_cooling_supply_air_temp=12.8,
            central_heating_supply_air_temp=12.8,
            central_cooling_supply_air_humidity_ratio=0.0085,
            central_heating_supply_air_humidity_ratio=0.008,
            sizing_option: int = 2,
            all_outdoor_air_cooling: bool = False,
            all_outdoor_air_heating: bool = False,
            cooling_supply_air_flow_method: int = 1,
            heating_supply_air_flow_method: int = 1,
            cooling_supply_air_flow_rate=0,
            heating_supply_air_flow_rate=0,
            cooling_supply_air_flow_rate_per_floor_area=0.0099676501,
            heating_supply_air_flow_rate_per_floor_area=0.0099676501,
            cooling_fraction_of_autosized_air_flow_rate=1,
            heating_fraction_of_autosized_air_flow_rate=1,
            heating_fraction_of_autosized_cooling_air_flow_rate=1,
            cooling_supply_air_flow_rate_per_unit_capacity=3.9475456e-05,
            heating_supply_air_flow_rate_per_unit_capacity=3.1588213e-05,
            cooling_design_capacity_method: int = 2,
            heating_design_capacity_method: int = 2,
            cooling_design_capacity=autosize,
            heating_design_capacity=autosize,
            cooling_design_capacity_per_floor_area=234.7,
            heating_design_capacity_per_floor_area=157,
            fraction_of_autosized_cooling_design_capacity: float = 1.0,
            fraction_of_autosized_heating_design_capacity: float = 1.0,
            central_cooling_capacity_control_method: int = 1,
            occupant_diversity=None):
        """
        -Options for "type_of_load_to_size_on":
            1: Total (Sensible + Latent)
            2: Sensible
            3: VentilationRequirement (choose this option for DOAS)

        -Options for "system_outdoor_air_method":
            1: ZoneSum
            2: Standard62.1VentilationRateProcedure (VRP)
            3: Standard62.1SimplifiedProcedure (SP)
            (Default is ZoneSum)

        -Options for "sizing_option":
            1: Coincident
            2: NonCoincident
            (Default is NonCoincident)

        -Options for "cooling_design_air_flow_rate_method":
            1: DesignDay
            2: Flow/System
            3: FlowPerFloorArea
            4: FractionOfAutosizedCoolingAirflow
            5: FlowPerCoolingCapacity
            (Default is DesignDay)

        -Options for "heating_design_air_flow_rate_method":
            1: DesignDay
            2: Flow/System
            3: FlowPerFloorArea
            4: FractionOfAutosizedHeatingAirflow
            5: FractionOfAutosizedCoolingAirflow
            6: FlowPerHeatingCapacity
            (Default is DesignDay)

        -Options for "cooling_design_capacity_method":
            1: None
            2: CoolingDesignCapacity
            3: CapacityPerFloorArea
            4: FractionOfAutosizedCoolingCapacity
            (Default is CoolingDesignCapacity)

        -Options for "heating_design_capacity_method":
            1: None
            2: HeatingDesignCapacity
            3: CapacityPerFloorArea
            4: FractionOfAutosizedHeatingCapacity
            (Default is HeatingDesignCapacity)

        -Options for "heating_design_capacity_method": same as above

        -Options for "central_cooling_capacity_control_method":
            1: OnOff
            2: VAV
            3: Bypass
            4: VT
            (Default is OnOff)
        """

        load_types = {1: "Total", 2: "Sensible", 3: "VentilationRequirement"}
        outdoor_air_methods = {1: "ZoneSum", 2: "Standard62.1VentilationRateProcedure",
                               3: "Standard62.1SimplifiedProcedure"}
        sizing_options = {1: "Coincident", 2: "NonCoincident"}
        cooling_air_flow_methods = {1: "DesignDay", 2: "Flow/System", 3: "FlowPerFloorArea",
                                    4: "FractionOfAutosizedCoolingAirflow", 5: "FlowPerCoolingCapacity"}
        heating_air_flow_methods = {1: "DesignDay", 2: "Flow/System", 3: "FlowPerFloorArea",
                                    4: "FractionOfAutosizedHeatingAirflow", 5: "FractionOfAutosizedCoolingAirflow",
                                    6: "FlowPerHeatingCapacity"}
        cooling_capacity_methods = {1: "None", 2: "CoolingDesignCapacity", 3: "CapacityPerFloorArea",
                                    4: "FractionOfAutosizedCoolingCapacity"}
        heating_capacity_methods = {1: "None", 2: "HeatingDesignCapacity", 3: "CapacityPerFloorArea",
                                    4: "FractionOfAutosizedHeatingCapacity"}
        cooling_control_methods = {1: "OnOff", 2: "VAV", 3: "Bypass", 4: "VT"}

        sizing = idf.newidfobject('Sizing:System')

        if airloop is not None:
            if isinstance(airloop, EpBunch):
                sizing['AirLoop_Name'] = airloop.Name
            elif isinstance(airloop, str):
                sizing['AirLoop_Name'] = airloop
            else:
                raise TypeError('Invalid input type of airloop.')

        if doas:
            sizing['Type_of_Load_to_Size_On'] = load_types[3]
        else:
            sizing['Type_of_Load_to_Size_On'] = load_types[type_of_load]

        sizing['Design_Outdoor_Air_Flow_Rate'] = design_outdoor_air_flow_rate
        sizing['Central_Heating_Maximum_System_Air_Flow_Ratio'] = central_heating_max_flow_ratio
        sizing['Preheat_Design_Temperature'] = preheat_temp
        sizing['Preheat_Design_Humidity_Ratio'] = preheat_humidity_ratio
        sizing['Precool_Design_Temperature'] = precool_temp
        sizing['Precool_Design_Humidity_Ratio'] = precool_humidity_ratio
        sizing['Central_Cooling_Design_Supply_Air_Temperature'] = central_cooling_supply_air_temp
        sizing['Central_Heating_Design_Supply_Air_Temperature'] = central_heating_supply_air_temp
        sizing['Central_Cooling_Design_Supply_Air_Humidity_Ratio'] = central_cooling_supply_air_humidity_ratio
        sizing['Central_Heating_Design_Supply_Air_Humidity_Ratio'] = central_heating_supply_air_humidity_ratio
        sizing['Type_of_Zone_Sum_to_Use'] = sizing_options[sizing_option]

        if doas:
            sizing['100_Outdoor_Air_in_Cooling'] = 'Yes'
            sizing['100_Outdoor_Air_in_Heating'] = 'Yes'
        else:
            if all_outdoor_air_cooling:
                sizing['100_Outdoor_Air_in_Cooling'] = 'Yes'
            else:
                sizing['100_Outdoor_Air_in_Cooling'] = 'No'
            if all_outdoor_air_heating:
                sizing['100_Outdoor_Air_in_Heating'] = 'Yes'
            else:
                sizing['100_Outdoor_Air_in_Heating'] = 'No'

        sizing['Cooling_Supply_Air_Flow_Rate_Method'] = cooling_air_flow_methods[cooling_supply_air_flow_method]
        sizing['Heating_Supply_Air_Flow_Rate_Method'] = heating_air_flow_methods[heating_supply_air_flow_method]
        sizing['Cooling_Supply_Air_Flow_Rate'] = cooling_supply_air_flow_rate
        sizing['Heating_Supply_Air_Flow_Rate'] = heating_supply_air_flow_rate

        sizing['Cooling_Supply_Air_Flow_Rate_Per_Floor_Area'] = cooling_supply_air_flow_rate_per_floor_area
        sizing['Heating_Supply_Air_Flow_Rate_Per_Floor_Area'] = heating_supply_air_flow_rate_per_floor_area
        sizing['Cooling_Fraction_of_Autosized_Cooling_Supply_Air_Flow_Rate'] = cooling_fraction_of_autosized_air_flow_rate
        sizing['Heating_Fraction_of_Autosized_Heating_Supply_Air_Flow_Rate'] = heating_fraction_of_autosized_air_flow_rate
        sizing['Heating_Fraction_of_Autosized_Cooling_Supply_Air_Flow_Rate'] = heating_fraction_of_autosized_cooling_air_flow_rate
        sizing['Cooling_Supply_Air_Flow_Rate_Per_Unit_Cooling_Capacity'] = cooling_supply_air_flow_rate_per_unit_capacity
        sizing['Heating_Supply_Air_Flow_Rate_Per_Unit_Heating_Capacity'] = heating_supply_air_flow_rate_per_unit_capacity

        sizing['System_Outdoor_Air_Method'] = outdoor_air_methods[system_outdoor_air_method]
        sizing['Zone_Maximum_Outdoor_Air_Fraction'] = max_outdoor_air_fraction

        sizing['Cooling_Design_Capacity_Method'] = cooling_capacity_methods[cooling_design_capacity_method]
        sizing['Heating_Design_Capacity_Method'] = heating_capacity_methods[heating_design_capacity_method]
        sizing['Cooling_Design_Capacity'] = cooling_design_capacity
        sizing['Heating_Design_Capacity'] = heating_design_capacity
        sizing['Cooling_Design_Capacity_Per_Floor_Area'] = cooling_design_capacity_per_floor_area
        sizing['Heating_Design_Capacity_Per_Floor_Area'] = heating_design_capacity_per_floor_area
        sizing['Fraction_of_Autosized_Cooling_Design_Capacity'] = fraction_of_autosized_cooling_design_capacity
        sizing['Fraction_of_Autosized_Heating_Design_Capacity'] = fraction_of_autosized_heating_design_capacity

        sizing['Central_Cooling_Capacity_Control_Method'] = cooling_control_methods[central_cooling_capacity_control_method]

        if occupant_diversity is not None:
            sizing['Occupant_Diversity'] = occupant_diversity

        return sizing

    # Coils
    # ********************************************************************************
    @staticmethod
    def cooling_coil_water(
            idf: IDF,
            name: str = None,
            schedule: EpBunch | str = None,
            design_water_temp_diff: float = None,
            design_water_flow_rate=autosize,
            design_air_flow_rate=autosize,
            design_inlet_water_temp=autosize,
            design_inlet_air_temp=autosize,
            design_outlet_air_temp=autosize,
            design_inlet_air_humidity_ratio=autosize,
            design_outlet_air_humidity_ratio=autosize,
            type_of_analysis: int = 1,
            heat_exchanger_config: int = 1,
            control_variable: int = 1,
            need_controller: bool = True,):
        """
        -Type_of_analysis: 1.SimpleAnalysis 2.DetailedAnalysis \n
        -Heat_exchanger_config: 1.CrossFlow 2.CounterFlow \n
        -Control_variable: 1.Temperature 2.HumidityRatio 3.TemperatureAndHumidityRatio \n
        """

        analysis_types = {1: "SimpleAnalysis", 2: "DetailedAnalysis"}
        hx_configs = {1: "CrossFlow", 2: "CounterFlow"}

        name = 'Coil Cooling Water' if name is None else name
        coil = idf.newidfobject('Coil:Cooling:Water', Name=name)

        if schedule is None:
            coil['Availability_Schedule_Name'] = schedule_always_on_hvac
        else:
            if isinstance(schedule, EpBunch):
                coil['Availability_Schedule_Name'] = schedule.Name
            elif isinstance(schedule, str):
                coil['Availability_Schedule_Name'] = schedule
            else:
                raise TypeError('Invalid type of schedule.')

        if design_water_temp_diff is not None:
            coil['Design_Water_Temperature_Difference'] = design_water_temp_diff
        coil['Design_Water_Flow_Rate'] = design_water_flow_rate
        coil['Design_Air_Flow_Rate'] = design_air_flow_rate
        coil['Design_Inlet_Water_Temperature'] = design_inlet_water_temp
        coil['Design_Inlet_Air_Temperature'] = design_inlet_air_temp
        coil['Design_Outlet_Air_Temperature'] = design_outlet_air_temp
        coil['Design_Inlet_Air_Humidity_Ratio'] = design_inlet_air_humidity_ratio
        coil['Design_Outlet_Air_Humidity_Ratio'] = design_outlet_air_humidity_ratio

        coil['Type_of_Analysis'] = analysis_types[type_of_analysis]
        coil['Heat_Exchanger_Configuration'] = hx_configs[heat_exchanger_config]

        coil['Water_Inlet_Node_Name'] = f'{name}_water_inlet'
        coil['Water_Outlet_Node_Name'] = f'{name}_water_outlet'
        coil['Air_Inlet_Node_Name'] = f'{name}_air_inlet'
        coil['Air_Outlet_Node_Name'] = f'{name}_air_outlet'

        # Controller:
        if need_controller:
            controller_name = f'{name} Controller'
            controller = Controller.controller_watercoil(idf, controller_name, control_variable, 2)
            controller['Sensor_Node_Name'] = coil.Air_Outlet_Node_Name
            controller['Actuator_Node_Name'] = coil.Water_Inlet_Node_Name
        else:
            controller = None

        component = {
            'object': coil,
            'controller': controller,
            'type': 'Coil:Cooling:Water',
            'water_inlet_field': 'Water_Inlet_Node_Name',
            'water_outlet_field': 'Water_Outlet_Node_Name',
            'air_inlet_field': 'Air_Inlet_Node_Name',
            'air_outlet_field': 'Air_Outlet_Node_Name',
        }

        return component

    # @staticmethod
    # def cooling_coil_dx_single_speed(
    #         idf: IDF,
    #         name: str = None,
    #         schedule: EpBunch | str = None,
    #         capacity=autosize,
    #         sensible_heat_ratio=None,
    #         cop=None,
    #         rated_air_flow_rate=None,
    #         evaporator_fan_power_per_flow_2017=None,
    #         evaporator_fan_power_per_flow_2023=None,
    #         min_outdoor_air_temp_compressor_operation=None,
    #         crankcase_heater_capacity=None,
    #         max_outdoor_air_temp_crankcase_operation=None,
    #         condenser_type: str = None,
    #         evaporative_condenser_effectiveness=None,
    #         evaporative_condenser_air_flow_rate=None,
    #         evaporative_condenser_pump_power=None,
    #         capacity_temperature_curve = None,
    #         capacity_flow_curve = None,
    #         cop_temperature_curve = None,
    #         cop_flow_curve = None,
    #         plr_curve = None):
    #
    #     name = 'Coil Cooling DX Single Speed' if name is None else name
    #     coil = idf.newidfobject('Coil:Cooling:DX:SingleSpeed', Name=name)
    #
    #     if schedule is None:
    #         coil['Availability_Schedule_Name'] = schedule_always_on_hvac
    #     else:
    #         if isinstance(schedule, EpBunch):
    #             coil['Availability_Schedule_Name'] = schedule.Name
    #         elif isinstance(schedule, str):
    #             coil['Availability_Schedule_Name'] = schedule
    #         else:
    #             raise TypeError('Invalid type of schedule.')
    #
    #     component = {
    #         'object': coil,
    #         'type': 'Coil:Cooling:Water',
    #         'air_inlet_field': 'Air_Inlet_Node_Name',
    #         'air_outlet_field': 'Air_Outlet_Node_Name',
    #     }
    #
    #     return component

    @staticmethod
    def cooling_coil_vrf(
            idf: IDF,
            name: str = None,
            schedule: EpBunch | str = None,
            cooling_capacity=autosize,
            sensible_heat_ratio=autosize,
            air_flow_rate=autosize,
            capacity_temperature_curve=None,
            capacity_flow_curve=None):
        name = 'VRF Cooling Coil' if name is None else name
        coil = idf.newidfobject('Coil:Cooling:DX:VariableRefrigerantFlow', Nmae=name)

        if schedule is None:
            coil['Availability_Schedule_Name'] = schedule_always_on_hvac
        else:
            if isinstance(schedule, EpBunch):
                coil['Availability_Schedule_Name'] = schedule.Name
            elif isinstance(schedule, str):
                coil['Availability_Schedule_Name'] = schedule
            else:
                raise TypeError('Invalid type of schedule.')

        coil['Gross_Rated_Total_Cooling_Capacity'] = cooling_capacity
        coil['Gross_Rated_Sensible_Heat_Ratio'] = sensible_heat_ratio
        coil['Rated_Air_Flow_Rate'] = air_flow_rate
        if capacity_temperature_curve is None:
            capacity_temperature_curve = PerformanceCurve.biquadratic(
                idf,
                name=f'{name} VRFTUCoolCapFT',
                coeff_constant=0.0585884077803259,
                coeff_x=0.0587396532718384,
                coeff_x2=-0.000210274979759697,
                coeff_y=0.0109370473889647,
                coeff_y2=-0.0001219549,
                coeff_xy=-0.0005246615,
                min_x=15,
                max_x=23.89,
                min_y=20,
                max_y=43.33,
                min_out=0.8083,
                max_out=1.2583,
                input_unit_type_x='Temperature',
                input_unit_type_y='Temperature',
                output_unit_type='Dimensionless')
            coil['Cooling_Capacity_Ratio_Modifier_Function_of_Temperature_Curve_Name'] = capacity_temperature_curve.Name
        else:
            coil['Cooling_Capacity_Ratio_Modifier_Function_of_Temperature_Curve_Name'] = capacity_temperature_curve.Name
        if capacity_flow_curve is None:
            capacity_flow_curve = PerformanceCurve.quadratic(
                idf, name=f'{name} VRFACCoolCapFFF',
                coeff_constant=0.8,
                coeff_x=0.2,
                coeff_x2=0.0,
                min_x=0.5,
                max_x=1.5)
            coil['Cooling_Capacity_Modifier_Curve_Function_of_Flow_Fraction_Name'] = capacity_flow_curve.Name
        else:
            coil['Cooling_Capacity_Modifier_Curve_Function_of_Flow_Fraction_Name'] = capacity_flow_curve.Name

        coil['Coil_Air_Inlet_Node'] = f'{name} Air Inlet'
        coil['Coil_Air_Outlet_Node'] = f'{name} Air Outlet'

        comp = {
            'object': coil,
            'type': 'Coil:Cooling:DX:VariableRefrigerantFlow',
            'air_inlet_field': 'Coil_Air_Inlet_Node',
            'air_outlet_field': 'Coil_Air_Outlet_Node'
        }
        return comp

    @staticmethod
    def heating_coil_water(
            idf: IDF,
            name: str = None,
            schedule: EpBunch | str = None,
            ufactor_times_area=autosize,
            max_water_flow_rate=autosize,
            performance_input_method: int = 1,
            rated_capacity=autosize,
            design_water_temp_diff: float = 20,
            inlet_water_temp=60,
            inlet_air_temp=16.6,
            outlet_water_temp=40,
            outlet_air_temp=32.2,
            ratio_air_water_convection=0.5,
            need_controller: bool = True,
            control_variable: int = 1):
        """
        -Performance_input_method: 1.UFactorTimesAreaAndDesignWaterFlowRate 2.NominalCapacity
        """

        methods = {1: "UFactorTimesAreaAndDesignWaterFlowRate", 2: "NominalCapacity"}

        name = 'Coil Heating Water' if name is None else name
        coil = idf.newidfobject('Coil:Heating:Water', Name=name)

        if schedule is None:
            coil['Availability_Schedule_Name'] = schedule_always_on_hvac
        else:
            if isinstance(schedule, EpBunch):
                coil['Availability_Schedule_Name'] = schedule.Name
            elif isinstance(schedule, str):
                coil['Availability_Schedule_Name'] = schedule
            else:
                raise TypeError('Invalid type of schedule.')

        coil['UFactor_Times_Area_Value'] = ufactor_times_area
        coil['Maximum_Water_Flow_Rate'] = max_water_flow_rate

        coil['Performance_Input_Method'] = methods[performance_input_method]
        coil['Rated_Capacity'] = rated_capacity
        coil['Design_Water_Temperature_Difference'] = design_water_temp_diff
        coil['Rated_Inlet_Water_Temperature'] = inlet_water_temp
        coil['Rated_Inlet_Air_Temperature'] = inlet_air_temp
        coil['Rated_Outlet_Water_Temperature'] = outlet_water_temp
        coil['Rated_Outlet_Air_Temperature'] = outlet_air_temp
        coil['Rated_Ratio_for_Air_and_Water_Convection'] = ratio_air_water_convection

        coil['Water_Inlet_Node_Name'] = f'{name}_water_inlet'
        coil['Water_Outlet_Node_Name'] = f'{name}_water_outlet'
        coil['Air_Inlet_Node_Name'] = f'{name}_air_inlet'
        coil['Air_Outlet_Node_Name'] = f'{name}_air_outlet'

        # Controller:
        if need_controller:
            controller_name = f'{name} Controller'
            controller = Controller.controller_watercoil(idf, controller_name, control_variable, 1)
            controller['Sensor_Node_Name'] = coil.Air_Outlet_Node_Name
            controller['Actuator_Node_Name'] = coil.Water_Inlet_Node_Name
        else:
            controller = None

        component = {
            'object': coil,
            'controller': controller,
            'type': 'Coil:Heating:Water',
            'water_inlet_field': 'Water_Inlet_Node_Name',
            'water_outlet_field': 'Water_Outlet_Node_Name',
            'air_inlet_field': 'Air_Inlet_Node_Name',
            'air_outlet_field': 'Air_Outlet_Node_Name',
        }

        return component

    @staticmethod
    def heating_coil_electric(
            idf: IDF,
            name: str = None,
            schedule: EpBunch | str = None,
            efficiency=1,
            capacity=autosize):
        name = 'Heating Coil Electric' if name is None else name
        coil = idf.newidfobject('Coil:Heating:Electric', Name=name)

        if schedule is None:
            coil['Availability_Schedule_Name'] = schedule_always_on_hvac
        else:
            if isinstance(schedule, EpBunch):
                coil['Availability_Schedule_Name'] = schedule.Name
            elif isinstance(schedule, str):
                coil['Availability_Schedule_Name'] = schedule
            else:
                raise TypeError('Invalid type of schedule.')

        coil['Efficiency'] = efficiency
        coil['Nominal_Capacity'] = capacity

        component = {
            'object': coil,
            'type': 'Coil:Heating:Electric',
            'air_inlet_field': 'Air_Inlet_Node_Name',
            'air_outlet_field': 'Air_Outlet_Node_Name',
        }

        return component

    @staticmethod
    def heating_coil_vrf(
            idf: IDF,
            name: str = None,
            schedule: EpBunch | str = None,
            heating_capacity=autosize,
            air_flow_rate=autosize,
            capacity_temperature_curve=None,
            capacity_flow_curve=None):
        name = 'VRF Heating Coil' if name is None else name
        coil = idf.newidfobject('Coil:Heating:DX:VariableRefrigerantFlow', Nmae=name)

        if schedule is None:
            coil['Availability_Schedule_Name'] = schedule_always_on_hvac
        else:
            if isinstance(schedule, EpBunch):
                coil['Availability_Schedule_Name'] = schedule.Name
            elif isinstance(schedule, str):
                coil['Availability_Schedule_Name'] = schedule
            else:
                raise TypeError('Invalid type of schedule.')

        coil['Gross_Rated_Heating_Capacity'] = heating_capacity
        coil['Rated_Air_Flow_Rate'] = air_flow_rate
        if capacity_temperature_curve is None:
            capacity_temperature_curve = PerformanceCurve.biquadratic(
                idf,
                name=f'{name} VRFTUHeatCAPFT',
                coeff_constant=0.375443994956127,
                coeff_x=0.0668190645147821,
                coeff_x2=-0.00194171026482001,
                coeff_y=0.0442618420640187,
                coeff_y2=-0.0004009578,
                coeff_xy=-0.0014819801,
                min_x=21.11,
                max_x=27.22,
                min_y=-15,
                max_y=18.33,
                min_out=0.6074,
                max_out=1,
                input_unit_type_x='Temperature',
                input_unit_type_y='Temperature',
                output_unit_type='Dimensionless')
            coil['Heating_Capacity_Ratio_Modifier_Function_of_Temperature_Curve_Name'] = capacity_temperature_curve.Name
        else:
            coil['Heating_Capacity_Ratio_Modifier_Function_of_Temperature_Curve_Name'] = capacity_temperature_curve.Name
        if capacity_flow_curve is None:
            capacity_flow_curve = PerformanceCurve.quadratic(
                idf, name=f'{name} VRFACHeatCapFFF',
                coeff_constant=0.8,
                coeff_x=0.2,
                coeff_x2=0.0,
                min_x=0.5,
                max_x=1.5)
            coil['Heating_Capacity_Modifier_Function_of_Flow_Fraction_Curve_Name'] = capacity_flow_curve.Name
        else:
            coil['Heating_Capacity_Modifier_Function_of_Flow_Fraction_Curve_Name'] = capacity_flow_curve.Name

        coil['Coil_Air_Inlet_Node'] = f'{name} Air Inlet'
        coil['Coil_Air_Outlet_Node'] = f'{name} Air Outlet'

        comp = {
            'object': coil,
            'type': 'Coil:Heating:DX:VariableRefrigerantFlow',
            'air_inlet_field': 'Coil_Air_Inlet_Node',
            'air_outlet_field': 'Coil_Air_Outlet_Node'
        }
        return comp

    # Fan
    # ********************************************************************************
    @staticmethod
    def fan_variable_speed(
            idf: IDF,
            name: str = None,
            schedule: EpBunch | str = None,
            fan_total_efficiency=0.6,
            pressure_rise=fan_pressure_rise_default,
            max_flow_rate=autosize,
            power_min_flow_rate_input_method: str = "FixedFlowRate",
            power_min_flow_rate_fraction=0,
            power_min_flow_rate=0,
            motor_efficiency=0.93,
            motor_in_airstream_fraction=1,
            fan_curve_coeff=PerformanceCurve.fan_curve_set(0)):
        """
        -Options for "power_min_flow_rate_input_method":
        1: Fraction, 2: FixedFlowRate
        """
        name = 'Fan Variable Speed' if name is None else name
        fan = idf.newidfobject('Fan:VariableVolume', Name=name)

        if schedule is None:
            fan['Availability_Schedule_Name'] = schedule_always_on_hvac
        else:
            if isinstance(schedule, EpBunch):
                fan['Availability_Schedule_Name'] = schedule.Name
            elif isinstance(schedule, str):
                fan['Availability_Schedule_Name'] = schedule
            else:
                raise TypeError('Invalid type of schedule.')

        fan['Fan_Total_Efficiency'] = fan_total_efficiency
        fan['Pressure_Rise'] = pressure_rise
        fan['Maximum_Flow_Rate'] = max_flow_rate
        fan['Fan_Power_Minimum_Flow_Rate_Input_Method'] = power_min_flow_rate_input_method
        fan['Fan_Power_Minimum_Flow_Fraction'] = power_min_flow_rate_fraction
        fan['Fan_Power_Minimum_Air_Flow_Rate'] = power_min_flow_rate
        fan['Motor_Efficiency'] = motor_efficiency
        fan['Motor_In_Airstream_Fraction'] = motor_in_airstream_fraction
        fan['EndUse_Subcategory'] = 'General'

        if fan_curve_coeff is not None:
            if isinstance(fan_curve_coeff, list):
                fan['Fan_Power_Coefficient_1'] = fan_curve_coeff[0]
                fan['Fan_Power_Coefficient_2'] = fan_curve_coeff[1]
                fan['Fan_Power_Coefficient_3'] = fan_curve_coeff[2]
                fan['Fan_Power_Coefficient_4'] = fan_curve_coeff[3]
                fan['Fan_Power_Coefficient_5'] = fan_curve_coeff[4]

        fan['Air_Inlet_Node_Name'] = f'{name} air inlet'
        fan['Air_Outlet_Node_Name'] = f'{name} air outlet'

        component = {
            'object': fan,
            'type': 'Fan:VariableVolume',
            'air_inlet_field': 'Air_Inlet_Node_Name',
            'air_outlet_field': 'Air_Outlet_Node_Name',
        }

        return component

    @staticmethod
    def fan_constant_speed(
            idf: IDF,
            name: str = None,
            schedule: EpBunch | str = None,
            fan_total_efficiency=0.6,
            pressure_rise=fan_pressure_rise_default,
            max_flow_rate=autosize,
            motor_efficiency=0.93,
            motor_in_airstream_fraction=1):
        name = 'Fan Constant Speed' if name is None else name
        fan = idf.newidfobject('Fan:ConstantVolume', Name=name)

        if schedule is None:
            fan['Availability_Schedule_Name'] = schedule_always_on_hvac
        else:
            if isinstance(schedule, EpBunch):
                fan['Availability_Schedule_Name'] = schedule.Name
            elif isinstance(schedule, str):
                fan['Availability_Schedule_Name'] = schedule
            else:
                raise TypeError('Invalid type of schedule.')

        fan['Fan_Total_Efficiency'] = fan_total_efficiency
        fan['Pressure_Rise'] = pressure_rise
        fan['Maximum_Flow_Rate'] = max_flow_rate
        fan['Motor_Efficiency'] = motor_efficiency
        fan['Motor_In_Airstream_Fraction'] = motor_in_airstream_fraction
        fan['EndUse_Subcategory'] = 'General'

        fan['Air_Inlet_Node_Name'] = f'{name} air inlet'
        fan['Air_Outlet_Node_Name'] = f'{name} air outlet'

        component = {
            'object': fan,
            'type': 'Fan:ConstantVolume',
            'air_inlet_field': 'Air_Inlet_Node_Name',
            'air_outlet_field': 'Air_Outlet_Node_Name',
        }

        return component

    @staticmethod
    def fan_on_off(
            idf: IDF,
            name: str = None,
            schedule: EpBunch | str = None,
            pressure_rise=fan_pressure_rise_default,
            max_flow_rate=autosize,
            fan_total_efficiency=0.6,
            motor_efficiency=0.93,
            motor_in_airstream_fraction=1,
            power_ratio_function_speed_ratio_curve: dict = None,
            efficiency_ratio_function_speed_ratio_curve: dict = None):
        name = 'Fan On Off' if name is None else name
        fan = idf.newidfobject('Fan:OnOff', Name=name)

        if schedule is None:
            fan['Availability_Schedule_Name'] = schedule_always_on_hvac
        else:
            if isinstance(schedule, EpBunch):
                fan['Availability_Schedule_Name'] = schedule.Name
            elif isinstance(schedule, str):
                fan['Availability_Schedule_Name'] = schedule
            else:
                raise TypeError('Invalid type of schedule.')

        fan['Fan_Total_Efficiency'] = fan_total_efficiency
        fan['Pressure_Rise'] = pressure_rise
        fan['Maximum_Flow_Rate'] = max_flow_rate
        fan['Motor_Efficiency'] = motor_efficiency
        fan['Motor_In_Airstream_Fraction'] = motor_in_airstream_fraction
        fan['EndUse_Subcategory'] = 'General'
        if power_ratio_function_speed_ratio_curve is None:
            power_ratio_function_speed_ratio_curve = PerformanceCurve.exponent(
                idf,
                coeff1_constant=1,
                coeff2_constant=0,
                coeff3_constant=0,
                min_x=0.0,
                max_x=1.0,
                min_out=0.0,
                max_out=1.0,
                name=f'{name} Power Ratio Curve')
        fan['Fan_Power_Ratio_Function_of_Speed_Ratio_Curve_Name'] = power_ratio_function_speed_ratio_curve
        if efficiency_ratio_function_speed_ratio_curve is None:
            efficiency_ratio_function_speed_ratio_curve = PerformanceCurve.cubic(
                idf,
                coeff1_constant=1,
                coeff2_x=0,
                coeff3_x2=0,
                coeff4_x3=0,
                min_x=0.0,
                max_x=1.0,
                name=f'{name} Efficiency Curve')
        fan['Fan_Efficiency_Ratio_Function_of_Speed_Ratio_Curve_Name'] = efficiency_ratio_function_speed_ratio_curve

        fan['Air_Inlet_Node_Name'] = f'{name} air inlet'
        fan['Air_Outlet_Node_Name'] = f'{name} air outlet'

        component = {
            'object': fan,
            'type': 'Fan:OnOff',
            'air_inlet_field': 'Air_Inlet_Node_Name',
            'air_outlet_field': 'Air_Outlet_Node_Name',
        }

        return component

    # Heat exchanger:
    # ***************************************************************************
    @staticmethod
    def heat_exchanger_air_to_air(
            idf: IDF,
            name: str = None,
            supply_air_flow_rate=autosize,
            sensible_only: bool = False,
            sensible_effectiveness_100_heating=0.75,
            latent_effectiveness_100_heating=0.68,
            sensible_effectiveness_75_heating=0.75,
            latent_effectiveness_75_heating=0.68,
            sensible_effectiveness_100_cooling=0.75,
            latent_effectiveness_100_cooling=0.68,
            sensible_effectiveness_75_cooling=0.75,
            latent_effectiveness_75_cooling=0.68,
            nominal_electric_power=0,
            supply_air_outlet_temp_control: bool = True,
            heat_exchanger_type: int = 0,
            frost_control_type: int = 0,
            threshold_temp=1.7,
            initial_defrost_time_fraction=None,
            rate_of_defrost_time_fraction_increase=None,
            economizer_lockout: bool = False,
            availability_schedule: EpBunch | str = None):
        """
        -Heat_exchanger_type: 1.Plate 2.Rotary \n
        -Frost_control_type: \n
        1.None 2.ExhaustAirRecirculation 3.ExhaustOnly 4.MinimumExhaustTemperature
        """

        types = {0: "Plate", 1: "Rotary"}
        frost_types = {0: "None", 1: "ExhaustAirRecirculation", 2: "ExhaustOnly", 3: "MinimumExhaustTemperature"}

        name = 'Plate Heat Recovery' if name is None else name
        hx = idf.newidfobject('HeatExchanger:AirToAir:SensibleAndLatent', Name=name)

        if availability_schedule is None:
            hx['Availability_Schedule_Name'] = schedule_always_on_hvac
        else:
            if isinstance(availability_schedule, EpBunch):
                hx['Availability_Schedule_Name'] = availability_schedule.Name
            elif isinstance(availability_schedule, str):
                hx['Availability_Schedule_Name'] = availability_schedule
            else:
                raise TypeError('Invalid type of availability_schedule.')

        hx['Nominal_Supply_Air_Flow_Rate'] = supply_air_flow_rate

        hx['Sensible_Effectiveness_at_100_Heating_Air_Flow'] = sensible_effectiveness_100_heating
        hx['Sensible_Effectiveness_at_100_Cooling_Air_Flow'] = sensible_effectiveness_100_cooling
        hx['Sensible_Effectiveness_at_75_Heating_Air_Flow'] = sensible_effectiveness_75_heating
        hx['Sensible_Effectiveness_at_75_Cooling_Air_Flow'] = sensible_effectiveness_75_cooling

        if sensible_only:
            hx['Latent_Effectiveness_at_100_Heating_Air_Flow'] = 0
            hx['Latent_Effectiveness_at_75_Heating_Air_Flow'] = 0
            hx['Latent_Effectiveness_at_100_Cooling_Air_Flow'] = 0
            hx['Latent_Effectiveness_at_75_Cooling_Air_Flow'] = 0
        else:
            hx['Latent_Effectiveness_at_100_Heating_Air_Flow'] = latent_effectiveness_100_heating
            hx['Latent_Effectiveness_at_100_Cooling_Air_Flow'] = latent_effectiveness_100_cooling
            hx['Latent_Effectiveness_at_75_Heating_Air_Flow'] = latent_effectiveness_75_heating
            hx['Latent_Effectiveness_at_75_Cooling_Air_Flow'] = latent_effectiveness_75_cooling

        hx['Nominal_Electric_Power'] = nominal_electric_power
        hx['Supply_Air_Outlet_Temperature_Control'] = 'Yes' if supply_air_outlet_temp_control else 'No'
        hx['Heat_Exchanger_Type'] = types[heat_exchanger_type]
        hx['Frost_Control_Type'] = frost_types[frost_control_type]
        hx['Threshold_Temperature'] = threshold_temp

        if initial_defrost_time_fraction is not None:
            hx['Initial_Defrost_Time_Fraction'] = initial_defrost_time_fraction
        if rate_of_defrost_time_fraction_increase is not None:
            hx['Rate_of_Defrost_Time_Fraction_Increase'] = rate_of_defrost_time_fraction_increase

        hx['Economizer_Lockout'] = 'Yes' if economizer_lockout else 'No'

        component = {
            'object': hx,
            'type': 'HeatExchanger:AirToAir:SensibleAndLatent',
            'supply_air_inlet_field': 'Supply_Air_Inlet_Node_Name',
            'supply_air_outlet_field': 'Supply_Air_Outlet_Node_Name',
            'exhaust_air_inlet_field': 'Exhaust_Air_Inlet_Node_Name',
            'exhaust_air_outlet_field': 'Exhaust_Air_Outlet_Node_Name',
        }

        return component

    @staticmethod
    def heat_exchanger_air_to_air_v24(
            idf: IDF,
            name: str = None,
            supply_air_flow_rate=autosize,
            sensible_only: bool = False,
            sensible_effectiveness_100_heating=0.75,
            latent_effectiveness_100_heating=0.68,
            sensible_effectiveness_100_cooling=0.75,
            latent_effectiveness_100_cooling=0.68,
            sensible_effectiveness_heat_air_flow_curve: EpBunch = None,
            latent_effectiveness_heat_air_flow_curve: EpBunch = None,
            sensible_effectiveness_cool_air_flow_curve: EpBunch = None,
            latent_effectiveness_cool_air_flow_curve: EpBunch = None,
            nominal_electric_power=0,
            supply_air_outlet_temp_control: bool = True,
            heat_exchanger_type: int = 0,
            frost_control_type: int = 0,
            threshold_temp=1.7,
            initial_defrost_time_fraction=None,
            rate_of_defrost_time_fraction_increase=None,
            economizer_lockout: bool = False,
            availability_schedule: EpBunch | str = None):
        """
        -Heat_exchanger_type: 1.Plate 2.Rotary \n
        -Frost_control_type: \n
        1.None 2.ExhaustAirRecirculation 3.ExhaustOnly 4.MinimumExhaustTemperature
        """

        types = {0: "Plate", 1: "Rotary"}
        frost_types = {0: "None", 1: "ExhaustAirRecirculation", 2: "ExhaustOnly", 3: "MinimumExhaustTemperature"}

        name = 'Plate Heat Recovery' if name is None else name
        hx = idf.newidfobject('HeatExchanger:AirToAir:SensibleAndLatent', Name=name)

        if availability_schedule is None:
            hx['Availability_Schedule_Name'] = schedule_always_on_hvac
        else:
            if isinstance(availability_schedule, EpBunch):
                hx['Availability_Schedule_Name'] = availability_schedule.Name
            elif isinstance(availability_schedule, str):
                hx['Availability_Schedule_Name'] = availability_schedule
            else:
                raise TypeError('Invalid type of availability_schedule.')

        hx['Nominal_Supply_Air_Flow_Rate'] = supply_air_flow_rate

        hx['Sensible_Effectiveness_at_100_Heating_Air_Flow'] = sensible_effectiveness_100_heating
        hx['Sensible_Effectiveness_at_100_Cooling_Air_Flow'] = sensible_effectiveness_100_cooling

        if sensible_only:
            latent_effectiveness_100_heating = 0
            latent_effectiveness_100_cooling = 0
            hx['Latent_Effectiveness_at_100_Heating_Air_Flow'] = latent_effectiveness_100_heating
            hx['Latent_Effectiveness_at_100_Cooling_Air_Flow'] = latent_effectiveness_100_cooling
        else:
            hx['Latent_Effectiveness_at_100_Heating_Air_Flow'] = latent_effectiveness_100_heating
            hx['Latent_Effectiveness_at_100_Cooling_Air_Flow'] = latent_effectiveness_100_cooling

        hx['Nominal_Electric_Power'] = nominal_electric_power
        hx['Supply_Air_Outlet_Temperature_Control'] = 'Yes' if supply_air_outlet_temp_control else 'No'
        hx['Heat_Exchanger_Type'] = types[heat_exchanger_type]
        hx['Frost_Control_Type'] = frost_types[frost_control_type]
        hx['Threshold_Temperature'] = threshold_temp

        if initial_defrost_time_fraction is not None:
            hx['Initial_Defrost_Time_Fraction'] = initial_defrost_time_fraction
        if rate_of_defrost_time_fraction_increase is not None:
            hx['Rate_of_Defrost_Time_Fraction_Increase'] = rate_of_defrost_time_fraction_increase

        hx['Economizer_Lockout'] = 'Yes' if economizer_lockout else 'No'

        # Performance Table:
        if sensible_effectiveness_heat_air_flow_curve is None:
            curve_independent_var_name = f'{name} HX_SensHeatEff_IndependentVariable'
            curve_independent_var = PerformanceTable.table_independent_variable(
                idf,
                name=curve_independent_var_name,
                interpolation_methods=1,
                extrapolation_methods=2,
                values=[0.75, 1])

            table_name = f'{name} HX_SensHeatEff'
            table = PerformanceTable.table_loop_up(
                idf,
                name=table_name,
                independent_variables=[curve_independent_var],
                output_values=[0.81, sensible_effectiveness_100_heating])
            hx['Sensible_Effectiveness_of_Heating_Air_Flow_Curve_Name'] = table.Name
        else:
            hx['Sensible_Effectiveness_of_Heating_Air_Flow_Curve_Name'] =\
                sensible_effectiveness_heat_air_flow_curve.Name

        if latent_effectiveness_heat_air_flow_curve is None:
            curve_independent_var_name = f'{name} HX_LatHeatEff_IndependentVariable'
            curve_independent_var = PerformanceTable.table_independent_variable(
                idf,
                name=curve_independent_var_name,
                interpolation_methods=1,
                extrapolation_methods=2,
                values=[0.75, 1])
            table_name = f'{name} HX_LatHeatEff'
            table = PerformanceTable.table_loop_up(
                idf,
                name=table_name,
                independent_variables=[curve_independent_var],
                output_values=[0.73, latent_effectiveness_100_heating])
            hx['Latent_Effectiveness_of_Heating_Air_Flow_Curve_Name'] = table.Name
        else:
            hx['Latent_Effectiveness_of_Heating_Air_Flow_Curve_Name'] =\
                latent_effectiveness_heat_air_flow_curve.Name

        if sensible_effectiveness_cool_air_flow_curve is None:
            curve_independent_var_name = f'{name} HX_SensCoolEff_IndependentVariable'
            curve_independent_var = PerformanceTable.table_independent_variable(
                idf,
                name=curve_independent_var_name,
                interpolation_methods=1,
                extrapolation_methods=2,
                values=[0.75, 1])
            table_name = f'{name} HX_SensCoolEff'
            table = PerformanceTable.table_loop_up(
                idf,
                name=table_name,
                independent_variables=[curve_independent_var],
                output_values=[0.81, sensible_effectiveness_100_cooling])
            hx['Sensible_Effectiveness_of_Cooling_Air_Flow_Curve_Name'] = table.Name
        else:
            hx['Sensible_Effectiveness_of_Cooling_Air_Flow_Curve_Name'] =\
                sensible_effectiveness_cool_air_flow_curve.Name

        if latent_effectiveness_cool_air_flow_curve is None:
            curve_independent_var_name = f'{name} HX_LatCoolEff_IndependentVariable'
            curve_independent_var = PerformanceTable.table_independent_variable(
                idf,
                name=curve_independent_var_name,
                interpolation_methods=1,
                extrapolation_methods=2,
                values=[0.75, 1])
            table_name = f'{name} HX_LatCoolEff'
            table = PerformanceTable.table_loop_up(
                idf,
                name=table_name,
                independent_variables=[curve_independent_var],
                output_values=[0.73, latent_effectiveness_100_cooling])
            hx['Latent_Effectiveness_of_Cooling_Air_Flow_Curve_Name'] = table.Name
        else:
            hx['Latent_Effectiveness_of_Cooling_Air_Flow_Curve_Name'] = latent_effectiveness_cool_air_flow_curve.Name

        component = {
            'object': hx,
            'type': 'HeatExchanger:AirToAir:SensibleAndLatent',
            'supply_air_inlet_field': 'Supply_Air_Inlet_Node_Name',
            'supply_air_outlet_field': 'Supply_Air_Outlet_Node_Name',
            'exhaust_air_inlet_field': 'Exhaust_Air_Inlet_Node_Name',
            'exhaust_air_outlet_field': 'Exhaust_Air_Outlet_Node_Name',
        }

        return component
