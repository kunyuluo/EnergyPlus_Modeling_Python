from eppy.modeleditor import IDF
from eppy.bunch_subclass import EpBunch


class NodeBranch:
    @staticmethod
    def branch(
            idf: IDF,
            name: str = None,
            components: dict | list[dict] = None,
            inlet_node_name: str = None,
            outlet_node_name: str = None,
            water_side: bool = True,
            condenser_side: bool = False):
        name = 'Branch' if name is None else name
        branch = idf.newidfobject("BRANCH", Name=name)

        if isinstance(components, dict):
            components = [components]
        else:
            if len(components) > 10:
                raise ValueError("Too many components in a branch")

        if len(components) <= 1:
            branch['Component_1_Object_Type'] = components[0]['type']
            branch['Component_1_Name'] = components[0]['object'].Name
            if water_side:
                if condenser_side:
                    branch['Component_1_Inlet_Node_Name'] = components[0]['object'][
                        components[0]['condenser_water_inlet_field']]
                    branch['Component_1_Outlet_Node_Name'] = components[0]['object'][
                        components[0]['condenser_water_outlet_field']]
                else:
                    branch['Component_1_Inlet_Node_Name'] = components[0]['object'][components[0]['water_inlet_field']]
                    branch['Component_1_Outlet_Node_Name'] = components[0]['object'][components[0]['water_outlet_field']]
            else:
                branch['Component_1_Inlet_Node_Name'] = components[0]['object'][components[0]['air_inlet_field']]
                branch['Component_1_Outlet_Node_Name'] = components[0]['object'][components[0]['air_outlet_field']]
        else:
            # Find index of chiller:
            chiller_index = []
            for i in range(len(components)):
                if 'Chiller' in components[i]['type']:
                    chiller_index.append(i)

            for i in range(len(components)):
                branch[f'Component_{i + 1}_Object_Type'] = components[i]['type']
                branch[f'Component_{i + 1}_Name'] = components[i]['object'].Name

                if i == 0:
                    if water_side:
                        if condenser_side:
                            inlet_name = components[i]['object'][components[i]['condenser_water_inlet_field']]
                        else:
                            inlet_name = components[i]['object'][components[i]['water_inlet_field']]
                    else:
                        inlet_name = components[i]['object'][components[i]['air_inlet_field']]
                else:
                    if water_side:
                        if condenser_side:
                            inlet_name = components[i-1]['object'][components[i-1]['condenser_water_outlet_field']]
                        else:
                            inlet_name = components[i - 1]['object'][components[i - 1]['water_outlet_field']]
                    else:
                        inlet_name = components[i-1]['object'][components[i-1]['air_outlet_field']]

                branch[f'Component_{i + 1}_Inlet_Node_Name'] = inlet_name

                if water_side:
                    if condenser_side:
                        branch[f'Component_{i + 1}_Outlet_Node_Name'] = components[i]['object'][
                            components[i]['condenser_water_outlet_field']]
                    else:
                        branch[f'Component_{i + 1}_Outlet_Node_Name'] = components[i]['object'][
                            components[i]['water_outlet_field']]
                else:
                    branch[f'Component_{i + 1}_Outlet_Node_Name'] = components[i]['object'][
                        components[i]['air_outlet_field']]

            # Adjust inlet / outlet node name for chiller:
            for idx in chiller_index:
                branch[f'Component_{idx + 1}_Inlet_Node_Name'] = components[idx]['object'][
                    components[idx]['water_inlet_field']]
                branch[f'Component_{idx + 1}_Outlet_Node_Name'] = components[idx]['object'][
                    components[idx]['water_outlet_field']]
                if idx == 0:
                    branch[f'Component_{idx + 2}_Inlet_Node_Name'] = components[idx]['object'][
                        components[idx]['water_outlet_field']]
                    components[idx+1]['object'][components[idx+1]['water_inlet_field']] = components[idx]['object'][
                        components[idx]['water_outlet_field']]
                elif idx == len(components) - 1:
                    branch[f'Component_{idx}_Outlet_Node_Name'] = components[idx]['object'][
                        components[idx]['water_inlet_field']]
                    components[idx-1]['object'][components[idx-1]['water_outlet_field']] = components[idx]['object'][
                        components[idx]['water_inlet_field']]
                else:
                    branch[f'Component_{idx}_Outlet_Node_Name'] = components[idx]['object'][
                        components[idx]['water_inlet_field']]
                    branch[f'Component_{idx + 2}_Inlet_Node_Name'] = components[idx]['object'][
                        components[idx]['water_outlet_field']]
                    components[idx-1]['object'][components[idx-1]['water_outlet_field']] = components[idx]['object'][
                        components[idx]['water_inlet_field']]
                    components[idx+1]['object'][components[idx+1]['water_inlet_field']] = components[idx]['object'][
                        components[idx]['water_outlet_field']]

        # Adjust inlet / outlet node name if available:
        if isinstance(components, list):
            branch_max_index = len(components)
        else:
            branch_max_index = 1
        if inlet_node_name is not None:
            branch[f'Component_{branch_max_index}_Inlet_Node_Name'] = inlet_node_name
        if outlet_node_name is not None:
            branch[f'Component_{branch_max_index}_Outlet_Node_Name'] = outlet_node_name

        return branch

    @staticmethod
    def branch_list(idf: IDF, name: str = None, branches: list[EpBunch] = None):
        name = 'BranchList' if name is None else name
        branchlist = idf.newidfobject("BRANCHLIST", Name=name)

        if len(branches) > 0:
            for i, branch in enumerate(branches, 1):
                branchlist.obj.append(branch.Name)
        else:
            raise ValueError("No branches in branch list")

        return branchlist

    @staticmethod
    def connector(
            idf: IDF,
            name: str = None,
            connector_type: int = 0,
            inlet_branch: EpBunch | list[EpBunch] = None,
            outlet_branch: EpBunch | list[EpBunch] = None):
        """
        Connector type: 0.Splitter 1.Mixer
        """
        types = {0: 'Connector:Splitter', 1: 'Connector:Mixer'}

        name = f'Connector_{types[connector_type].split(":")[-1]}' if name is None else name
        connector = idf.newidfobject(types[connector_type].upper(), Name=name)

        if connector_type == 0:  # Splitter
            # One inlet branch:
            if isinstance(inlet_branch, list):
                connector.Inlet_Branch_Name = inlet_branch[0].Name
            elif isinstance(inlet_branch, EpBunch):
                connector.Inlet_Branch_Name = inlet_branch.Name
            else:
                raise TypeError('Invalid type of inlet_branch')

            # Multiple outlet branch:
            if isinstance(outlet_branch, list):
                for i in range(len(outlet_branch)):
                    connector[f'Outlet_Branch_{i + 1}_Name'] = outlet_branch[i].Name
            elif isinstance(outlet_branch, EpBunch):
                connector['Outlet_Branch_1_Name'] = outlet_branch.Name
            else:
                raise TypeError('Invalid type of outlet_branch')

        else:  # Mixer
            # One outlet branch:
            if isinstance(outlet_branch, list):
                connector.Outlet_Branch_Name = outlet_branch[0].Name
            elif isinstance(outlet_branch, EpBunch):
                connector.Outlet_Branch_Name = outlet_branch.Name
            else:
                raise TypeError('Invalid type of outlet_branch')

            # Multiple inlet branch:
            if isinstance(inlet_branch, list):
                for i in range(len(inlet_branch)):
                    connector[f'Inlet_Branch_{i + 1}_Name'] = inlet_branch[i].Name
            elif isinstance(inlet_branch, EpBunch):
                connector['Inlet_Branch_1_Name'] = inlet_branch.Name
            else:
                raise TypeError('Invalid type of inlet_branch')

        return connector

    @staticmethod
    def connector_list(
            idf: IDF,
            name: str = None,
            splitter: str | EpBunch = None,
            mixer: str | EpBunch = None):
        name = 'ConnectorList' if name is None else name
        connector_list = idf.newidfobject("CONNECTORLIST", Name=name)
        if splitter is not None and mixer is not None:
            connector_list['Connector_1_Object_Type'] = 'Connector:Splitter'
            if isinstance(splitter, str):
                connector_list['Connector_1_Name'] = splitter
            elif isinstance(splitter, EpBunch):
                connector_list['Connector_1_Name'] = splitter.Name
            else:
                raise TypeError('Invalid type of splitter')

            connector_list['Connector_2_Object_Type'] = 'Connector:Mixer'
            if isinstance(mixer, str):
                connector_list['Connector_2_Name'] = mixer
            elif isinstance(mixer, EpBunch):
                connector_list['Connector_2_Name'] = mixer.Name
            else:
                raise TypeError('Invalid type of mixer')

        else:
            raise ValueError("Invalid connector detected.")
        return connector_list

