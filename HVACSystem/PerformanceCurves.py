from eppy.modeleditor import IDF
from eppy.bunch_subclass import EpBunch


class PerformanceCurve:

    # Input options:        # Output options:
    # ******************    # **********************
    # Dimensionless         # Dimensionless
    # Temperature           # Temperature
    # MassFlow              # Power
    # VolumetricFlow        # Capacity
    # Power
    # Distance

    @staticmethod
    def biquadratic(
            idf: IDF,
            coeff_constant=1.0,
            coeff_x=0.0,
            coeff_x2=0.0,
            coeff_y=0.0,
            coeff_y2=0.0,
            coeff_xy=0.0,
            min_x=5.0,
            max_x=10.0,
            min_y=24.0,
            max_y=35.0,
            min_out=None,
            max_out=None,
            input_unit_type_x: str = "Dimensionless",
            input_unit_type_y: str = "Dimensionless",
            output_unit_type: str = "Dimensionless",
            name: str = None):

        """
        f(x) = c1 + c2*x + c3*x^2 + c4*y + c5*y^2 + c6*x*y
        """
        name = 'Curve Biquadratic' if name is None else name
        curve = idf.newidfobject('Curve:Biquadratic'.upper(), Name=name)

        curve['Coefficient1_Constant'] = coeff_constant
        curve['Coefficient2_x'] = coeff_x
        curve['Coefficient3_x2'] = coeff_x2
        curve['Coefficient4_y'] = coeff_y
        curve['Coefficient5_y2'] = coeff_y2
        curve['Coefficient6_xy'] = coeff_xy
        curve['Minimum_Value_of_x'] = min_x
        curve['Maximum_Value_of_x'] = max_x
        curve['Minimum_Value_of_y'] = min_y
        curve['Maximum_Value_of_y'] = max_y
        if min_out is None:
            curve['Minimum_Curve_Output'] = min_out
        if max_out is None:
            curve['Maximum_Curve_Output'] = max_out
        curve['Input_Unit_Type_for_X'] = input_unit_type_x
        curve['Input_Unit_Type_for_Y'] = input_unit_type_y
        curve['Output_Unit_Type'] = output_unit_type

        return curve

    @staticmethod
    def quadratic(
            idf: IDF,
            coeff_constant=1.0,
            coeff_x=0.0,
            coeff_x2=0.0,
            min_x=0.0,
            max_x=1.0,
            min_out=None,
            max_out=None,
            input_unit_type_x: str = "Dimensionless",
            output_unit_type: str = "Dimensionless",
            name: str = None):

        """
        f(x) = c1 + c2*x + c3*x^2
        """
        name = 'Curve Quadratic' if name is None else name
        curve = idf.newidfobject('Curve:Quadratic'.upper(), Name=name)

        curve['Coefficient1_Constant'] = coeff_constant
        curve['Coefficient2_x'] = coeff_x
        curve['Coefficient3_x2'] = coeff_x2
        curve['Minimum_Value_of_x'] = min_x
        curve['Maximum_Value_of_x'] = max_x
        if min_out is None:
            curve['Minimum_Curve_Output'] = min_out
        if max_out is None:
            curve['Maximum_Curve_Output'] = max_out
        curve['Input_Unit_Type_for_X'] = input_unit_type_x
        curve['Output_Unit_Type'] = output_unit_type

        return curve

    @staticmethod
    def quartic(
            idf: IDF,
            coeff1_constant=1.0,
            coeff2_x=0.0,
            coeff3_x2=0.0,
            coeff4_x3=0.0,
            coeff5_x4=0.0,
            min_x=0.0,
            max_x=1.0,
            min_out=None,
            max_out=None,
            input_unit_type: str = "Dimensionless",
            output_unit_type: str = "Dimensionless",
            name: str = None):

        """
        f(x) = c1 + c2*x + c3*x^2 + c4*x^3 + c5*x^4
        """
        name = 'Curve Quartic' if name is None else name
        curve = idf.newidfobject('Curve:Quartic'.upper(), Name=name)

        curve['Coefficient1_Constant'] = coeff1_constant
        curve['Coefficient2_x'] = coeff2_x
        curve['Coefficient3_x2'] = coeff3_x2
        curve['Coefficient4_x3'] = coeff4_x3
        curve['Coefficient5_x4'] = coeff5_x4
        curve['Minimum_Value_of_x'] = min_x
        curve['Maximum_Value_of_x'] = max_x
        if min_out is None:
            curve['Minimum_Curve_Output'] = min_out
        if max_out is None:
            curve['Maximum_Curve_Output'] = max_out
        curve['Input_Unit_Type_for_X'] = input_unit_type
        curve['Output_Unit_Type'] = output_unit_type

        return curve

    @staticmethod
    def cubic(
            idf: IDF,
            coeff1_constant=1.0,
            coeff2_x=0.0,
            coeff3_x2=0.0,
            coeff4_x3=0.0,
            min_x=0.0,
            max_x=1.0,
            min_out=None,
            max_out=None,
            input_unit_type: str = "Dimensionless",
            output_unit_type: str = "Dimensionless",
            name: str = None):

        """
        f(x) = c1 + c2*x + c3*x^2 + c4*x^3
        """
        name = 'Curve Cubic' if name is None else name
        curve = idf.newidfobject('Curve:Cubic'.upper(), Name=name)

        curve['Coefficient1_Constant'] = coeff1_constant
        curve['Coefficient2_x'] = coeff2_x
        curve['Coefficient3_x2'] = coeff3_x2
        curve['Coefficient4_x3'] = coeff4_x3
        curve['Minimum_Value_of_x'] = min_x
        curve['Maximum_Value_of_x'] = max_x
        if min_out is None:
            curve['Minimum_Curve_Output'] = min_out
        if max_out is None:
            curve['Maximum_Curve_Output'] = max_out
        curve['Input_Unit_Type_for_X'] = input_unit_type
        curve['Output_Unit_Type'] = output_unit_type

        return curve

    @staticmethod
    def pump_curve_set(control_strategy: int = 0):
        """
        :param str control_strategy:
        0:"Linear",
        1:"VSD No Reset",
        2:"VSD Reset"
        :return: a list of coefficient values from C1 to C4
        """

        if control_strategy == 0:
            values = [0, 1, 0, 0]
        elif control_strategy == 1:
            values = [0.103, -0.04, 0.767, 0.1679]
        elif control_strategy == 2:
            values = [0.0273, -0.1317, 0.6642, 0.445]
        else:
            values = [0, 1, 0, 0]

        return values

    @staticmethod
    def fan_curve_set(control_strategy: int = 0):
        """
        :param str control_strategy:
        0:"ASHRAE 90.1 Baseline",
        1:"VSD Only",
        2:"VSD+StaticPressureControl (Good)",
        3:"VSD+StaticPressureControl (Perfect)"
        :return: a list of coefficient values from C1 to C4
        """

        if control_strategy == 0:
            values = [0.0013, 0.147, 0.9506, -0.0998, 0]
        elif control_strategy == 1:
            values = [0.070428852, 0.385330201, -0.460864118, 1.00920344, 0]
        elif control_strategy == 2:
            values = [0.04076, 0.08804, -0.07293, 0.94374, 0]
        elif control_strategy == 3:
            values = [0.02783, 0.02658, -0.08707, 1.03092, 0]
        else:
            values = [0, 1, 0, 0, 0]

        return values

    @staticmethod
    def chiller_performance_curve_ashrae_baseline(idf: IDF, name: str = None):

        """
        1.Cooling Capacity Function of Temperature Curve \n
        2.Electric Input to Cooling Output Ratio Function of Temperature Curve \n
        3.Electric Input to Cooling Output Ratio Function of Part Load Ratio Curve
        """
        curves = []
        name = 'Chiller' if name is None else name

        # Cooling Capacity Function of Temperature Curve
        curves.append(PerformanceCurve.biquadratic(
            idf, 0.258, 0.0389, -0.000217, 0.0469, -0.000943, -0.000343, 5, 10, 24, 35,
            input_unit_type_x="Temperature", input_unit_type_y="Temperature",
            name=f"{name} CoolingCapTempCurve_ASHRAE90.1"))

        # Electric Input to Cooling Output Ratio Function of Temperature Curve
        curves.append(PerformanceCurve.biquadratic(
            idf, 0.934, -0.0582, 0.0045, 0.00243, 0.000486, -0.00122, 5, 10, 24, 35,
            input_unit_type_x="Temperature", input_unit_type_y="Temperature",
            name=f"{name} CoolingEIRRatioTempCurve_ASHRAE90.1"))

        # Electric Input to Cooling Output Ratio Function of Part Load Ratio Curve
        curves.append(PerformanceCurve.quadratic(
            idf, 0.222903, 0.313387, 0.46371, 0, 1, name=f"{name} CoolingEIRRatioPLRCurve_ASHRAE90.1"))

        return curves

    @staticmethod
    def chiller_performance_curve_title24(idf: IDF, name: str = None):

        """
        1.Cooling Capacity Function of Temperature Curve \n
        2.Electric Input to Cooling Output Ratio Function of Temperature Curve \n
        3.Electric Input to Cooling Output Ratio Function of Part Load Ratio Curve
        """
        curves = []
        name = 'Chiller' if name is None else name

        # Cooling Capacity Function of Temperature Curve
        curves.append(PerformanceCurve.biquadratic(
            idf, 1.35608, 0.04875, -0.000888, -0.014525, -0.000286, -0.00004, 5, 10, 24, 35,
            input_unit_type_x="Temperature", input_unit_type_y="Temperature",
            name=f"{name} CoolingCapTempCurve_Title24"))

        # Electric Input to Cooling Output Ratio Function of Temperature Curve
        curves.append(PerformanceCurve.biquadratic(
            idf, 0.756376, -0.015019, 0.000156, 0.00246, 0.000515, -0.000687, 5, 10, 24, 35,
            input_unit_type_x="Temperature", input_unit_type_y="Temperature",
            name=f"{name} CoolingEIRRatioTempCurve_Title24"))

        # Electric Input to Cooling Output Ratio Function of Part Load Ratio Curve
        curves.append(PerformanceCurve.quadratic(
            idf, 0.055483, 0.451866, 0.488242, 0, 1, name=f"{name} CoolingEIRRatioPLRCurve_Title24"))

        return curves
