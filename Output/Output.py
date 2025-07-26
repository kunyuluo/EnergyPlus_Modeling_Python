from eppy.modeleditor import IDF
from eppy.bunch_subclass import EpBunch


class Output:
    @staticmethod
    def variable(
            idf: IDF,
            key_value: str = None,
            variables: str | list[str] = None,
            frequency: int = 1):
        """
        Frequency: 1: 'Hourly', 2: 'Daily', 3: 'RunPeriod', 4: 'Timestep', 5: 'Detailed'
        """

        freq = {1: 'Hourly', 2: 'Daily', 3: 'RunPeriod', 4: 'Timestep', 5: 'Detailed'}

        variables = [variables] if isinstance(variables, str) else variables
        output_vars = []
        for var in variables:
            out_var = idf.newidfobject('Output:Variable')
            if key_value is not None:
                out_var.Key_Value = key_value
            if variables is not None:
                out_var.Variable_Name = var
            out_var.Reporting_Frequency = freq[frequency]
            output_vars.append(out_var)

        return output_vars

    @staticmethod
    def ems(
            idf: IDF,
            actuator: bool = True,
            internal_variable: bool = True,
            ems_runtime_lang: bool = True):
        ems = idf.newidfobject('Output:EnergyManagementSystem')
        if actuator:
            ems.Actuator_Availability_Dictionary_Reporting = 'Verbose'
        if internal_variable:
            ems.Internal_Variable_Availability_Dictionary_Reporting = 'Verbose'
        if ems_runtime_lang:
            ems.EMS_Runtime_Language_Debug_Output_Level = 'Verbose'

        return ems

