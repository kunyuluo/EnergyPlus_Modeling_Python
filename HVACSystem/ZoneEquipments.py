from eppy.modeleditor import IDF
from eppy.bunch_subclass import EpBunch
from HVACSystem.AirTerminals import AirTerminal
from HVACSystem.ZoneForcedAirUnits import ZoneForcedAirUnit
from HVACSystem.ZoneRadiativeUnits import ZoneRadiativeUnit
from Helper import get_all_targets, find_dsoa_by_zone


class ZoneEquipment:
    @staticmethod
    def zone_equipment_list(
            idf: IDF,
            name: str = None,
            load_distribution_scheme: int = 1,
            equipments: list[dict] = None,
            equipment_sequences: list[int] = None, ):
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
                equipment_sequences.append(i + 1)

        for i, equip in enumerate(equipments):
            equip_list[f'Zone_Equipment_{i + 1}_Object_Type'] = equip['type']
            equip_list[f'Zone_Equipment_{i + 1}_Name'] = equip['object'].Name
            equip_list[f'Zone_Equipment_{i + 1}_Cooling_Sequence'] = equipment_sequences[i]
            equip_list[f'Zone_Equipment_{i + 1}_Heating_or_NoLoad_Sequence'] = equipment_sequences[i]

        return equip_list

    @staticmethod
    def zone_equipment_group(
            idf: IDF,
            zones: list[EpBunch] | list[str] = None,
            air_terminal_type: int = 1,
            terminal_for_outdoor_air: bool = False,
            vrf_terminal: bool = False,
            zone_air_unit_type: int = None,
            zone_radiative_type: int = None):
        """
        Air Terminal Types: \n
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
            4: 'ZoneHVAC:Baseboard:Convective:Water',
            5: 'ZoneHVAC:Baseboard:Convective:Electric',
            6: 'ZoneHVAC:CoolingPanel:RadiantConvective:Water',
            7: 'ZoneHVAC:LowTemperatureRadiant:VariableFlow',
            8: 'ZoneHVAC:LowTemperatureRadiant:VariableFlow:Design',
            9: 'ZoneHVAC:LowTemperatureRadiant:ConstantFlow',
            10: 'ZoneHVAC:LowTemperatureRadiant:ConstantFlow:Design',
            11: 'ZoneHVAC:LowTemperatureRadiant:Electric',
            12: 'ZoneHVAC:LowTemperatureRadiant:SurfaceGroup',
            13: 'ZoneHVAC:HighTemperatureRadiant',
            14: 'ZoneHVAC:VentilatedSlab',
            15: 'ZoneHVAC:VentilatedSlab:SlabGroup'
        """
        Air_Terminal_types = {
            1: ['AirTerminal:SingleDuct:ConstantVolume:NoReheat', 'single_duct_constant_volume_no_reheat'],
            2: ['AirTerminal:SingleDuct:ConstantVolume:Reheat', None],
            3: ['AirTerminal:SingleDuct:VAV:Reheat', 'single_duct_vav_reheat'],
            4: ['AirTerminal:SingleDuct:VAV:NoReheat', 'single_duct_vav_no_reheat'],
            5: ['AirTerminal:SingleDuct:VAV:Reheat:VariableSpeedFan', None],
            6: ['AirTerminal:SingleDuct:VAV:HeatAndCool:Reheat', None],
            7: ['AirTerminal:SingleDuct:VAV:HeatAndCool:NoReheat', None],
            8: ['AirTerminal:SingleDuct:SeriesPIU:Reheat', None],
            9: ['AirTerminal:SingleDuct:ParallelPIU:Reheat', None],
            10: ['AirTerminal:SingleDuct:ConstantVolume:FourPipeInduction', None],
            11: ['AirTerminal:SingleDuct:ConstantVolume:FourPipeBeam', None],
            12: ['AirTerminal:SingleDuct:ConstantVolume:CooledBeam', None],
            13: ['AirTerminal:SingleDuct:Mixer', None],
            14: ['AirTerminal:DualDuct:ConstantVolume', None],
            15: ['AirTerminal:DualDuct:VAV', None],
            16: ['AirTerminal:DualDuct:VAV:OutdoorAir', None],
        }
        Zone_HVAC_types = {
            1: ['ZoneHVAC:IdealLoadsAirSystem', None],
            2: ['ZoneHVAC:FourPipeFanCoil', 'fan_coil_unit'],
            3: ['ZoneHVAC:UnitVentilator', None],
            4: ['ZoneHVAC:UnitHeater', None],
            5: ['ZoneHVAC:EvaporativeCoolerUnit', None],
            6: ['ZoneHVAC:OutdoorAirUnit', None],
            8: ['ZoneHVAC:WindowAirConditioner', None],
            9: ['ZoneHVAC:PackagedTerminalAirConditioner', None],
            10: ['ZoneHVAC:PackagedTerminalHeatPump', None],
            11: ['ZoneHVAC:RefrigerationChillerSet', None],
            12: ['ZoneHVAC:WaterToAirHeatPump', None],
            13: ['ZoneHVAC:Dehumidifier:DX', None],
            14: ['ZoneHVAC:EnergyRecoveryVentilator', None],
            15: ['ZoneHVAC:TerminalUnit:VariableRefrigerantFlow', None],
            16: ['ZoneHVAC:HybridUnitaryHVAC', None],
        }
        Radiative_Unit_types = {
            1: ['ZoneHVAC:Baseboard:RadiantConvective:Water', None],
            2: ['ZoneHVAC:Baseboard:RadiantConvective:Steam', None],
            3: ['ZoneHVAC:Baseboard:RadiantConvective:Electric', None],
            4: ['ZoneHVAC:Baseboard:Convective:Water', 'baseboard_convective_water'],
            5: ['ZoneHVAC:Baseboard:Convective:Electric', 'baseboard_convective_electric'],
            6: ['ZoneHVAC:CoolingPanel:RadiantConvective:Water', None],
            7: ['ZoneHVAC:LowTemperatureRadiant:VariableFlow', None],
            8: ['ZoneHVAC:LowTemperatureRadiant:VariableFlow:Design', None],
            9: ['ZoneHVAC:LowTemperatureRadiant:ConstantFlow', None],
            10: ['ZoneHVAC:LowTemperatureRadiant:ConstantFlow:Design', None],
            11: ['ZoneHVAC:LowTemperatureRadiant:Electric', None],
            12: ['ZoneHVAC:LowTemperatureRadiant:SurfaceGroup', None],
            13: ['ZoneHVAC:HighTemperatureRadiant', None],
            14: ['ZoneHVAC:VentilatedSlab', None],
            15: ['ZoneHVAC:VentilatedSlab:SlabGroup', None],
        }

        terminal_type = Air_Terminal_types[air_terminal_type][0]
        zone_equip_type = Zone_HVAC_types[zone_air_unit_type][0] if zone_air_unit_type is not None else None
        radiative_unit_type = Radiative_Unit_types[zone_radiative_type][0] if zone_radiative_type is not None else None
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
                connection = idf.newidfobject('ZoneHVAC:EquipmentConnections')

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
                if zone_air_unit_type is not None:
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
                inlet_nodelist = idf.newidfobject('NodeList', Name=inlet_nodelist_name)
                terminal_node_name = f'{zone_name} terminal outlet'
                zone_equip_node_name = f'{zone_name} zone hvac outlet'
                inlet_nodelist['Node_1_Name'] = terminal_node_name
                # if zone_air_unit_type is not None:
                #     inlet_nodelist['Node_2_Name'] = zone_equip_node_name
                equip_group_assembly.append(inlet_nodelist)

                # Exhaust NodeList:
                # if zone_air_unit_type is not None:
                #     exhaust_nodelist = idf.newidfobject('NodeList', Name=exhaust_nodelist_name)
                #     # exhaust_nodelist['Node_1_Name'] = zone_air_unit_type['object']['Air_Inlet_Node_Name']
                #     equip_group_assembly.append(exhaust_nodelist)

                # Return Air NodeList:
                return_air_nodelist = idf.newidfobject('NodeList', Name=return_air_nodelist_name)
                return_air_node_name = f'{zone_name} return air inlet'
                return_air_nodelist['Node_1_Name'] = return_air_node_name
                equip_group_assembly.append(return_air_nodelist)
                zone_mixer_in_nodes.append(return_air_node_name)

                equipments = []
                if air_terminal_type is not None:
                    # AirDistributionUnit:
                    ###############################################################################################
                    air_distribute_name = f'{zone_name} Air Distribution Unit'
                    air_distribute = AirTerminal.air_distribution_unit(idf, name=air_distribute_name)
                    air_distribute['object']['Air_Distribution_Unit_Outlet_Node_Name'] = terminal_node_name
                    air_distribute['object']['Air_Terminal_Object_Type'] = terminal_type
                    terminal_name = f'{zone_name} terminal'
                    air_distribute['object']['Air_Terminal_Name'] = terminal_name
                    equip_group_assembly.append(air_distribute['object'])

                    # Air Terminal Unit:
                    ###############################################################################################
                    terminal_func_name = Air_Terminal_types[air_terminal_type][1]
                    if terminal_func_name is not None:
                        terminal_func = getattr(AirTerminal, terminal_func_name)
                        terminal = terminal_func(idf, name=terminal_name)

                        terminal_air_inlet = f'{zone_name} terminal inlet'
                        terminal['object'][terminal['air_inlet_field']] = terminal_air_inlet
                        terminal['object'][terminal['air_outlet_field']] = terminal_node_name
                        if terminal_for_outdoor_air:
                            try:
                                dsoa_for_zone = find_dsoa_by_zone(idf, zone_name)
                                terminal['object']['Design_Specification_Outdoor_Air_Object_Name'] = dsoa_for_zone
                            except Exception:
                                pass
                        zone_splitter_out_nodes.append(terminal_air_inlet)

                        # Reheat coil if available:
                        if 'reheat_coil' in terminal.keys():
                            terminal['reheat_coil']['object'][terminal['reheat_coil']['air_outlet_field']] = terminal_node_name

                        equip_group_assembly.append(terminal['object'])
                        if 'reheat_coil' in terminal.keys():
                            heating_coils.append(terminal['reheat_coil'])
                            equip_group_assembly.append(terminal['reheat_coil']['object'])
                    else:
                        raise NotImplementedError('Air terminal type not implemented')

                    equipments.append(air_distribute)
                    
                # VRF Terminal if available:
                ###############################################################################################
                if vrf_terminal:
                    vrf_terminal_name = f'{zone_name} VRF Terminal'
                    vrf_terminal = ZoneForcedAirUnit.vrf_terminal(idf, name=vrf_terminal_name)

                    equipments.append(vrf_terminal)

                # Zone HVAC Equipment if available:
                ###############################################################################################
                if zone_air_unit_type is not None:
                    zone_hvac_func_name = Zone_HVAC_types[zone_air_unit_type][1]
                    if zone_hvac_func_name is not None:
                        zone_hvac_func = getattr(ZoneForcedAirUnit, zone_hvac_func_name)
                        zone_hvac_name = zone_name + ' ' + zone_equip_type.split(':')[-1]
                        zone_equip = zone_hvac_func(idf, zone_hvac_name)

                        equip_group_assembly.append(zone_equip['object'])
                        equipments.append(zone_equip)

                        if 'cooling_coil' in zone_equip.keys() and zone_equip['cooling_coil'] is not None:
                            cooling_coils.append(zone_equip['cooling_coil'])
                        if 'heating_coil' in zone_equip.keys() and zone_equip['heating_coil'] is not None:
                            heating_coils.append(zone_equip['heating_coil'])

                        # Add to Inlet Node List:
                        inlet_nodelist['Node_2_Name'] = zone_equip['object']['Air_Outlet_Node_Name']

                        # Add exhaust nodelist accordingly:
                        exhaust_nodelist = idf.newidfobject('NodeList', Name=exhaust_nodelist_name)
                        exhaust_nodelist['Node_1_Name'] = zone_equip['object']['Air_Inlet_Node_Name']
                        equip_group_assembly.append(exhaust_nodelist)
                    else:
                        raise NotImplementedError('Zone HVAC type not implemented')

                # Zone Radiative Equipment if available:
                ###############################################################################################
                if zone_radiative_type is not None:
                    zone_rad_func_name = Radiative_Unit_types[zone_radiative_type][1]
                    if zone_rad_func_name is not None:
                        zone_rad_func = getattr(ZoneRadiativeUnit, zone_rad_func_name)
                        zone_rad_name = zone_name + ' ' + radiative_unit_type.split(':')[1]
                        zone_rad = zone_rad_func(idf, zone_rad_name)
                        equip_group_assembly.append(zone_rad['object'])
                        equipments.append(zone_rad)

                        if 'cooling_coil' in zone_rad.keys() and zone_rad['cooling_coil'] is not None:
                            cooling_coils.append(zone_rad['cooling_coil'])
                        if 'heating_coil' in zone_rad.keys() and zone_rad['heating_coil'] is not None:
                            heating_coils.append(zone_rad['heating_coil'])
                    else:
                        raise NotImplementedError('Zone Radiative type not implemented')

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
