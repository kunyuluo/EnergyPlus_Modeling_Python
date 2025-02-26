from eppy.modeleditor import IDF
from HVACSystem.AirLoopComponents import AirLoopComponent
from HVACSystem.SetpointManager import SetpointManager
from HVACSystem.AvailabilityManagers import AvailabilityManager
from HVACSystem.NodeBranch import NodeBranch
from HVACSystem.Controllers import Controller
from HVACSystem.ZoneEquipments import ZoneEquipment
from Helper import SomeFields, get_all_targets
from eppy.bunch_subclass import EpBunch


class AirLoop:
    @staticmethod
    def air_loop_hvac(
            idf: IDF,
            name: str = None,
            doas: bool = False,
            doas_control_strategy: int = 1,
            outdoor_air_stream_comp: dict | list[dict] = None,
            heat_recovery: bool = False,
            supply_branches: list[dict] = None,
            supply_fan: dict = None,
            setpoint_manager_dehumidification: EpBunch = None,
            setpoint_manager: EpBunch = None,
            zones: list[str] | list[EpBunch] = None,
            air_terminal_type: int = 1,
            vrf_system: bool = False,
            zone_air_unit_type: int = None,
            zone_radiative_type: int = None,
            design_supply_air_flow_rate: float = None,
            design_return_air_fraction: float = 1.0,
            sizing: EpBunch = None,
            availability_manager: EpBunch = None,):
        """
        Air Terminal Types:
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
            16: 'AirTerminal:DualDuct:VAV:OutdoorAir'

        Zone HVAC Types:
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
        doas_strategies = {1: 'NeutralSupplyAir', 2: 'NeutralDehumidifiedSupplyAir', 3: ' ColdSupplyAir'}

        loop_assembly = []
        water_clg_coils = []
        water_htg_coils = []
        vrf_terminals = []

        # Add water coils from supply branch if available:
        ###############################################################################################
        if supply_branches is not None and len(supply_branches) > 0:
            for item in supply_branches:
                if 'Coil' in item['type'] and 'Water' in item['type']:
                    if 'Cooling' in item['type']:
                        water_clg_coils.append(item)
                    if 'Heating' in item['type']:
                        water_htg_coils.append(item)

        # Adjust zone sizing for DOAS system if needed:
        ###############################################################################################
        if doas:
            all_sizing = get_all_targets(idf, key='Sizing:Zone', field='Zone_or_ZoneList_Name')
            all_sizing_objs = all_sizing['object']
            all_sizing_names = all_sizing['field']

            demand_zone_names = []
            for zone in zones:
                if isinstance(zone, str):
                    demand_zone_names.append(zone)
                elif isinstance(zone, EpBunch):
                    demand_zone_names.append(zone.Name)
                else:
                    raise ValueError("Zone name is not a string or EpBunch")

            for i, sizing_zone_name in enumerate(all_sizing_names):
                if sizing_zone_name in demand_zone_names:
                    sizing_obj = all_sizing_objs[i]
                    sizing_obj['Account_for_Dedicated_Outdoor_Air_System'] = 'Yes'
                    sizing_obj['Dedicated_Outdoor_Air_System_Control_Strategy'] = doas_strategies[doas_control_strategy]
                    match doas_control_strategy:
                        case 1:
                            sizing_obj['Dedicated_Outdoor_Air_Low_Setpoint_Temperature_for_Design'] = 21.1
                            sizing_obj['Dedicated_Outdoor_Air_High_Setpoint_Temperature_for_Design'] = 23.9
                        case 2:
                            sizing_obj['Dedicated_Outdoor_Air_Low_Setpoint_Temperature_for_Design'] = 14.4
                            sizing_obj['Dedicated_Outdoor_Air_High_Setpoint_Temperature_for_Design'] = 22.2
                        case 3:
                            sizing_obj['Dedicated_Outdoor_Air_Low_Setpoint_Temperature_for_Design'] = 12.2
                            sizing_obj['Dedicated_Outdoor_Air_High_Setpoint_Temperature_for_Design'] = 14.4

        # Air Loop:
        ###############################################################################################
        name = 'Air Loop' if name is None else name

        loop = idf.newidfobject('AirLoopHVAC', Name=name)
        loop_assembly.append(loop)

        # Sizing:
        ###############################################################################################
        if sizing is not None:
            sizing['AirLoop_Name'] = name
            loop_assembly.append(sizing)
        else:
            sizing = AirLoopComponent.sizing(idf, doas=doas)
            sizing['AirLoop_Name'] = name
            loop_assembly.append(sizing)

        # Field Names:
        ###############################################################################################
        fields = SomeFields.a_fields
        flnames = [field.replace(" ", "_") for field in fields]
        # simplify naming
        fields1 = [
            'Controllers',
            'Availability Manager List',
            "Branches",
            # "Connectors",
            "Supply Inlet Node",
            "Demand Outlet Node",
            "Demand Inlet Nodes",
            "Supply Outlet Nodes",
        ]

        fieldnames = ["%s %s" % (name, field) for field in fields1]
        for fieldname, thefield in zip(fieldnames, flnames):
            loop[thefield] = fieldname

        if design_supply_air_flow_rate is not None:
            loop['Design_Supply_Air_Flow_Rate'] = design_supply_air_flow_rate
        else:
            loop['Design_Supply_Air_Flow_Rate'] = 'AutoSize'
        if design_return_air_fraction is not None:
            loop['Design_Return_Air_Flow_Fraction_of_Supply_Air_Flow'] = design_return_air_fraction

        # Node List:
        ###############################################################################################
        supply_outlet_nodelist_name = f'{name} Supply Outlet Nodes'
        supply_outlet_node_name = supply_outlet_nodelist_name.replace('Nodes', 'Node')
        supply_outlet_nodelist = idf.newidfobject('NodeList', Name=supply_outlet_nodelist_name)
        supply_outlet_nodelist['Node_1_Name'] = supply_outlet_node_name
        loop_assembly.append(supply_outlet_nodelist)

        demand_inlet_nodelist_name = f'{name} Demand Inlet Nodes'
        demand_inlet_node_name = demand_inlet_nodelist_name.replace('Nodes', 'Node')
        demand_inlet_nodelist = idf.newidfobject('NodeList', Name=demand_inlet_nodelist_name)
        demand_inlet_nodelist['Node_1_Name'] = demand_inlet_node_name
        loop_assembly.append(demand_inlet_nodelist)

        # ControllerList if needed:
        ###############################################################################################
        controllers = []
        for comp in supply_branches:
            comp_type = comp['type']
            if 'Coil' in comp_type and 'Water' in comp_type:
                controllers.append(comp['controller'])

        controller_list_name = f'{name} Controllers'
        controller_list = idf.newidfobject('AirLoopHVAC:ControllerList', Name=controller_list_name)
        loop_assembly.append(controller_list)
        for i, controller in enumerate(controllers):
            controller_list[f'Controller_{i + 1}_Object_Type'] = 'Controller:WaterCoil'
            controller_list[f'Controller_{i + 1}_Name'] = controller.Name
            loop_assembly.append(controller)

        # Availability Manager List:
        ###############################################################################################
        avail_manager_list_name = f'{name} Availability Manager List'
        avail_manager_name = f'{name} Availability Manager'
        avail_manager_list = idf.newidfobject('AvailabilityManagerAssignmentList', Name=avail_manager_list_name)
        avail_manager_list['Availability_Manager_1_Object_Type'] = 'AvailabilityManager:Scheduled'
        avail_manager_list['Availability_Manager_1_Name'] = avail_manager_name
        loop_assembly.append(avail_manager_list)

        if availability_manager is not None:
            loop_assembly.append(availability_manager)
        else:
            avail_manager = AvailabilityManager.scheduled(idf, name=avail_manager_name)
            loop_assembly.append(avail_manager)

        # Outdoor air system
        ###############################################################################################
        # OutdoorAirSystem:
        oa_sys_name = f'{name} Outdoor Air System'
        controller_list_name = f'{oa_sys_name} Controller List'
        equipment_list_name = f'{oa_sys_name} Equipment List'

        oa_sys = idf.newidfobject('AirLoopHVAC:OutdoorAirSystem', Name=oa_sys_name)
        oa_sys['Controller_List_Name'] = controller_list_name
        oa_sys['Outdoor_Air_Equipment_List_Name'] = equipment_list_name
        loop_assembly.append(oa_sys)

        # Controller List:
        controller_name = f'{oa_sys_name} Controller'
        controller_list = idf.newidfobject('AirLoopHVAC:ControllerList', Name=controller_list_name)
        controller_list['Controller_1_Object_Type'] = 'Controller:OutdoorAir'
        controller_list['Controller_1_Name'] = controller_name
        loop_assembly.append(controller_list)

        # Controller:
        controller = Controller.controller_outdoor_air(idf, controller_name)
        controller['Relief_Air_Outlet_Node_Name'] = f'{controller_name} relief_air_outlet'
        controller['Return_Air_Node_Name'] = loop['Supply_Side_Inlet_Node_Name']
        controller['Mixed_Air_Node_Name'] = f'{controller_name} mixed_air'
        controller['Actuator_Node_Name'] = f'{controller_name} outdoor_air_inlet'

        oa_inlet_node_list = idf.newidfobject('OutdoorAir:NodeList')
        oa_inlet_node_list['Node_or_NodeList_Name_1'] = controller.Actuator_Node_Name

        loop_assembly.append(controller)

        # Equipment List:
        os_sys_equip_list = idf.newidfobject('AirLoopHVAC:OutdoorAirSystem:EquipmentList',
                                             Name=equipment_list_name)

        mixer_name = f'{oa_sys_name} Outdoor Air Mixer'
        os_sys_equip_list['Component_1_Object_Type'] = 'OutdoorAir:Mixer'
        os_sys_equip_list['Component_1_Name'] = mixer_name
        loop_assembly.append(os_sys_equip_list)

        mixer_oa_stream_name = controller.Actuator_Node_Name
        mixer_ra_stream_name = controller.Relief_Air_Outlet_Node_Name

        spm_nodes = []
        fan_inlet_node = None
        fan_outlet_node = None
        if outdoor_air_stream_comp is not None:
            if isinstance(outdoor_air_stream_comp, list) and len(outdoor_air_stream_comp) > 1:
                for i, comp in enumerate(outdoor_air_stream_comp):
                    os_sys_equip_list[f'Component_{i + 2}_Object_Type'] = comp['type']
                    os_sys_equip_list[f'Component_{i + 2}_Name'] = comp['object'].Name
                    if i == 0:
                        comp['object'][comp['air_inlet_field']] = controller.Actuator_Node_Name
                        comp['object'][comp['air_outlet_field']] = comp['object'].Name + '_air_outlet'
                        spm_nodes.append(comp['object'][comp['air_outlet_field']])
                    elif i == len(outdoor_air_stream_comp) - 1:
                        if comp['type'] != 'HeatExchanger:AirToAir:SensibleAndLatent':
                            comp['object'][comp['air_inlet_field']] = outdoor_air_stream_comp[i - 1][
                                'object'].Air_Outlet_Node_Name
                            comp['object'][comp['air_outlet_field']] = comp['object'].Name + '_air_outlet'

                            mixer_oa_stream_name = comp['object'][comp['air_outlet_field']]
                            spm_nodes.append(comp['object'][comp['air_outlet_field']])
                        else:
                            comp['object'][comp['supply_air_inlet_field']] =\
                                outdoor_air_stream_comp[i - 1]['object'].Air_Outlet_Node_Name
                            comp['object'][comp['supply_air_outlet_field']] = comp['object'].Name + '_supply_air_outlet'
                            comp['object'][comp['exhaust_air_inlet_field']] = controller.Relief_Air_Outlet_Node_Name
                            comp['object'][comp['exhaust_air_outlet_field']] =\
                                comp['object'].Name + '_exhaust_air_outlet'

                            mixer_oa_stream_name = comp['object'][comp['supply_air_outlet_field']]
                            mixer_ra_stream_name = comp['object'][comp['exhaust_air_inlet_field']]
                            spm_nodes.append(comp['object'][comp['supply_air_outlet_field']])
                    else:
                        pass
                    loop_assembly.append(comp['object'])

            elif isinstance(outdoor_air_stream_comp, dict):
                os_sys_equip_list['Component_2_Object_Type'] = outdoor_air_stream_comp['type']
                os_sys_equip_list['Component_2_Name'] = outdoor_air_stream_comp['object'].Name

                if outdoor_air_stream_comp['type'] != 'HeatExchanger:AirToAir:SensibleAndLatent':
                    outdoor_air_stream_comp['object'][outdoor_air_stream_comp['air_inlet_field']] = \
                        controller.Actuator_Node_Name
                    outdoor_air_stream_comp['object'][outdoor_air_stream_comp['air_outlet_field']] = \
                        outdoor_air_stream_comp['object'].Name + '_air_outlet'

                    mixer_oa_stream_name = outdoor_air_stream_comp['object'].Air_Outlet_Node_Name
                    spm_nodes.append(outdoor_air_stream_comp['object'][outdoor_air_stream_comp['air_outlet_field']])
                else:
                    outdoor_air_stream_comp['object'][outdoor_air_stream_comp['supply_air_inlet_field']] = \
                        controller.Actuator_Node_Name
                    outdoor_air_stream_comp['object'][outdoor_air_stream_comp['supply_air_outlet_field']] = \
                        outdoor_air_stream_comp['object'].Name + '_supply_air_outlet'
                    outdoor_air_stream_comp['object'][outdoor_air_stream_comp['exhaust_air_inlet_field']] = \
                        controller.Relief_Air_Outlet_Node_Name
                    outdoor_air_stream_comp['object'][outdoor_air_stream_comp['exhaust_air_outlet_field']] = \
                        outdoor_air_stream_comp['object'].Name + '_exhaust_air_outlet'

                    mixer_oa_stream_name = \
                        outdoor_air_stream_comp['object'][outdoor_air_stream_comp['supply_air_outlet_field']]
                    mixer_ra_stream_name = \
                        outdoor_air_stream_comp['object'][outdoor_air_stream_comp['exhaust_air_inlet_field']]
                    spm_nodes.append(
                        outdoor_air_stream_comp['object'][outdoor_air_stream_comp['supply_air_outlet_field']])

                loop_assembly.append(outdoor_air_stream_comp['object'])
            else:
                raise TypeError('Invalid type of outdoor air stream components.')
        else:
            if heat_recovery:
                hx_name = f'{oa_sys_name} Heat Exchanger'
                hx = AirLoopComponent.heat_exchanger_air_to_air_v24(idf, hx_name)
                # hx = AirLoopComponent.heat_exchanger_air_to_air(idf, hx_name)
                os_sys_equip_list['Component_2_Object_Type'] = hx['type']
                os_sys_equip_list['Component_2_Name'] = hx['object'].Name

                hx['object'].Supply_Air_Inlet_Node_Name = controller.Actuator_Node_Name
                hx['object'].Supply_Air_Outlet_Node_Name = hx['object'].Name + '_supply_air_outlet'
                hx['object'].Exhaust_Air_Inlet_Node_Name = controller.Relief_Air_Outlet_Node_Name
                hx['object'].Exhaust_Air_Outlet_Node_Name = hx['object'].Name + '_exhaust_air_outlet'

                mixer_oa_stream_name = hx['object'].Supply_Air_Outlet_Node_Name
                mixer_ra_stream_name = hx['object'].Exhaust_Air_Inlet_Node_Name
                spm_nodes.append(hx['object'].Supply_Air_Outlet_Node_Name)

                loop_assembly.append(hx['object'])

        # Outdoor Air Mixer:
        oa_mixer = idf.newidfobject('OutdoorAir:Mixer', Name=mixer_name)
        oa_mixer['Mixed_Air_Node_Name'] = controller.Mixed_Air_Node_Name
        oa_mixer['Outdoor_Air_Stream_Node_Name'] = mixer_oa_stream_name
        oa_mixer['Relief_Air_Stream_Node_Name'] = mixer_ra_stream_name
        oa_mixer['Return_Air_Stream_Node_Name'] = controller.Return_Air_Node_Name
        spm_nodes.append(controller.Mixed_Air_Node_Name)
        loop_assembly.append(oa_mixer)

        # Supply Branch List:
        ###############################################################################################
        if len(supply_branches) > 0:
            # Supply branches:
            ###############################################################################################
            supply_branch_name = f'{name} Main Branch'
            supply_branch = idf.newidfobject("BRANCH", Name=supply_branch_name)

            if len(supply_branches) <= 1:
                raise ValueError('Supply branches must be more than one')
            else:
                supply_branch['Component_1_Object_Type'] = 'AirLoopHVAC:OutdoorAirSystem'
                supply_branch['Component_1_Name'] = oa_sys_name
                supply_branch['Component_1_Inlet_Node_Name'] = loop['Supply_Side_Inlet_Node_Name']
                supply_branch['Component_1_Outlet_Node_Name'] = controller['Mixed_Air_Node_Name']

                for i in range(len(supply_branches)):
                    if i == 0:
                        inlet_name = controller['Mixed_Air_Node_Name']
                    else:
                        inlet_name = supply_branches[i-1]['object'][supply_branches[i - 1]['air_outlet_field']]

                    # Rename inlet / outlet node names of object:
                    supply_branches[i]['object'][supply_branches[i]['air_inlet_field']] = inlet_name

                    # Rename inlet / outlet node names in the branch
                    supply_branch[f'Component_{i + 2}_Object_Type'] = supply_branches[i]['type']
                    supply_branch[f'Component_{i + 2}_Name'] = supply_branches[i]['object'].Name
                    supply_branch[f'Component_{i + 2}_Inlet_Node_Name'] = inlet_name
                    supply_branch[f'Component_{i + 2}_Outlet_Node_Name'] = \
                        supply_branches[i]['object'][supply_branches[i]['air_outlet_field']]

                    spm_nodes.append(supply_branch[f'Component_{i + 2}_Outlet_Node_Name'])

                    # Add setpoint manager for dehumidification control if needed:
                    if supply_branches[i]['type'] == 'Coil:Cooling:Water':
                        control_var = supply_branches[i]['controller']['Control_Variable']
                        if control_var == "HumidityRatio":
                            spm_dehum_node = supply_branches[i]['object'][supply_branches[i]['air_outlet_field']]
                            if setpoint_manager_dehumidification is not None:
                                setpoint_manager_dehumidification.Setpoint_Node_or_NodeList_Name = spm_dehum_node
                                loop_assembly.append(setpoint_manager_dehumidification)
                            else:
                                spm_dehum_name = f'{name} Humidity SPM'
                                spm_dehum = SetpointManager.scheduled(
                                    idf,
                                    name=spm_dehum_name,
                                    control_variable=5,
                                    constant_value=0.008)
                                spm_dehum.Setpoint_Node_or_NodeList_Name = spm_dehum_node
                                loop_assembly.append(spm_dehum)

                    # Add Supply Fan at the end:
                    if i == len(supply_branches) - 1:
                        if supply_fan is not None:
                            supply_branch[f'Component_{i + 2}_Outlet_Node_Name'] = \
                                supply_fan['object'][supply_fan['air_inlet_field']]
                            supply_fan['object'][supply_fan['air_outlet_field']] = supply_outlet_node_name
                            fan_inlet_node = supply_fan['object'][supply_fan['air_inlet_field']]
                            fan_outlet_node = supply_outlet_node_name

                            # Rename inlet / outlet node names of object:
                            supply_branches[i]['object'][supply_branches[i]['air_outlet_field']] = fan_inlet_node
                            # Rename controller sensor node name if available:
                            if 'Coil' in supply_branches[i]['type'] and 'Water' in supply_branches[i]['type']:
                                supply_branches[i]['controller']['Sensor_Node_Name'] = fan_inlet_node
                            spm_nodes[-1] = fan_inlet_node

                            # Add fan to branch:
                            fan_index = i + 3
                            supply_branch[f'Component_{fan_index}_Object_Type'] = supply_fan['type']
                            supply_branch[f'Component_{fan_index}_Name'] = supply_fan['object'].Name
                            supply_branch[f'Component_{fan_index}_Inlet_Node_Name'] = fan_inlet_node
                            supply_branch[f'Component_{fan_index}_Outlet_Node_Name'] = fan_outlet_node

                            loop_assembly.append(supply_fan['object'])
                        else:
                            raise ValueError('Supply fan cannot be None.')

            loop_assembly.append(supply_branch)

            # Add setpoint manager to node:
            if setpoint_manager is not None:
                if isinstance(setpoint_manager, EpBunch):
                    setpoint_manager.Setpoint_Node_or_NodeList_Name = supply_outlet_node_name
                elif isinstance(setpoint_manager, dict):
                    setpoint_manager['object'].Setpoint_Node_or_NodeList_Name = supply_outlet_node_name

            # Setpoint Manager:MixedAir at each node in outdoor air stream:
            for node in spm_nodes:
                spm_mix = idf.newidfobject('SetpointManager:MixedAir', Name=f'{node} SPM')
                spm_mix['Control_Variable'] = 'Temperature'
                spm_mix['Reference_Setpoint_Node_Name'] = supply_outlet_node_name
                spm_mix['Fan_Inlet_Node_Name'] = fan_inlet_node
                spm_mix['Fan_Outlet_Node_Name'] = fan_outlet_node
                spm_mix['Setpoint_Node_or_NodeList_Name'] = node
                loop_assembly.append(spm_mix)

            # Branch List:
            branch_list = NodeBranch.branch_list(
                idf,
                name=loop.Branch_List_Name,
                branches=[supply_branch])
            loop_assembly.append(branch_list)

        # Zone Equipment List:
        ###############################################################################################
        zone_equips = ZoneEquipment.zone_equipment_group(
            idf,
            zones=zones,
            air_terminal_type=air_terminal_type,
            vrf_terminal=vrf_system,
            zone_air_unit_type=zone_air_unit_type,
            zone_radiative_type=zone_radiative_type)
        loop_assembly.extend(zone_equips['Equipments'])

        zone_splitter_nodes = zone_equips['Zone_Splitter_Nodes']
        zone_mixer_nodes = zone_equips['Zone_Mixer_Nodes']
        water_clg_coils.extend(zone_equips['Cooling_Coils'])
        water_htg_coils.extend(zone_equips['Heating_Coils'])
        vrf_terminals.extend(zone_equips['VRF_Terminals'])

        # Supply / Return Path:
        ###############################################################################################
        # Supply Path:
        supply_path_name = f'{name} Supply Path'
        zone_splitter_name = f'{name} Zone Splitter'
        supply_path = idf.newidfobject('AirLoopHVAC:SupplyPath', Name=supply_path_name)
        supply_path['Supply_Air_Path_Inlet_Node_Name'] = demand_inlet_node_name
        supply_path['Component_1_Object_Type'] = 'AirLoopHVAC:ZoneSplitter'
        supply_path['Component_1_Name'] = zone_splitter_name
        loop_assembly.append(supply_path)

        # Zone Splitter:
        zone_splitter = idf.newidfobject('AirLoopHVAC:ZoneSplitter', Name=zone_splitter_name)
        zone_splitter['Inlet_Node_Name'] = demand_inlet_node_name
        if len(zone_splitter_nodes) > 0:
            for i, node in enumerate(zone_splitter_nodes):
                zone_splitter[f'Outlet_{i+1}_Node_Name'] = node
        loop_assembly.append(zone_splitter)

        # Return Path:
        return_path_name = f'{name} Return Path'
        zone_mixer_name = f'{name} Zone Mixer'
        return_path = idf.newidfobject('AirLoopHVAC:ReturnPath', Name=return_path_name)
        return_path['Return_Air_Path_Outlet_Node_Name'] = loop.Demand_Side_Outlet_Node_Name
        return_path['Component_1_Object_Type'] = 'AirLoopHVAC:ZoneMixer'
        return_path['Component_1_Name'] = zone_mixer_name
        loop_assembly.append(return_path)

        # Zone Mixer:
        zone_mixer = idf.newidfobject('AirLoopHVAC:ZoneMixer', Name=zone_mixer_name)
        zone_mixer['Outlet_Node_Name'] = loop.Demand_Side_Outlet_Node_Name
        if len(zone_mixer_nodes) > 0:
            for i, node in enumerate(zone_mixer_nodes):
                zone_mixer[f'Inlet_{i+1}_Node_Name'] = node
        loop_assembly.append(zone_mixer)

        output_assembly = {
            'Loop': loop_assembly,
            'Cooling_Coils': water_clg_coils,
            'Heating_Coils': water_htg_coils,
            'VRF_Terminals': vrf_terminals,
        }

        return output_assembly

    @staticmethod
    def no_air_loop(
            idf: IDF,
            zones: list[str] | list[EpBunch] = None,
            vrf_system: bool = False,
            zone_air_unit_type: int = None,
            zone_radiative_type: int = None,):
        """
        Zone HVAC Types:
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
        loop_assembly = []
        water_clg_coils = []
        water_htg_coils = []
        vrf_terminals = []

        # Zone Equipment List:
        ###############################################################################################
        zone_equips = ZoneEquipment.zone_equipment_group(
            idf,
            zones=zones,
            air_terminal_type=None,
            vrf_terminal=vrf_system,
            zone_air_unit_type=zone_air_unit_type,
            zone_radiative_type=zone_radiative_type)
        loop_assembly.extend(zone_equips['Equipments'])

        water_clg_coils.extend(zone_equips['Cooling_Coils'])
        water_htg_coils.extend(zone_equips['Heating_Coils'])
        vrf_terminals.extend(zone_equips['VRF_Terminals'])

        output_assembly = {
            'Loop': loop_assembly,
            'Cooling_Coils': water_clg_coils,
            'Heating_Coils': water_htg_coils,
            'VRF_Terminals': vrf_terminals,
        }

        return output_assembly


