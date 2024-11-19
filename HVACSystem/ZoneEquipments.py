from eppy.modeleditor import IDF
from eppy.bunch_subclass import EpBunch
from HVACSystem.AirTerminals import AirTerminal
from HVACSystem.AirLoopComponents import AirLoopComponent


class ZoneEquipment:
    @staticmethod
    def zone_equipment_list(
            idf: IDF,
            name: str = None,
            load_distribution_scheme: int = 1,
            equipments: list[dict] = None,
            equipment_sequences: list[int] = None,):
        """
        Load Distribution Schemes:
            1: SequentialLoad,
            2: UniformLoad,
            3: UniformPLR,
            4: SequentialUniformPLR
        """
        schemes = {1: 'SequentialLoad', 2: 'UniformLoad', 3: 'UniformPLR', 4: 'SequentialUniformPLR'}

        name = 'ZoneEquipmentList' if name is None else name
        equip_list = idf.newidfobject('ZoneHVAC:EquipmentList'.upper(), Name=name)
        equip_list['Load_Distribution_Scheme'] = schemes[load_distribution_scheme]

        if equipment_sequences is None:
            equipment_sequences = []
            for i in range(len(equipments)):
                equipment_sequences.append(i+1)

        for i, equip in enumerate(equipments):
            equip_list[f'Zone_Equipment_{i+1}_Object_Type'] = equip['type']
            equip_list[f'Zone_Equipment_{i+1}_Name'] = equip['object'].Name
            equip_list[f'Zone_Equipment_{i+1}_Cooling_Sequence'] = equipment_sequences[i]
            equip_list[f'Zone_Equipment_{i+1}_Heating_or_NoLoad_Sequence'] = equipment_sequences[i]

        return equip_list

    @staticmethod
    def zone_equipment_group(
            idf: IDF,
            zones: list[EpBunch] | list[str] = None,
            air_terminal_type: int = 1,
            zone_hvac_type: int = None,
            zone_radiative_type: int = None):
        """
        Air Terminal Types: \n
            1: 'AirTerminal:SingleDuct:ConstantVolume:Reheat',
            2: 'AirTerminal:SingleDuct:ConstantVolume:NoReheat',
            3: 'AirTerminal:SingleDuct:VAV:Reheat',
            4: 'AirTerminal:SingleDuct:VAV:Reheat:VariableSpeedFan',
            5: 'AirTerminal:SingleDuct:VAV:HeatAndCool:Reheat',
            6: 'AirTerminal:SingleDuct:VAV:NoReheat',
            7: 'AirTerminal:SingleDuct:VAV:HeatAndCool:NoReheat',
            8: 'AirTerminal:SingleDuct:SeriesPIU:Reheat',
            9: 'AirTerminal:SingleDuct:ParallelPIU:Reheat',
            10: 'AirTerminal:SingleDuct:ConstantVolume:FourPipeInduction',
            11: 'AirTerminal:SingleDuct:ConstantVolume:FourPipeBeam',
            12: 'AirTerminal:SingleDuct:ConstantVolume:CooledBeam',
            13: 'AirTerminal:SingleDuct:Mixer',
            14: 'AirTerminal:DualDuct:ConstantVolume',
            15: 'AirTerminal:DualDuct:VAV',
            16: 'AirTerminal:DualDuct:VAV:OutdoorAir',

        Zone HVAC Types: \n
            1: 'ZoneHVAC:IdealLoadsAirSystem',
            2: 'ZoneHVAC:FourPipeFanCoil',
            3: 'ZoneHVAC:UnitVentilator',
            4: 'ZoneHVAC:UnitHeater',
            5: 'ZoneHVAC:EvaporativeCoolerUnit',
            6: 'ZoneHVAC:OutdoorAirUnit',
            7: 'ZoneHVAC:OutdoorAirUnit:EquipmentList',
            8: 'ZoneHVAC:WindowAirConditioner',
            9: 'ZoneHVAC:PackagedTerminalAirConditioner',
            10: 'ZoneHVAC:PackagedTerminalHeatPump',
            11: 'ZoneHVAC:RefrigerationChillerSet',
            12: 'ZoneHVAC:WaterToAirHeatPump',
            13: 'ZoneHVAC:Dehumidifier:DX',
            14: 'ZoneHVAC:EnergyRecoveryVentilator',
            15: 'ZoneHVAC:TerminalUnit:VariableRefrigerantFlow',
            16: 'ZoneHVAC:HybridUnitaryHVAC',

        Zone Radiative Unit Types:
            1: 'ZoneHVAC:Baseboard:RadiantConvective:Water',
            2: 'ZoneHVAC:Baseboard:RadiantConvective:Steam',
            3: 'ZoneHVAC:Baseboard:RadiantConvective:Electric',
            4: 'ZoneHVAC:CoolingPanel:RadiantConvective:Water',
            5: 'ZoneHVAC:Baseboard:Convective:Water',
            6: 'ZoneHVAC:Baseboard:Convective:Electric',
            7: 'ZoneHVAC:LowTemperatureRadiant:VariableFlow',
            8: 'ZoneHVAC:LowTemperatureRadiant:VariableFlow:Design',
            9: 'ZoneHVAC:LowTemperatureRadiant:ConstantFlow',
            10: 'ZoneHVAC:LowTemperatureRadiant:ConstantFlow:Design',
            11: 'ZoneHVAC:LowTemperatureRadiant:Electric',
            12: 'ZoneHVAC:LowTemperatureRadiant:SurfaceGroup',
            13: 'ZoneHVAC:HighTemperatureRadiant',
            14: 'ZoneHVAC:VentilatedSlab',
            15: 'ZoneHVAC:VentilatedSlab:SlabGroup',
        """
        Air_Terminal_types = {
            1: 'AirTerminal:SingleDuct:ConstantVolume:NoReheat',
            2: 'AirTerminal:SingleDuct:ConstantVolume:Reheat',
            3: 'AirTerminal:SingleDuct:VAV:Reheat',
            4: 'AirTerminal:SingleDuct:VAV:NoReheat',
            5: 'AirTerminal:SingleDuct:VAV:Reheat:VariableSpeedFan',
            6: 'AirTerminal:SingleDuct:VAV:HeatAndCool:Reheat',
            7: 'AirTerminal:SingleDuct:VAV:HeatAndCool:NoReheat',
            8: 'AirTerminal:SingleDuct:SeriesPIU:Reheat',
            9: 'AirTerminal:SingleDuct:ParallelPIU:Reheat',
            10: 'AirTerminal:SingleDuct:ConstantVolume:FourPipeInduction',
            11: 'AirTerminal:SingleDuct:ConstantVolume:FourPipeBeam',
            12: 'AirTerminal:SingleDuct:ConstantVolume:CooledBeam',
            13: 'AirTerminal:SingleDuct:Mixer',
            14: 'AirTerminal:DualDuct:ConstantVolume',
            15: 'AirTerminal:DualDuct:VAV',
            16: 'AirTerminal:DualDuct:VAV:OutdoorAir',
        }
        Zone_HVAC_types = {
            1: 'ZoneHVAC:IdealLoadsAirSystem',
            2: 'ZoneHVAC:FourPipeFanCoil',
            3: 'ZoneHVAC:UnitVentilator',
            4: 'ZoneHVAC:UnitHeater',
            5: 'ZoneHVAC:EvaporativeCoolerUnit',
            6: 'ZoneHVAC:OutdoorAirUnit',
            8: 'ZoneHVAC:WindowAirConditioner',
            9: 'ZoneHVAC:PackagedTerminalAirConditioner',
            10: 'ZoneHVAC:PackagedTerminalHeatPump',
            11: 'ZoneHVAC:RefrigerationChillerSet',
            12: 'ZoneHVAC:WaterToAirHeatPump',
            13: 'ZoneHVAC:Dehumidifier:DX',
            14: 'ZoneHVAC:EnergyRecoveryVentilator',
            15: 'ZoneHVAC:TerminalUnit:VariableRefrigerantFlow',
            16: 'ZoneHVAC:HybridUnitaryHVAC',
        }
        Radiative_Unit_types = {
            1: 'ZoneHVAC:Baseboard:RadiantConvective:Water',
            2: 'ZoneHVAC:Baseboard:RadiantConvective:Steam',
            3: 'ZoneHVAC:Baseboard:RadiantConvective:Electric',
            4: 'ZoneHVAC:CoolingPanel:RadiantConvective:Water',
            5: 'ZoneHVAC:Baseboard:Convective:Water',
            6: 'ZoneHVAC:Baseboard:Convective:Electric',
            7: 'ZoneHVAC:LowTemperatureRadiant:VariableFlow',
            8: 'ZoneHVAC:LowTemperatureRadiant:VariableFlow:Design',
            9: 'ZoneHVAC:LowTemperatureRadiant:ConstantFlow',
            10: 'ZoneHVAC:LowTemperatureRadiant:ConstantFlow:Design',
            11: 'ZoneHVAC:LowTemperatureRadiant:Electric',
            12: 'ZoneHVAC:LowTemperatureRadiant:SurfaceGroup',
            13: 'ZoneHVAC:HighTemperatureRadiant',
            14: 'ZoneHVAC:VentilatedSlab',
            15: 'ZoneHVAC:VentilatedSlab:SlabGroup',
        }

        terminal_type = Air_Terminal_types[air_terminal_type]
        zone_equip_type = Zone_HVAC_types[zone_hvac_type] if zone_hvac_type is not None else None
        radiative_unit_type = Radiative_Unit_types[zone_radiative_type] if zone_radiative_type is not None else None
        equip_group_assembly = []
        cooling_coils = []
        heating_coils = []
        zone_splitter_out_nodes = []
        zone_mixer_in_nodes = []

        zones = [] if zones is None else zones
        if len(zones) > 0:
            for i, zone in enumerate(zones):
                # Equipment Connections:
                ###############################################################################################
                connection = idf.newidfobject('ZoneHVAC:EquipmentConnections'.upper())

                if isinstance(zone, str):
                    zone_name = zone
                elif isinstance(zone, EpBunch):
                    zone_name = zone.Name
                else:
                    raise ValueError('zone must be a string or EpBunch')

                connection['Zone_Name'] = zone_name

                # Equipment List:
                equip_list_name = f'{zone_name} Equipment List'
                connection['Zone_Conditioning_Equipment_List_Name'] = equip_list_name

                # Inlet NodeList:
                inlet_nodelist_name = f'{zone_name} Inlet Node List'
                connection['Zone_Air_Inlet_Node_or_NodeList_Name'] = inlet_nodelist_name

                # Exhaust NodeList:
                exhaust_nodelist_name = f'{zone_name} Exhaust Node List'
                if zone_hvac_type is not None:
                    connection['Zone_Air_Exhaust_Node_or_NodeList_Name'] = exhaust_nodelist_name

                # Air Node:
                air_node_name = f'{zone_name} Air Node'
                connection['Zone_Air_Node_Name'] = air_node_name

                # Return Air NodeList:
                return_air_nodelist_name = f'{zone_name} Return Air Node List'
                connection['Zone_Return_Air_Node_or_NodeList_Name'] = return_air_nodelist_name

                equip_group_assembly.append(connection)

                # Node List:
                ###############################################################################################
                # Inlet NodeList:
                inlet_nodelist = idf.newidfobject('NodeList'.upper(), Name=inlet_nodelist_name)
                terminal_node_name = f'{zone_name} terminal outlet'
                zone_equip_node_name = f'{zone_name} zone hvac outlet'
                inlet_nodelist['Node_1_Name'] = terminal_node_name
                if zone_hvac_type is not None:
                    inlet_nodelist['Node_2_Name'] = zone_equip_node_name
                equip_group_assembly.append(inlet_nodelist)

                # Exhaust NodeList:
                if zone_hvac_type is not None:
                    exhaust_nodelist = idf.newidfobject('NodeList'.upper(), Name=exhaust_nodelist_name)
                    exhaust_nodelist['Node_1_Name'] = f'{zone_name} zone hvac inlet'
                    equip_group_assembly.append(exhaust_nodelist)

                # Return Air NodeList:
                return_air_nodelist = idf.newidfobject('NodeList'.upper(), Name=return_air_nodelist_name)
                return_air_node_name = f'{zone_name} return air inlet'
                return_air_nodelist['Node_1_Name'] = return_air_node_name
                equip_group_assembly.append(return_air_nodelist)
                zone_mixer_in_nodes.append(return_air_node_name)

                # AirDistributionUnit:
                ###############################################################################################
                air_distribute_name = f'{zone_name} Air Distribution Unit'
                air_distribute = idf.newidfobject('ZoneHVAC:AirDistributionUnit'.upper(), Name=air_distribute_name)
                air_distribute['Air_Distribution_Unit_Outlet_Node_Name'] = terminal_node_name
                air_distribute['Air_Terminal_Object_Type'] = terminal_type
                terminal_name = f'{zone_name} terminal'
                air_distribute['Air_Terminal_Name'] = terminal_name
                equip_group_assembly.append(air_distribute)

                # Air Terminal Unit:
                ###############################################################################################
                match air_terminal_type:
                    case 1:
                        terminal = AirTerminal.single_duct_constant_volume_no_reheat(idf, name=terminal_name)
                    case 3:
                        terminal = AirTerminal.single_duct_vav_reheat(idf, name=terminal_name)
                    case 4:
                        terminal = AirTerminal.single_duct_vav_no_reheat(idf, name=terminal_name)
                    case _:
                        terminal = AirTerminal.single_duct_constant_volume_no_reheat(idf, name=terminal_name)
                terminal_air_inlet = f'{zone_name} terminal inlet'
                terminal['object'][terminal['air_inlet_field']] = terminal_air_inlet
                terminal['object'][terminal['air_outlet_field']] = terminal_node_name
                zone_splitter_out_nodes.append(terminal_air_inlet)

                equip_group_assembly.append(terminal['object'])
                if 'reheat_coil' in terminal.keys():
                    heating_coils.append(terminal['reheat_coil'])
                    equip_group_assembly.append(terminal['reheat_coil'])

                equipments = [terminal]
                # Zone HVAC Equipment if available:
                ###############################################################################################
                if zone_hvac_type is not None:
                    zone_hvac_func = getattr(ZoneEquipment, 'fan_coil_unit')
                    zone_hvac_name = zone_name + ' ' + zone_equip_type.split(':')[-1]
                    zone_equip = zone_hvac_func(idf, zone_hvac_name)

                    equip_group_assembly.append(zone_equip['object'])
                    equipments.append(zone_equip)

                    if 'cooling_coil' in zone_equip.keys() and zone_equip['cooling_coil'] is not None:
                        cooling_coils.append(zone_equip['cooling_coil']['object'])
                    if 'heating_coil' in zone_equip.keys() and zone_equip['heating_coil'] is not None:
                        heating_coils.append(zone_equip['heating_coil']['object'])

                # Zone Radiative Equipment if available:
                ###############################################################################################
                # if zone_radiative_type is not None:
                #     zone_rad_unit = zone_radiative_unit['object']
                #     equip_group_assembly.append(zone_rad_unit)
                #     equipments.append(zone_rad_unit)
                #
                #     if 'cooling_coil' in zone_radiative_unit.keys() and zone_radiative_unit['cooling_coil'] is not None:
                #         cooling_coils.append(zone_radiative_unit['cooling_coil']['object'])
                #     if 'heating_coil' in zone_radiative_unit.keys() and zone_radiative_unit['heating_coil'] is not None:
                #         heating_coils.append(zone_radiative_unit['heating_coil']['object'])

                # Equipment List:
                ###############################################################################################
                equip_list = ZoneEquipment.zone_equipment_list(idf, equip_list_name, equipments=equipments)
                equip_group_assembly.append(equip_list)

            output_assembly = {
                'Equipments': equip_group_assembly,
                'Cooling_Coils': cooling_coils,
                'Heating_Coils': heating_coils,
                'Zone_Splitter_Nodes': zone_splitter_out_nodes,
                'Zone_Mixer_Nodes': zone_mixer_in_nodes,
            }

            return output_assembly

    @staticmethod
    def fan_coil_unit(
            idf: IDF,
            name: str = None,
            schedule: EpBunch | str = None,
            capacity_control_method: int = 0,
            heating_coil_type: int = 1,
            fan_pressure_rise=500,
            max_supply_air_flow_rate='AutoSize',
            low_speed_supply_air_flow_ratio=None,
            medium_speed_supply_air_flow_ratio=None,
            max_outdoor_air_flow_rate='AutoSize',
            outdoor_air_schedule=None,
            max_cold_water_flow_rate='AutoSize',
            min_cold_water_flow_rate=None,
            max_hot_water_flow_rate=None,
            min_hot_water_flow_rate=None,
            supply_air_fan_operating_mode_schedule=None,
            min_supply_air_temp_cooling='AutoSize',
            max_supply_air_temp_heating='AutoSize'):

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
        fcu = idf.newidfobject('ZoneHVAC:FourPipeFanCoil'.upper(), Name=name)

        if schedule is None:
            fcu['Availability_Schedule_Name'] = 'Always On Discrete hvac_library'
        else:
            if isinstance(schedule, EpBunch):
                fcu['Availability_Schedule_Name'] = schedule.Name
            elif isinstance(schedule, str):
                fcu['Availability_Schedule_Name'] = schedule
            else:
                raise TypeError('Invalid type of schedule.')

        # Create a OA Mixer object:
        mixer_name = f'{name} OA Mixer'
        oa_mixer = idf.newidfobject('OutdoorAir:Mixer'.upper(), Name=mixer_name)
        mixed_air_node_name = f'{mixer_name} Mixed Air Node'
        oa_node_name = f'{mixer_name} Outdoor Air Node'
        relief_air_node_name = f'{mixer_name} Relief Air Node'
        return_air_node_name = f'{mixer_name} Return Air Node'
        oa_mixer['Mixed_Air_Node_Name'] = mixed_air_node_name
        oa_mixer['Outdoor_Air_Stream_Node_Name'] = oa_node_name
        oa_mixer['Relief_Air_Stream_Node_Name'] = relief_air_node_name
        oa_mixer['Return_Air_Stream_Node_Name'] = return_air_node_name

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
        cooling_coil = AirLoopComponent.cooling_coil_water(idf, name=clg_coil_name)
        cooling_coil['object'][cooling_coil['air_inlet_field']] = fan_outlet_node_name
        clg_coil_outlet_node_name = f'{clg_coil_name} Coil Outlet Node'
        cooling_coil['object'][cooling_coil['air_outlet_field']] = clg_coil_outlet_node_name
        fcu_assembly.append(cooling_coil['object'])

        # Create a heating coil object based on control method:
        htg_coil_name = f'{name} Heating Coil'
        match heating_coil_type:
            case 1:
                heating_coil = AirLoopComponent.heating_coil_water(idf, name=htg_coil_name)
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
        if max_hot_water_flow_rate is not None:
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
