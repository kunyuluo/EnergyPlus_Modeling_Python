from eppy.modeleditor import IDF
from HVACSystem.AirLoopComponents import AirLoopComponent
from HVACSystem.SetpointManager import SetpointManager
from HVACSystem.NodeBranch import NodeBranch
from HVACSystem.Controllers import Controller
from Helper import SomeFields
from eppy.bunch_subclass import EpBunch


class AirLoop:
    @staticmethod
    def air_loop_hvac(
            idf: IDF,
            name: str = None,
            outdoor_air_stream_comp: dict | list[dict] = None,
            heat_recovery: bool = False,
            supply_branches: list[dict] = None,
            design_supply_air_flow_rate: float = None,
            design_return_air_fraction: float = 1.0,
            setpoint_manager: EpBunch = None,):
        loop_assembly = []

        name = 'Air Loop' if name is None else name

        loop = idf.newidfobject('AirLoopHVAC'.upper(), Name=name)
        loop_assembly.append(loop)

        fields = SomeFields.a_fields
        flnames = [field.replace(" ", "_") for field in fields]
        # simplify naming
        fields1 = [
            'Controllers',
            'Availability Manager',
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
        supply_outlet_nodelist = idf.newidfobject('NodeList'.upper(), Name=supply_outlet_nodelist_name)
        supply_outlet_nodelist['Node_1_Name'] = supply_outlet_node_name
        loop_assembly.append(supply_outlet_nodelist)

        demand_inlet_nodelist_name = f'{name} Demand Inlet Nodes'
        demand_inlet_node_name = demand_inlet_nodelist_name.replace('Nodes', 'Node')
        demand_inlet_nodelist = idf.newidfobject('NodeList'.upper(), Name=demand_inlet_nodelist_name)
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
        controller_list = idf.newidfobject('AirLoopHVAC:ControllerList'.upper(), Name=controller_list_name)
        loop_assembly.append(controller_list)
        for i, controller in enumerate(controllers):
            controller_list[f'Controller_{i+1}_Object_Type'] = 'Controller:WaterCoil'
            controller_list[f'Controller_{i+1}_Name'] = controller.Name
            loop_assembly.append(controller)

        # Availability Manager List:
        ###############################################################################################

            # Outdoor air system
            ###############################################################################################
            # OutdoorAirSystem:
            oa_sys_name = f'{name} Outdoor Air System'
            controller_list_name = f'{oa_sys_name} Controller List'
            equipment_list_name = f'{oa_sys_name} Equipment List'

            oa_sys = idf.newidfobject('AirLoopHVAC:OutdoorAirSystem'.upper(), Name=oa_sys_name)
            oa_sys['Controller_List_Name'] = controller_list_name
            oa_sys['Outdoor_Air_Equipment_List_Name'] = equipment_list_name
            loop_assembly.append(oa_sys)

            # Controller List:
            controller_name = f'{oa_sys_name} Controller'
            controller_list = idf.newidfobject('AirLoopHVAC:ControllerList'.upper(), Name=controller_list_name)
            controller_list['Controller_1_Object_Type'] = 'Controller:OutdoorAir'
            controller_list['Controller_1_Name'] = controller_name
            loop_assembly.append(controller_list)

            # Controller:
            controller = Controller.controller_outdoor_air(idf, controller_name)
            controller['Relief_Air_Outlet_Node_Name'] = f'{controller_name} relief_air_outlet'
            controller['Return_Air_Node_Name'] = f'{controller_name} return_air'
            controller['Mixed_Air_Node_Name'] = f'{controller_name} mixed_air'
            controller['Actuator_Node_Name'] = f'{controller_name} outdoor_air_inlet'

            oa_inlet_node_list = idf.newidfobject('OutdoorAir:NodeList'.upper())
            oa_inlet_node_list['Node_or_NodeList_Name_1'] = controller.Actuator_Node_Name

            loop_assembly.append(controller)

            # Equipment List:
            os_sys_equip_list = idf.newidfobject('AirLoopHVAC:OutdoorAirSystem:EquipmentList'.upper(), Name=equipment_list_name)

            mixer_name = f'{oa_sys_name} Outdoor Air Mixer'
            os_sys_equip_list['Component_1_Object_Type'] = 'OutdoorAir:Mixer'
            os_sys_equip_list['Component_1_Name'] = mixer_name
            loop_assembly.append(os_sys_equip_list)

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
                        loop_assembly.append(comp['object'])

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

                    loop_assembly.append(outdoor_air_stream_comp['object'])
                else:
                    raise TypeError('Invalid type of outdoor air stream components.')
            else:
                if heat_recovery:
                    hx_name = f'{oa_sys_name} Heat Exchanger'
                    hx = AirLoopComponent.heat_exchanger_air_to_air(idf, hx_name)
                    os_sys_equip_list['Component_2_Object_Type'] = hx['type']
                    os_sys_equip_list['Component_2_Name'] = hx['object'].Name

                    hx['object'].Supply_Air_Inlet_Node_Name = controller.Actuator_Node_Name
                    hx['object'].Supply_Air_Outlet_Node_Name = hx['object'].Name + '_supply_air_outlet'
                    hx['object'].Exhaust_Air_Inlet_Node_Name = controller.Relief_Air_Outlet_Node_Name
                    hx['object'].Exhaust_Air_Outlet_Node_Name = hx['object'].Name + '_exhaust_air_outlet'

                    mixer_oa_stream_name = hx['object'].Supply_Air_Outlet_Node_Name
                    mixer_ra_stream_name = hx['object'].Exhaust_Air_Inlet_Node_Name

                    loop_assembly.append(hx['object'])

            # Outdoor Air Mixer:
            oa_mixer = idf.newidfobject('OutdoorAir:Mixer'.upper(), Name=mixer_name)
            oa_mixer['Mixed_Air_Node_Name'] = controller.Mixed_Air_Node_Name
            oa_mixer['Outdoor_Air_Stream_Node_Name'] = mixer_oa_stream_name
            oa_mixer['Relief_Air_Stream_Node_Name'] = mixer_ra_stream_name
            oa_mixer['Return_Air_Stream_Node_Name'] = controller.Return_Air_Node_Name
            loop_assembly.append(oa_mixer)

        # Supply Branch List:
        ###############################################################################################
        if len(supply_branches) > 0:
            # Supply branches:
            ###############################################################################################
            supply_branch_name = f'{name} Main Branch'
            # supply_branch = NodeBranch.branch(idf, name=supply_branch_name, components=supply_branches, water_side=False)
            supply_branch = idf.newidfobject("BRANCH", Name=supply_branch_name)

            if len(supply_branches) <= 1:
                raise ValueError('Supply branches must be more than one')
            else:
                for i in range(len(supply_branches)):
                    if i == 0:
                        try:
                            inlet_name = supply_branches[i]['object'].Inlet_Node_Name
                        except:
                            inlet_name = supply_branches[i]['object'].Air_Inlet_Node_Name
                    else:
                        try:
                            inlet_name = supply_branches[i - 1]['object'].Outlet_Node_Name
                        except:
                            inlet_name = supply_branches[i - 1]['object'].Air_Outlet_Node_Name

                    supply_branch[f'Component_{i + 1}_Object_Type'] = supply_branches[0]['type']
                    supply_branch[f'Component_{i + 1}_Name'] = supply_branches[0]['object'].Name
                    supply_branch[f'Component_{i + 1}_Inlet_Node_Name'] = inlet_name

                    try:
                        supply_branch[f'Component_{i + 1}_Outlet_Node_Name'] = supply_branches[i]['object'].Outlet_Node_Name
                    except:
                        supply_branch[f'Component_{i + 1}_Outlet_Node_Name'] = supply_branches[i]['object'].Air_Outlet_Node_Name


            loop_assembly.append(supply_branch)

            # Add setpoint manager to node:
            if setpoint_manager is not None:
                setpoint_manager.Setpoint_Node_or_NodeList_Name = supply_outlet_node_name

            # Setpoint Manager:MixedAir at each node in outdoor air stream:

            # Branch List:
            branch_list = NodeBranch.branch_list(
                idf,
                name=loop.Branch_List_Name,
                branches=[supply_branch])
            loop_assembly.append(branch_list)

        return loop_assembly

