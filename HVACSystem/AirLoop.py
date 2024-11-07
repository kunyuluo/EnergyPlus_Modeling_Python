from eppy.modeleditor import IDF
from HVACSystem.AirLoopComponents import AirLoopComponent
from HVACSystem.SetpointManager import SetpointManager
from HVACSystem.NodeBranch import NodeBranch
from Helper import SomeFields
from eppy.bunch_subclass import EpBunch


class AirLoop:
    @staticmethod
    def air_loop_hvac(
            idf: IDF,
            name: str = None,
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

        # Supply Branch List:
        ###############################################################################################
        if len(supply_branches) > 0:
            all_supply_branches = []

            # Outdoor air system

            # Supply branches:

            # Add setpoint manager to node:
            if setpoint_manager is not None:
                setpoint_manager.Setpoint_Node_or_NodeList_Name = supply_outlet_node_name

            # Branch List:
            branch_list = NodeBranch.branch_list(
                idf,
                name=loop.Branch_List_Name,
                branches=all_supply_branches)
            loop_assembly.append(branch_list)


        return loop_assembly

