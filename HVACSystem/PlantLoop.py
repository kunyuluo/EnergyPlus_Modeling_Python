from eppy.modeleditor import IDF
from HVACSystem.PlantLoopComponents import PlantLoopComponent
from HVACSystem.SetpointManager import SetpointManager
from HVACSystem.NodeBranch import NodeBranch
from Helper import SomeFields
from eppy.bunch_subclass import EpBunch


class PlantLoop:
    @staticmethod
    def water_loop(
            idf: IDF,
            name: str = None,
            fluid_type: int = 1,
            max_loop_temp=None,
            min_loop_temp=None,
            max_loop_flow_rate=None,
            min_loop_flow_rate=None,
            plant_loop_volume=None,
            load_distribution_scheme: int = 1,
            demand_calculation_scheme: int = 1,
            supply_inlet_branches: dict | list[dict] = None,
            supply_branches: list[list[dict]] | list[dict] = None,
            demand_inlet_branches: dict | list[dict] = None,
            demand_branches: dict | list[dict] = None,
            common_pipe_simulation: int = 1,
            setpoint_manager: EpBunch = None,
            setpoint_manager_secondary: EpBunch = None,
            availability: EpBunch = None):
        """
        -Fluid_type:
            1:Water 2:Steam 3:PropyleneGlycol 4:EthyleneGlycol \n

        -Load_distribution_scheme:
            1:Optimal 2:SequentialLoad 3:UniformLoad 4:UniformPLR 5:SequentialUniformPLR \n

        -Demand_calculation_scheme:
            1:SingleSetpoint 2:DualSetpoint \n

        -Common_pipe_simulation:
            1:None \n
            2:CommonPipe (for secondary pump system.
            Typically, constant pump on primary side and variable speed pump on secondary side)\n
            3:TwoWayCommonPipe (for thermal energy storage system, with temperature control for
            both primary and secondary sides) \n

        -About supply branches:
            The order of components for each branch should follow the stream flow direction.
            (e.g. inlet --> pump --> chiller --> outlet. Then the list should be like [pump, chiller])
        """

        plant_assembly = []

        fluid_types = {1: "Water", 2: "Steam", 3: "PropyleneGlycol", 4: "EthyleneGlycol"}
        load_distribution_schemes = {1: "Optimal", 2: "SequentialLoad", 3: "UniformLoad",
                                     4: "UniformPLR", 5: "SequentialUniformPLR"}
        demand_calc_schemes = {1: "SingleSetpoint", 2: "DualSetpoint"}
        common_pipe_types = {1: "None", 2: "CommonPipe", 3: "TwoWayCommonPipe"}

        name = 'Chilled Water Loop' if name is None else name

        plant_configs = {
            'Name': name,
            "Fluid_Type": fluid_types[fluid_type],
            "Load_Distribution_Scheme": load_distribution_schemes[load_distribution_scheme],
            'Plant_Loop_Demand_Calculation_Scheme': demand_calc_schemes[demand_calculation_scheme],
            "Common_Pipe_Simulation": common_pipe_types[common_pipe_simulation],
        }
        if max_loop_temp is not None:
            plant_configs["Maximum_Loop_Temperature"] = max_loop_temp
        if min_loop_temp is not None:
            plant_configs["Minimum_Loop_Temperature"] = min_loop_temp
        if max_loop_flow_rate is not None:
            plant_configs["Maximum_Loop_Flow Rate"] = max_loop_flow_rate
        if min_loop_flow_rate is not None:
            plant_configs["Minimum_Loop_Flow Rate"] = min_loop_flow_rate
        if plant_loop_volume is not None:
            plant_configs["Plant_Loop_Volume"] = plant_loop_volume

        plant = idf.newidfobject('PlantLoop'.upper(), **plant_configs)
        plant_assembly.append(plant)

        fields = SomeFields.p_fields
        flnames = [field.replace(" ", "_") for field in fields]
        fields1 = [field.replace("Plant Side", "Supply") for field in fields]
        fields1 = [field.replace("Demand Side", "Demand") for field in fields1]
        fields1 = [field[: field.find("Name") - 1] for field in fields1]
        fields1 = [field.replace(" Node", "") for field in fields1]
        fields1 = [field.replace(" List", "s") for field in fields1]

        fieldnames = ["%s %s" % (name, field) for field in fields1]

        for fieldname, thefield in zip(fieldnames, flnames):
            plant[thefield] = fieldname

        # make the supply branch lists for this plant loop
        ###############################################################################################
        if supply_branches is not None and isinstance(supply_branches, list):
            if len(supply_branches) != 0:
                all_supply_branches = []
                mid_branches = []

                # Supply Inlet Branch:
                if supply_inlet_branches is None:
                    pipe = PlantLoopComponent.pipe(idf, name=f'{name} Supply Inlet Branch Pipe', pipe_type=1)
                    supply_inlet_branches = [pipe]
                else:
                    supply_inlet_branches = [supply_inlet_branches] if isinstance(supply_inlet_branches, dict) else supply_inlet_branches
                inlet_branch_name = f'{name} Supply Inlet Branch'
                inlet_branch = NodeBranch.branch(idf, inlet_branch_name, supply_inlet_branches)
                all_supply_branches.append(inlet_branch)

                # for multiple branches (2-d list)
                if isinstance(supply_branches[0], list) and isinstance(supply_branches[-1], list):
                    for i, comp_list in enumerate(supply_branches):
                        branch_name = f'{name} Supply Branch {i+1}'
                        branch = NodeBranch.branch(idf, branch_name, comp_list)
                        mid_branches.append(branch)
                        all_supply_branches.append(branch)

                # for single branch (1-d list)
                else:
                    branch_name = f'{name} Supply Branch 1'
                    branch = NodeBranch.branch(idf, branch_name, supply_branches)
                    mid_branches.append(branch)
                    all_supply_branches.append(branch)

                # Supply Outlet Branch:
                outlet_pipe = PlantLoopComponent.pipe(idf, name=f'{name} Supply Outlet Branch Pipe', pipe_type=1)
                outlet_branch_name = f'{name} Supply Outlet Branch'
                outlet_branch = NodeBranch.branch(idf, outlet_branch_name, [outlet_pipe])
                all_supply_branches.append(outlet_branch)

                plant_assembly.extend(all_supply_branches)

                # Add primary side setpoint manager to node:
                if setpoint_manager is not None:
                    spm_node_name = all_supply_branches[-1].Component_2_Outlet_Node_Name
                    if spm_node_name == "":
                        spm_node_name = all_supply_branches[-1].Component_1_Outlet_Node_Name
                    setpoint_manager.Setpoint_Node_or_NodeList_Name = spm_node_name

                # Branch List:
                branch_list = NodeBranch.branch_list(
                    idf,
                    name=plant.Plant_Side_Branch_List_Name,
                    branches=all_supply_branches)
                plant_assembly.append(branch_list)

                # Connectors:
                splitter = NodeBranch.connector(
                    idf,
                    name=f'{name} Supply Splitter',
                    connector_type=0,
                    inlet_branch=all_supply_branches[0],
                    outlet_branch=mid_branches)
                mixer = NodeBranch.connector(
                    idf,
                    name=f'{name} Supply Mixer',
                    connector_type=1,
                    inlet_branch=mid_branches,
                    outlet_branch=all_supply_branches[-1])
                connector_list = NodeBranch.connector_list(
                    idf,
                    name=plant.Plant_Side_Connector_List_Name,
                    splitter=splitter,
                    mixer=mixer)
                plant_assembly.append(splitter)
                plant_assembly.append(mixer)
                plant_assembly.append(connector_list)

        else:
            raise ValueError('Need valid input for supply branches.')

        # make the demand branch lists for this plant loop
        ###############################################################################################
        if demand_branches is not None:
            all_supply_branches = []
            mid_branches = []

            # Demand Inlet Branch:
            if demand_inlet_branches is None:
                pipe = PlantLoopComponent.pipe(idf, name=f'{name} Demand Inlet Branch Pipe', pipe_type=1)
                demand_inlet_branches = [pipe]
            else:
                if common_pipe_simulation != 1:
                    demand_inlet_branches = [demand_inlet_branches] if isinstance(demand_inlet_branches, dict) else demand_inlet_branches

            inlet_branch_name = f'{name} Demand Inlet Branch'
            inlet_branch = NodeBranch.branch(idf, inlet_branch_name, demand_inlet_branches)
            all_supply_branches.append(inlet_branch)

            # Demand Inlet Branch:
            if isinstance(demand_branches, list) and len(demand_branches) > 0:
                for i, comp in enumerate(supply_branches):
                    branch_name = f'{name} Demand Branch {i + 1}'
                    branch = NodeBranch.branch(idf, branch_name, comp)
                    mid_branches.append(branch)
                    all_supply_branches.append(branch)
            elif isinstance(demand_branches, dict):
                branch_name = f'{name} Demand Branch 1'
                branch = NodeBranch.branch(idf, branch_name, demand_branches)
                mid_branches.append(branch)
                all_supply_branches.append(branch)
            else:
                raise ValueError('Need valid input for demand branches.')

            # Demand Outlet Branch:
            outlet_pipe = PlantLoopComponent.pipe(idf, name=f'{name} Demand Outlet Branch Pipe', pipe_type=1)
            outlet_branch_name = f'{name} Demand Outlet Branch'
            outlet_branch = NodeBranch.branch(idf, outlet_branch_name, [outlet_pipe])
            all_supply_branches.append(outlet_branch)

            plant_assembly.extend(all_supply_branches)

            # Branch List:
            branch_list = NodeBranch.branch_list(
                idf,
                name=plant.Demand_Side_Branch_List_Name,
                branches=all_supply_branches)
            plant_assembly.append(branch_list)

            # Connectors:
            splitter = NodeBranch.connector(
                idf,
                name=f'{name} Demand Splitter',
                connector_type=0,
                inlet_branch=all_supply_branches[0],
                outlet_branch=mid_branches)
            mixer = NodeBranch.connector(
                idf,
                name=f'{name} Demand Mixer',
                connector_type=1,
                inlet_branch=mid_branches,
                outlet_branch=all_supply_branches[-1])
            connector_list = NodeBranch.connector_list(
                idf,
                name=plant.Demand_Side_Connector_List_Name,
                splitter=splitter,
                mixer=mixer)
            plant_assembly.append(splitter)
            plant_assembly.append(mixer)
            plant_assembly.append(connector_list)

            # Add setpoint manager on secondary side if needed:
            if common_pipe_simulation == 2:
                if setpoint_manager_secondary is not None:
                    try:
                        spm_node_name = all_supply_branches[0].Component_Inlet_Node_Name_2
                    except:
                        spm_node_name = all_supply_branches[0].Component_Inlet_Node_Name_1
                    setpoint_manager_secondary.Setpoint_Node_or_NodeList_Name = spm_node_name
                else:
                    raise ValueError('Need valid input for setpoint manager on secondary side.')

        return plant_assembly
