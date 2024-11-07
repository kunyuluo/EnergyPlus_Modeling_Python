from eppy.modeleditor import IDF
from eppy.bunch_subclass import EpBunch


class NodeBranch:
    @staticmethod
    def branch(idf: IDF, name: str = None, components: dict | list[dict] = None):
        name = 'Branch' if name is None else name
        branch = idf.newidfobject("BRANCH", Name=name)

        if isinstance(components, dict):
            components = [components]
        else:
            if len(components) > 3:
                raise ValueError("Too many components in a branch")

        if len(components) <= 1:
            branch['Component_1_Object_Type'] = components[0]['type']
            branch['Component_1_Name'] = components[0]['object'].Name
            branch['Component_1_Inlet_Node_Name'] = components[0]['object'].Inlet_Node_Name
            branch['Component_1_Outlet_Node_Name'] = components[0]['object'].Outlet_Node_Name
        else:
            for i in range(len(components)):
                if i == 0:
                    inlet_name = components[i]['object'].Inlet_Node_Name
                else:
                    inlet_name = components[i - 1]['object'].Outlet_Node_Name

                branch[f'Component_{i + 1}_Object_Type'] = components[0]['type']
                branch[f'Component_{i + 1}_Name'] = components[0]['object'].Name
                branch[f'Component_{i + 1}_Inlet_Node_Name'] = inlet_name
                branch[f'Component_{i + 1}_Outlet_Node_Name'] = components[i]['object'].Outlet_Node_Name

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