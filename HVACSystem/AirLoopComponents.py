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

    @staticmethod
    def heating_coil_electric(
            idf: IDF,
            name: str = None,
            schedule: EpBunch | str = None,
            efficiency=None,
            capacity=None):
        name = 'Heating Coil Electric' if name is None else name
        coil = idf.newidfobject('Coil:Heating:Electric'.upper(), Name=name)

        if schedule is not None:
            if isinstance(schedule, EpBunch):
                coil['Availability_Schedule_Name'] = schedule.Name
            elif isinstance(schedule, str):
                coil['Availability_Schedule_Name'] = schedule
            else:
                raise TypeError('Invalid type of schedule.')

        if efficiency is not None:
            coil['Efficiency'] = efficiency
        if capacity is not None:
            coil['Nominal_Capacity'] = capacity
        else:
            coil['Nominal_Capacity'] = 'Autosize'

        component = {
            'object': coil,
            'type': 'Coil:Cooling:Electric'
        }

        return component

    @staticmethod
    def heat_exchanger_air_to_air(
            idf: IDF,
            name: str = None,
            supply_air_flow_rate=None,
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
            economizer_lockout: bool = False):
        """
        -Heat_exchanger_type: 1.Plate 2.Rotary \n
        -Frost_control_type: \n
        1.None 2.ExhaustAirRecirculation 3.ExhaustOnly 4.MinimumExhaustTemperature
        """

        types = {0: "Plate", 1: "Rotary"}
        frost_types = {0: "None", 1: "ExhaustAirRecirculation", 2: "ExhaustOnly", 3: "MinimumExhaustTemperature"}

        name = 'Plate Heat Recovery' if name is None else name
        hx = idf.newidfobject('HeatExchanger:AirToAir:SensibleAndLatent'.upper(), Name=name)

        hx['Nominal_Supply_Air_Flow_Rate'] = supply_air_flow_rate if supply_air_flow_rate is not None else 'Autosize'

        if sensible_effectiveness_100_heating is not None:
            hx['Sensible_Effectiveness_at_100_Heating_Air_Flow'] = sensible_effectiveness_100_heating
        if sensible_effectiveness_100_cooling is not None:
            hx['Sensible_Effectiveness_at_100_Cooling_Air_Flow'] = sensible_effectiveness_100_cooling
        if sensible_effectiveness_75_heating is not None:
            hx['Sensible_Effectiveness_at_75_Heating_Air_Flow'] = sensible_effectiveness_75_heating
        if sensible_effectiveness_75_cooling is not None:
            hx['Sensible_Effectiveness_at_75_Cooling_Air_Flow'] = sensible_effectiveness_75_cooling

        if sensible_only:
            hx['Latent_Effectiveness_at_100_Heating_Air_Flow'] = 0
            hx['Latent_Effectiveness_at_75_Heating_Air_Flow'] = 0
            hx['Latent_Effectiveness_at_100_Cooling_Air_Flow'] = 0
            hx['Latent_Effectiveness_at_75_Cooling_Air_Flow'] = 0
        else:
            if latent_effectiveness_100_heating is not None:
                hx['Latent_Effectiveness_at_100_Heating_Air_Flow'] = latent_effectiveness_100_heating
            if latent_effectiveness_100_cooling is not None:
                hx['Latent_Effectiveness_at_100_Cooling_Air_Flow'] = latent_effectiveness_100_cooling
            if latent_effectiveness_75_heating is not None:
                hx['Latent_Effectiveness_at_75_Heating_Air_Flow'] = latent_effectiveness_75_heating
            if latent_effectiveness_75_cooling is not None:
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
            'type': 'HeatExchanger:AirToAir:SensibleAndLatent'
        }

        return component

    @staticmethod
    def outdoor_air_system(
            idf: IDF,
            name: str = None,
            outdoor_air_stream_comp: dict | list[dict] = None,
            heat_recovery: bool = False):
        oa_sys_assembly = []

        name = 'Outdoor Air System' if name is None else name
        controller_list_name = f'{name} Controller List'
        equipment_list_name = f'{name} Equipment List'

        oa_sys = idf.newidfobject('AirLoopHVAC:OutdoorAirSystem'.upper(), Name=name)
        oa_sys['Controller_List_Name'] = controller_list_name
        oa_sys['Outdoor_Air_Equipment_List_Name'] = equipment_list_name
        oa_sys_assembly.append(oa_sys)

        # Controller List:
        controller_name = f'{name} Controller'
        controller_list = idf.newidfobject('AirLoopHVAC:ControllerList'.upper(), Name=controller_list_name)
        controller_list['Controller_1_Object_Type'] = 'Controller:OutdoorAir'
        controller_list['Controller_1_Name'] = controller_name
        oa_sys_assembly.append(controller_list)

        # Controller:
        controller = Controller.controller_outdoor_air(idf, controller_name)
        controller['Relief_Air_Outlet_Node_Name'] = f'{controller_name} relief_air_outlet'
        controller['Return_Air_Node_Name'] = f'{controller_name} return_air'
        controller['Mixed_Air_Node_Name'] = f'{controller_name} mixed_air'
        controller['Actuator_Node_Name'] = f'{controller_name} outdoor_air_inlet'

        oa_inlet_node_list = idf.newidfobject('OutdoorAir:NodeList'.upper())
        oa_inlet_node_list['Node_or_NodeList_Name_1'] = controller.Actuator_Node_Name

        oa_sys_assembly.append(controller)

        # Equipment List:
        os_sys_equip_list = idf.newidfobject('AirLoopHVAC:OutdoorAirSystem:EquipmentList'.upper(), Name=equipment_list_name)

        mixer_name = f'{name} Outdoor Air Mixer'
        os_sys_equip_list['Component_1_Object_Type'] = 'OutdoorAir:Mixer'
        os_sys_equip_list['Component_1_Name'] = mixer_name
        oa_sys_assembly.append(os_sys_equip_list)

        mixer_oa_stream_name = controller.Actuator_Node_Name
        mixer_ra_stream_name = controller.Relief_Air_Outlet_Node_Name

        if outdoor_air_stream_comp is not None:
            if isinstance(outdoor_air_stream_comp, list) and len(outdoor_air_stream_comp) > 1:
                for i, comp in enumerate(outdoor_air_stream_comp):
                    os_sys_equip_list[f'Component_{i+2}_Object_Type'] = comp['type']
                    os_sys_equip_list[f'Component_{i+2}_Name'] = comp['object'].Name
                    if i == 0:
                        comp['object'].Air_Inlet_Node_Name = controller.Actuator_Node_Name
                        comp['object'].Air_Outlet_Node_Name = comp['object'].Name + '_air_outlet'
                    elif i == len(outdoor_air_stream_comp)-1:
                        if comp['type'] != 'HeatExchanger:AirToAir:SensibleAndLatent':
                            comp['object'].Air_Inlet_Node_Name = outdoor_air_stream_comp[i-1]['object'].Air_Outlet_Node_Name
                            comp['object'].Air_Outlet_Node_Name = comp['object'].Name + '_air_outlet'

                            mixer_oa_stream_name = comp['object'].Air_Outlet_Node_Name
                        else:
                            comp['object'].Supply_Air_Inlet_Node_Name = comp['object'].Name + '_supply_air_inlet'
                            comp['object'].Supply_Air_Outlet_Node_Name = comp['object'].Name + '_supply_air_outlet'
                            comp['object'].Exhaust_Air_Inlet_Node_Name = controller.Relief_Air_Outlet_Node_Name
                            comp['object'].Exhaust_Air_Outlet_Node_Name = comp['object'].Name + '_exhaust_air_outlet'

                            mixer_oa_stream_name = comp['object'].Supply_Air_Outlet_Node_Name
                            mixer_ra_stream_name = comp['object'].Exhaust_Air_Inlet_Node_Name
                    else:
                        pass
                    oa_sys_assembly.append(comp['object'])

            elif isinstance(outdoor_air_stream_comp, dict):
                os_sys_equip_list['Component_2_Object_Type'] = outdoor_air_stream_comp['type']
                os_sys_equip_list['Component_2_Name'] = outdoor_air_stream_comp['object'].Name
                if outdoor_air_stream_comp['type'] != 'HeatExchanger:AirToAir:SensibleAndLatent':
                    outdoor_air_stream_comp['object'].Air_Inlet_Node_Name = controller.Actuator_Node_Name
                    outdoor_air_stream_comp['object'].Air_Outlet_Node_Name = outdoor_air_stream_comp['object'].Name + '_air_outlet'

                    mixer_oa_stream_name = outdoor_air_stream_comp['object'].Air_Outlet_Node_Name
                else:
                    outdoor_air_stream_comp['object'].Supply_Air_Inlet_Node_Name = controller.Actuator_Node_Name
                    outdoor_air_stream_comp['object'].Supply_Air_Outlet_Node_Name = outdoor_air_stream_comp['object'].Name + '_supply_air_outlet'
                    outdoor_air_stream_comp['object'].Exhaust_Air_Inlet_Node_Name = controller.Relief_Air_Outlet_Node_Name
                    outdoor_air_stream_comp['object'].Exhaust_Air_Outlet_Node_Name = outdoor_air_stream_comp['object'].Name + '_exhaust_air_outlet'

                    mixer_oa_stream_name = outdoor_air_stream_comp['object'].Supply_Air_Outlet_Node_Name
                    mixer_ra_stream_name = outdoor_air_stream_comp['object'].Exhaust_Air_Inlet_Node_Name

                oa_sys_assembly.append(outdoor_air_stream_comp['object'])
            else:
                raise TypeError('Invalid type of outdoor air stream components.')
        else:
            if heat_recovery:
                hx_name = f'{name} Heat Exchanger'
                hx = AirLoopComponent.heat_exchanger_air_to_air(idf, hx_name)
                os_sys_equip_list['Component_2_Object_Type'] = hx['type']
                os_sys_equip_list['Component_2_Name'] = hx['object'].Name

                hx['object'].Supply_Air_Inlet_Node_Name = controller.Actuator_Node_Name
                hx['object'].Supply_Air_Outlet_Node_Name = hx['object'].Name + '_supply_air_outlet'
                hx['object'].Exhaust_Air_Inlet_Node_Name = controller.Relief_Air_Outlet_Node_Name
                hx['object'].Exhaust_Air_Outlet_Node_Name = hx['object'].Name + '_exhaust_air_outlet'

                mixer_oa_stream_name = hx['object'].Supply_Air_Outlet_Node_Name
                mixer_ra_stream_name = hx['object'].Exhaust_Air_Inlet_Node_Name

                oa_sys_assembly.append(hx['object'])

        # Outdoor Air Mixer:
        oa_mixer = idf.newidfobject('OutdoorAir:Mixer'.upper(), Name=mixer_name)
        oa_mixer['Mixed_Air_Node_Name'] = controller.Mixed_Air_Node_Name
        oa_mixer['Outdoor_Air_Stream_Node_Name'] = mixer_oa_stream_name
        oa_mixer['Relief_Air_Stream_Node_Name'] = mixer_ra_stream_name
        oa_mixer['Return_Air_Stream_Node_Name'] = controller.Return_Air_Node_Name
        oa_sys_assembly.append(oa_mixer)

        # Setpoint Manager:MixedAir at each node in outdoor air stream:


        return oa_sys_assembly
