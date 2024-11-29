from eppy.modeleditor import IDF
from eppy.bunch_subclass import EpBunch


class PerformanceTable:
    @staticmethod
    def table_loop_up(
            idf: IDF,
            name: str = None,
            independent_variables: list[EpBunch] = None,
            normalization_method: int = 2,
            normalization_divisor=None,
            min_out: int | float = 0,
            max_out: int | float = 10,
            out_unit_type:int = 1,
            output_values: list[float] = None,
            test_mode: bool = False):
        """
        -Normalization Methods: 1.No 2.DivisorOnly 3.AutomaticWithDivisor \n
        -Output Unit Type: 1.Dimensionless 2.Capacity 3.Power
        """
        norm_methods = {1: 'No', 2: 'DivisorOnly', 3: 'AutomaticWithDivisor'}
        unit_types = {1: 'Dimensionless', 2: 'Capacity', 3: 'Power'}

        table_assembly = []

        output_values = [0.81, 0.76] if output_values is None else output_values
        name = 'Table Loop Up' if name is None else name
        table = idf.newidfobject('Table:Lookup', Name=name)

        independent_var_list_name = f'{name} Independent Variable List'
        independent_var_list = idf.newidfobject('Table:IndependentVariableList', Name=independent_var_list_name)

        if independent_variables is None:
            independent_var_name = f'{name} Independent Variable'
            independent_var = idf.newidfobject('Table:IndependentVariable', Name=independent_var_name)
            independent_var['Interpolation_Method'] = 'Linear'
            independent_var['Extrapolation_Method'] = 'Linear'
            independent_var['Minimum_Value'] = 0
            independent_var['Maximum_Value'] = 10
            independent_var['Unit_Type'] = 'Dimensionless'
            independent_var['Value_1'] = 0.75
            independent_var['Value_2'] = 1
            table_assembly.append(independent_var)

            independent_var_list['Independent_Variable_1_Name'] = independent_var_name
        else:
            for i, independent_variable in enumerate(independent_variables):
                independent_var_list[f'Independent_Variable_{i+1}_Name'] = independent_variable['Name']
                table_assembly.append(independent_variable)

        table_assembly.append(independent_var_list)

        table['Independent_Variable_List_Name'] = independent_var_list_name
        table['Normalization_Method'] = norm_methods[normalization_method]
        if normalization_method != 1:
            if normalization_divisor is not None:
                table['Normalization_Divisor'] = normalization_divisor
            else:
                table['Normalization_Divisor'] = output_values[-1]

        table['Minimum_Output'] = min_out
        table['Maximum_Output'] = max_out
        table['Output_Unit_Type'] = unit_types[out_unit_type]

        for i, value in enumerate(output_values):
            table[f'Output_Value_{i + 1}'] = value

        table_assembly.append(table)

        if test_mode:
            return table_assembly
        else:
            return table

    @staticmethod
    def table_independent_variable(
            idf: IDF,
            name: str = None,
            interpolation_methods: int = 1,
            extrapolation_methods: int = 1,
            min_value: int | float = 0,
            max_value: int | float = 10,
            norm_ref_value=None,
            unit_type: int = 1,
            values: list[int | float] = None):
        """
        -Interpolation Methods: 1.Linear 2.Cubic \n
        -Extrapolation Methods: 1.Constant 2.Linear \n
        -Unit Type: 1.Dimensionless 2.Temperature 3.VolumetricFlow 4.MassFlow 5.Distance 6.Power
        """
        interp_methods = {1: 'Linear', 2: 'Cubic'}
        ext_methods = {1: 'Constant', 2: 'Linear'}
        unit_types = {1: 'Dimensionless', 2: 'Temperature', 3: 'VolumetricFlow', 4: 'MassFlow', 5: 'Distance', 6: 'Power'}

        name = 'Table Independent Variable' if name is None else name
        variable = idf.newidfobject('Table:IndependentVariable', Name=name)

        variable['Interpolation_Method'] = interp_methods[interpolation_methods]
        variable['Extrapolation_Method'] = ext_methods[extrapolation_methods]
        variable['Minimum_Value'] = min_value
        variable['Maximum_Value'] = max_value
        variable['Unit_Type'] = unit_types[unit_type]
        if norm_ref_value is not None:
            variable['Normalization_Reference_Value'] = norm_ref_value

        values = [0.75, 1] if values is None else values
        for i, value in enumerate(values):
            variable[f'Value_{i + 1}'] = value

        return variable
