from eppy.modeleditor import IDF
from eppy.bunch_subclass import EpBunch
from HVACSystem.Controllers import Controller


class AirLoopComponent:
    @staticmethod
    def sizing(
            idf: IDF,
            airloop: EpBunch | str,
            type_of_load_to_size_on: int = 1,
            design_outdoor_air_flow_rate=None,
            central_heating_max_flow_ratio=None,
            system_outdoor_air_method: int = 1,
            max_outdoor_air_fraction: float = 1.0,
            preheat_temp=None,
            preheat_humidity_ratio=None,
            precool_temp=None,
            precool_humidity_ratio=None,
            central_cooling_supply_air_temp=None,
            central_heating_supply_air_temp=None,
            central_cooling_supply_air_humidity_ratio=None,
            central_heating_supply_air_humidity_ratio=None,
            sizing_option: int = 2,
            all_outdoor_air_cooling: bool = False,
            all_outdoor_air_heating: bool = False,
            cooling_supply_air_flow_method: int = 1,
            heating_supply_air_flow_method: int = 1,
            cooling_supply_air_flow_rate=None,
            heating_supply_air_flow_rate=None,
            cooling_supply_air_flow_rate_per_floor_area=None,
            heating_supply_air_flow_rate_per_floor_area=None,
            cooling_fraction_of_autosized_air_flow_rate=None,
            heating_fraction_of_autosized_air_flow_rate=None,
            heating_fraction_of_autosized_cooling_air_flow_rate=None,
            cooling_supply_air_flow_rate_per_unit_capacity=None,
            heating_supply_air_flow_rate_per_unit_capacity=None,
            cooling_design_capacity_method: int = 2,
            heating_design_capacity_method: int = 2,
            cooling_design_capacity=None,
            heating_design_capacity=None,
            cooling_design_capacity_per_floor_area=None,
            heating_design_capacity_per_floor_area=None,
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

        sizing = idf.newidfobject('Sizing:System'.upper())

        if isinstance(airloop, EpBunch):
            sizing['AirLoop_Name'] = airloop.Name
        elif isinstance(airloop, str):
            sizing['AirLoop_Name'] = airloop
        else:
            raise TypeError('Invalid input type of airloop.')

        sizing['Type_of_Load_to_Size_On'] = load_types[type_of_load_to_size_on]

        if design_outdoor_air_flow_rate is not None:
            sizing['Design_Outdoor_Air_Flow_Rate'] = design_outdoor_air_flow_rate
        if central_heating_max_flow_ratio is not None:
            sizing['Central_Heating_Maximum_System_Air_Flow_Ratio'] = central_heating_max_flow_ratio
        if preheat_temp is not None:
            sizing['Preheat_Design_Temperature'] = preheat_temp
        if preheat_humidity_ratio is not None:
            sizing['Preheat_Design_Humidity_Ratio'] = preheat_humidity_ratio
        if precool_temp is not None:
            sizing['Precool_Design_Temperature'] = precool_temp
        if precool_humidity_ratio is not None:
            sizing['Precool_Design_Humidity_Ratio'] = precool_humidity_ratio
        if central_cooling_supply_air_temp is not None:
            sizing['Central_Cooling_Design_Supply_Air_Temperature'] = central_cooling_supply_air_temp
        if central_heating_supply_air_temp is not None:
            sizing['Central_Heating_Design_Supply_Air_Temperature'] = central_heating_supply_air_temp
        if central_cooling_supply_air_humidity_ratio is not None:
            sizing['Central_Cooling_Design_Supply_Air_Humidity_Ratio'] = central_cooling_supply_air_humidity_ratio
        if central_heating_supply_air_humidity_ratio is not None:
            sizing['Central_Heating_Design_Supply_Air_Humidity_Ratio'] = central_heating_supply_air_humidity_ratio
        if sizing_option is not None:
            sizing['Type_of_Zone_Sum_to_Use'] = sizing_options[sizing_option]

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
        if cooling_supply_air_flow_rate is not None:
            sizing['Cooling_Supply_Air_Flow_Rate'] = cooling_supply_air_flow_rate
        else:
            sizing['Cooling_Supply_Air_Flow_Rate'] = 'Autosize'
        if heating_supply_air_flow_rate is not None:
            sizing['Heating_Supply_Air_Flow_Rate'] = heating_supply_air_flow_rate
        else:
            sizing['Heating_Supply_Air_Flow_Rate'] = 'Autosize'

        if cooling_supply_air_flow_rate_per_floor_area is not None:
            sizing['Cooling_Supply_Air_Flow_Rate_Per_Floor_Area'] = cooling_supply_air_flow_rate_per_floor_area
        if heating_supply_air_flow_rate_per_floor_area is not None:
            sizing['Heating_Supply_Air_Flow_Rate_Per_Floor_Area'] = heating_supply_air_flow_rate_per_floor_area
        if cooling_fraction_of_autosized_air_flow_rate is not None:
            sizing['Cooling_Fraction_of_Autosized_Cooling_Supply_Air_Flow_Rate'] = cooling_fraction_of_autosized_air_flow_rate
        if heating_fraction_of_autosized_air_flow_rate is not None:
            sizing['Heating_Fraction_of_Autosized_Heating_Supply_Air_Flow_Rate'] = heating_fraction_of_autosized_air_flow_rate
        if heating_fraction_of_autosized_cooling_air_flow_rate is not None:
            sizing['Heating_Fraction_of_Autosized_Cooling_Supply_Air_Flow_Rate'] = heating_fraction_of_autosized_cooling_air_flow_rate
        if cooling_supply_air_flow_rate_per_unit_capacity is not None:
            sizing['Cooling_Supply_Air_Flow_Rate_Per_Unit_Cooling_Capacity'] = cooling_supply_air_flow_rate_per_unit_capacity
        if heating_supply_air_flow_rate_per_unit_capacity is not None:
            sizing['Heating_Supply_Air_Flow_Rate_Per_Unit_Heating_Capacity'] = heating_supply_air_flow_rate_per_unit_capacity

        sizing['System_Outdoor_Air_Method'] = outdoor_air_methods[system_outdoor_air_method]
        sizing['Zone_Maximum_Outdoor_Air_Fraction'] = max_outdoor_air_fraction

        sizing['Cooling_Design_Capacity_Method'] = cooling_capacity_methods[cooling_design_capacity_method]
        sizing['Heating_Design_Capacity_Method'] = heating_capacity_methods[heating_design_capacity_method]
        if cooling_design_capacity is not None:
            sizing['Cooling_Design_Capacity'] = cooling_design_capacity
        if heating_design_capacity is not None:
            sizing['Heating_Design_Capacity'] = heating_design_capacity
        if cooling_design_capacity_per_floor_area is not None:
            sizing['Cooling_Design_Capacity_Per_Floor_Area'] = cooling_design_capacity_per_floor_area
        if heating_design_capacity_per_floor_area is not None:
            sizing['Heating_Design_Capacity_Per_Floor_Area'] = heating_design_capacity_per_floor_area
        if fraction_of_autosized_cooling_design_capacity is not None:
            sizing['Fraction_of_Autosized_Cooling_Design_Capacity'] = fraction_of_autosized_cooling_design_capacity
        if fraction_of_autosized_heating_design_capacity is not None:
            sizing['Fraction_of_Autosized_Heating_Design_Capacity'] = fraction_of_autosized_heating_design_capacity

        sizing['Central_Cooling_Capacity_Control_Method'] = cooling_control_methods[central_cooling_capacity_control_method]

        if occupant_diversity is not None:
            sizing['Occupant_Diversity'] = occupant_diversity

        return sizing

    @staticmethod
    def cooling_coil_water(
            idf: IDF,
            name: str = None,
            schedule: EpBunch | str = None,
            design_water_temp_diff: float = None,
            design_water_flow_rate=None,
            design_air_flow_rate=None,
            design_inlet_water_temp=None,
            design_inlet_air_temp=None,
            design_outlet_air_temp=None,
            design_inlet_air_humidity_ratio=None,
            design_outlet_air_humidity_ratio=None,
            type_of_analysis: int = 1,
            heat_exchanger_config: int = 1,
            control_variable: int = 1):
        """
        -Type_of_analysis: 1.SimpleAnalysis 2.DetailedAnalysis \n
        -Heat_exchanger_config: 1.CrossFlow 2.CounterFlow \n
        -Control_variable: 1.Temperature 2.HumidityRatio 3.TemperatureAndHumidityRatio \n
        """

        analysis_types = {1: "SimpleAnalysis", 2: "DetailedAnalysis"}
        hx_configs = {1: "CrossFlow", 2: "CounterFlow"}

        name = 'Coil Cooling Water' if name is None else name
        coil = idf.newidfobject('Coil:Cooling:Water'.upper(), Name=name)

        if schedule is not None:
            if isinstance(schedule, EpBunch):
                coil['Availability_Schedule_Name'] = schedule.Name
            elif isinstance(schedule, str):
                coil['Availability_Schedule_Name'] = schedule
            else:
                raise TypeError('Invalid type of schedule.')

        if design_water_temp_diff is not None:
            coil['Design_Water_Temperature_Difference'] = design_water_temp_diff
        if design_water_flow_rate is not None:
            coil['Design_Water_Flow_Rate'] = design_water_flow_rate
        if design_air_flow_rate is not None:
            coil['Design_Air_Flow_Rate'] = design_air_flow_rate
        if design_inlet_water_temp is not None:
            coil['Design_Inlet_Water_Temperature'] = design_inlet_water_temp
        if design_inlet_air_temp is not None:
            coil['Design_Inlet_Air_Temperature'] = design_inlet_air_temp
        if design_outlet_air_temp is not None:
            coil['Design_Outlet_Air_Temperature'] = design_outlet_air_temp
        if design_inlet_air_humidity_ratio is not None:
            coil['Design_Inlet_Humidity_Ratio'] = design_inlet_air_humidity_ratio
        if design_outlet_air_humidity_ratio is not None:
            coil['Design_Outlet_Humidity_Ratio'] = design_outlet_air_humidity_ratio

        coil['Type_of_Analysis'] = analysis_types[type_of_analysis]
        coil['Heat_Exchanger_Configuration'] = hx_configs[heat_exchanger_config]

        coil['Water_Inlet_Node_Name'] = f'{name}_water_inlet'
        coil['Water_Outlet_Node_Name'] = f'{name}_water_outlet'
        coil['Air_Inlet_Node_Name'] = f'{name}_air_inlet'
        coil['Air_Outlet_Node_Name'] = f'{name}_air_outlet'

        # Controller:
        controller_name = f'{name} Controller'
        controller = Controller.controller_watercoil(idf, controller_name, control_variable, 2)
        controller['Sensor_Node_Name'] = coil.Air_Outlet_Node_Name
        controller['Actuator_Variable'] = coil.Water_Inlet_Node_Name

        component = {
            'object': coil,
            'controller': controller,
            'type': 'Coil:Cooling:Water'
        }

        return component

    @staticmethod
    def heating_coil_water(
            idf: IDF,
            name: str = None,
            schedule=None,
            ufactor_times_area=None,
            max_water_flow_rate=None,
            performance_input_method: int = 1,
            rated_capacity=None,
            design_water_temp_diff: float = None,
            inlet_water_temp=None,
            inlet_air_temp=None,
            outlet_water_temp=None,
            outlet_air_temp=None,
            ratio_air_water_convection=None,
            control_variable: int = 1):
        """
        -Performance_input_method: 1.UFactorTimesAreaAndDesignWaterFlowRate 2.NominalCapacity
        """

        methods = {1: "UFactorTimesAreaAndDesignWaterFlowRate", 2: "NominalCapacity"}

        name = 'Coil Heating Water' if name is None else name
        coil = idf.newidfobject('Coil:Heating:Water'.upper(), Name=name)

        if schedule is not None:
            if isinstance(schedule, EpBunch):
                coil['Availability_Schedule_Name'] = schedule.Name
            elif isinstance(schedule, str):
                coil['Availability_Schedule_Name'] = schedule
            else:
                raise TypeError('Invalid type of schedule.')

        if ufactor_times_area is not None:
            coil['UFactor_Times_Area_Value'] = ufactor_times_area
        if max_water_flow_rate is not None:
            coil['Maximum_Water_Flow_Rate'] = max_water_flow_rate

        coil['Performance_Input_Method'] = methods[performance_input_method]
        if rated_capacity is not None:
            coil['Rated_Capacity'] = rated_capacity
        if design_water_temp_diff is not None:
            coil['Design_Water_Temperature_Difference'] = design_water_temp_diff
        if inlet_water_temp is not None:
            coil['Rated_Inlet_Water_Temperature'] = inlet_water_temp
        if inlet_air_temp is not None:
            coil['Rated_Inlet_Air_Temperature'] = inlet_air_temp
        if outlet_water_temp is not None:
            coil['Rated_Outlet_Water_Temperature'] = outlet_water_temp
        if outlet_air_temp is not None:
            coil['Rated_Outlet_Air_Temperature'] = outlet_air_temp
        if ratio_air_water_convection is not None:
            coil['Rated_Ratio_for_Air_and_Water_Convection'] = ratio_air_water_convection

        coil['Water_Inlet_Node_Name'] = f'{name}_water_inlet'
        coil['Water_Outlet_Node_Name'] = f'{name}_water_outlet'
        coil['Air_Inlet_Node_Name'] = f'{name}_air_inlet'
        coil['Air_Outlet_Node_Name'] = f'{name}_air_outlet'

        # Controller:
        controller_name = f'{name} Controller'
        controller = Controller.controller_watercoil(idf, controller_name, control_variable, 1)
        controller['Sensor_Node_Name'] = coil.Air_Outlet_Node_Name
        controller['Actuator_Variable'] = coil.Water_Inlet_Node_Name

        component = {
            'object': coil,
            'controller': controller,
            'type': 'Coil:Cooling:Water'
        }

        return component
