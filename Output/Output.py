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

