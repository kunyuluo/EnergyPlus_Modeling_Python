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
    def linear(
            idf: IDF,
            coeff_constant=1.0,
            coeff_x=1.0,
            min_x=0.0,
            max_x=1.0,
            min_out=None,
            max_out=None,
            input_unit_type: str = "Dimensionless",
            output_unit_type: str = "Dimensionless",
            name: str = None):
        """
        f(x) = c1 + c2*x
        """
        name = 'Curve Linear' if name is None else name
        curve = idf.newidfobject('Curve:Linear', Name=name)
        curve['Coefficient1_Constant'] = coeff_constant
        curve['Coefficient2_x'] = coeff_x
        curve['Minimum_Value_of_x'] = min_x
        curve['Maximum_Value_of_x'] = max_x
        if min_out is not None:
            curve['Minimum_Curve_Output'] = min_out
        if max_out is not None:
            curve['Maximum_Curve_Output'] = max_out
        curve['Input_Unit_Type_for_X'] = input_unit_type
        curve['Output_Unit_Type'] = output_unit_type

        return curve

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
        curve = idf.newidfobject('Curve:Biquadratic', Name=name)

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
        if min_out is not None:
            curve['Minimum_Curve_Output'] = min_out
        if max_out is not None:
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
        curve = idf.newidfobject('Curve:Quadratic', Name=name)

        curve['Coefficient1_Constant'] = coeff_constant
        curve['Coefficient2_x'] = coeff_x
        curve['Coefficient3_x2'] = coeff_x2
        curve['Minimum_Value_of_x'] = min_x
        curve['Maximum_Value_of_x'] = max_x
        if min_out is not None:
            curve['Minimum_Curve_Output'] = min_out
        if max_out is not None:
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
        curve = idf.newidfobject('Curve:Quartic', Name=name)

        curve['Coefficient1_Constant'] = coeff1_constant
        curve['Coefficient2_x'] = coeff2_x
        curve['Coefficient3_x2'] = coeff3_x2
        curve['Coefficient4_x3'] = coeff4_x3
        curve['Coefficient5_x4'] = coeff5_x4
        curve['Minimum_Value_of_x'] = min_x
        curve['Maximum_Value_of_x'] = max_x
        if min_out is not None:
            curve['Minimum_Curve_Output'] = min_out
        if max_out is not None:
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
        curve = idf.newidfobject('Curve:Cubic', Name=name)

        curve['Coefficient1_Constant'] = coeff1_constant
        curve['Coefficient2_x'] = coeff2_x
        curve['Coefficient3_x2'] = coeff3_x2
        curve['Coefficient4_x3'] = coeff4_x3
        curve['Minimum_Value_of_x'] = min_x
        curve['Maximum_Value_of_x'] = max_x
        if min_out is not None:
            curve['Minimum_Curve_Output'] = min_out
        if max_out is not None:
            curve['Maximum_Curve_Output'] = max_out
        curve['Input_Unit_Type_for_X'] = input_unit_type
        curve['Output_Unit_Type'] = output_unit_type

        return curve

    @staticmethod
    def exponent(
            idf: IDF,
            coeff1_constant=1.0,
            coeff2_constant=1.0,
            coeff3_constant=1.0,
            min_x=0.0,
            max_x=1.0,
            min_out=None,
            max_out=None,
            input_unit_type: str = "Dimensionless",
            output_unit_type: str = "Dimensionless",
            name: str = None):

        """
        f(x) = c1 + c2*x^c3
        """
        name = 'Curve Cubic' if name is None else name
        curve = idf.newidfobject('Curve:Exponent', Name=name)

        curve['Coefficient1_Constant'] = coeff1_constant
        curve['Coefficient2_Constant'] = coeff2_constant
        curve['Coefficient3_Constant'] = coeff3_constant
        curve['Minimum_Value_of_x'] = min_x
        curve['Maximum_Value_of_x'] = max_x
        if min_out is not None:
            curve['Minimum_Curve_Output'] = min_out
        if max_out is not None:
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

    @staticmethod
    def vrf_performance_curve_set_1(idf: IDF, name: str = None):

        """
        1.Cooling Capacity Ratio Boundary Curve \n
        2.Cooling Capacity Ratio Modifier Function of Low Temperature Curve \n
        3.Cooling Capacity Ratio Modifier Function of High Temperature Curve \n
        4.Cooling Energy Input Ratio Boundary Curve \n
        5.Cooling Energy Input Ratio Modifier Function of Low Temperature Curve \n
        6.Cooling Energy Input Ratio Modifier Function of High Temperature Curve \n
        7.Cooling Energy Input Ratio Modifier Function of Low Part-Load Ratio Curve \n
        8.Cooling Energy Input Ratio Modifier Function of High Part-Load Ratio Curve \n
        9.Cooling Combination Ratio Correction Factor Curve \n
        10.Cooling Part-Load Fraction Correlation Curve \n
        11.Heating Capacity Ratio Boundary Curve \n
        12.Heating Capacity Ratio Modifier Function of Low Temperature Curve \n
        13.Heating Capacity Ratio Modifier Function of High Temperature Curve \n
        14.Heating Energy Input Ratio Boundary Curve \n
        15.Heating Energy Input Ratio Modifier Function of Low Temperature Curve \n
        16.Heating Energy Input Ratio Modifier Function of High Temperature Curve \n
        17.Heating Energy Input Ratio Modifier Function of Low Part-Load Ratio Curve \n
        18.Heating Energy Input Ratio Modifier Function of High Part-Load Ratio Curve \n
        19.Heating Combination Ratio Correction Factor Curve \n
        20.Heating Part-Load Fraction Correlation Curve \n
        21.Piping Correction Factor for Length in Cooling Mode Curve \n
        22.Piping Correction Factor for Length in Heating Mode Curve \n
        23.Heat Recovery Cooling Capacity Modifier Curve \n
        24.Heat Recovery Cooling Energy Modifier Curve \n
        25.Heat Recovery Heating Capacity Modifier Curve \n
        26.Heat Recovery Heating Energy Modifier Curve
        """

        curves = {}

        name = '' if name is None else name

        # Cooling
        # ******************************************************************************
        # Cooling Capacity Ratio Boundary Curve
        curves["Cooling_Capacity_Ratio_Boundary_Curve_Name"] = \
            PerformanceCurve.cubic(idf, 25.73, -0.03150043, -0.01416595, 0, 11, 30,
                                   input_unit_type="Temperature", output_unit_type="Temperature",
                                   name=f"{name} CapRatioBoundary_Cooling")

        # Cooling Capacity Ratio Modifier Function of Low Temperature Curve
        curves["Cooling_Capacity_Ratio_Modifier_Function_of_Low_Temperature_Curve_Name"] = \
            PerformanceCurve.biquadratic(idf, 0.576882692, 0.017447952, 0.000583269,
                                         -1.76324e-06, -7.474e-09, -1.30413e-07, 15, 24, -5, 23,
                                         input_unit_type_x="Temperature", input_unit_type_y="Temperature",
                                         name=f"{name} CapRatioLowTempCurve_Cooling")

        # Cooling Capacity Ratio Modifier Function of High Temperature Curve
        curves["Cooling_Capacity_Ratio_Modifier_Function_of_High_Temperature_Curve_Name"] = \
            PerformanceCurve.biquadratic(idf, 0.6867358, 0.0207631, 0.0005447,
                                         -0.0016218, -4.259e-07, -0.0003392, 15, 24, 16, 43,
                                         input_unit_type_x="Temperature", input_unit_type_y="Temperature",
                                         name=f"{name} CapRatioHighTempCurve_Cooling")

        # Cooling Energy Input Ratio Boundary Curve
        curves["Cooling_Energy_Input_Ratio_Boundary_Curve_Name"] = \
            PerformanceCurve.cubic(idf, 25.73473775, -0.03150043, -0.01416595, 0, 15, 24,
                                   input_unit_type="Temperature", output_unit_type="Temperature",
                                   name=f"{name} EIRRatioBoundary_Cooling")

        # Cooling Energy Input Ratio Modifier Function of Low Temperature Curve
        curves["Cooling_Energy_Input_Ratio_Modifier_Function_of_Low_Temperature_Curve_Name"] = \
            PerformanceCurve.biquadratic(idf, 0.989010541, -0.02347967, 0.000199711,
                                         0.005968336, -1.0289e-07, -0.00015686, 15, 24, -5, 23,
                                         input_unit_type_x="Temperature", input_unit_type_y="Temperature",
                                         name=f"{name} EIRRatioLowTempCurve_Cooling")

        # Cooling Energy Input Ratio Modifier Function of High Temperature Curve
        curves["Cooling_Energy_Input_Ratio_Modifier_Function_of_High_Temperature_Curve_Name"] = \
            PerformanceCurve.biquadratic(idf, -1.4395110176, 0.1619850459, -0.0034911781,
                                         0.0269442645, 0.0001346163, -0.0006714941,
                                         15, 23.89, 16.8, 43.3,
                                         input_unit_type_x="Temperature", input_unit_type_y="Temperature",
                                         name=f"{name} EIRRatioHighTempCurve_Cooling")

        # Cooling Energy Input Ratio Modifier Function of Low Part-Load Ratio Curve
        curves["Cooling_Energy_Input_Ratio_Modifier_Function_of_Low_PartLoad_Ratio_Curve_Name"] = \
            PerformanceCurve.cubic(idf, 0.4541226192, -0.1729687081, 1.0828661347, -0.3618480897,
                                   0.15, 1.0,
                                   name=f"{name} EIRRatioLowPLR_Cooling")

        # Cooling Energy Input Ratio Modifier Function of High Part-Load Ratio Curve
        curves["Cooling_Energy_Input_Ratio_Modifier_Function_of_High_PartLoad_Ratio_Curve_Name"] = \
            PerformanceCurve.cubic(idf, 1, 0, 0, 0, 1.0, 1.5,
                                   name=f"{name} EIRRatioHighPLR_Cooling")

        # Cooling Combination Ratio Correction Factor Curve
        curves["Cooling_Combination_Ratio_Correction_Factor_Curve_Name"] = \
            PerformanceCurve.cubic(idf, 0.576593263, 0.6349408697, -0.3076093963, 0.0960752636,
                                   1.0, 1.5, name=f"{name} CombinationRatio_Cooling")

        # Cooling Part-Load Fraction Correlation Curve
        curves["Cooling_PartLoad_Fraction_Correlation_Curve_Name"] = \
            PerformanceCurve.linear(idf, 0.85, 0.15, 0, 1, name=f"{name} PLRFractionCorrelation_Cooling")

        # Heating
        # ******************************************************************************
        # Heating Capacity Ratio Boundary Curve
        curves["Heating_Capacity_Ratio_Boundary_Curve_Name"] = \
            PerformanceCurve.cubic(idf, 58.577, -3.0255, 0.0193, 0, 15, 23.89,
                                   input_unit_type="Temperature", output_unit_type="Temperature",
                                   name=f"{name} CapRatioBoundary_Heating")

        # Heating Capacity Ratio Modifier Function of Low Temperature Curve
        curves["Heating_Capacity_Ratio_Modifier_Function_of_Low_Temperature_Curve_Name"] = \
            PerformanceCurve.biquadratic(idf, 1.012090154, -0.0012467553, -0.0001271847,
                                         0.0267564328, -4.986e-07, -0.0002635239, 21.1, 27.2, -20, 3.33,
                                         input_unit_type_x="Temperature", input_unit_type_y="Temperature",
                                         name=f"{name} CapRatioLowTempCurve_Heating")

        # Heating Capacity Ratio Modifier Function of High Temperature Curve
        curves["Heating_Capacity_Ratio_Modifier_Function_of_High_Temperature_Curve_Name"] = \
            PerformanceCurve.biquadratic(idf, 2.5859872368, -0.0953227101, 0.0009553288,
                                         0, 0, 0, 21.1, 27.2, -9.44, 15,
                                         input_unit_type_x="Temperature", input_unit_type_y="Temperature",
                                         name=f"{name} CapRatioHighTempCurve_Heating")

        # Heating Energy Input Ratio Boundary Curve
        curves["Heating_Energy_Input_Ratio_Boundary_Curve_Name"] = \
            PerformanceCurve.cubic(idf, 58.577, -3.0255, 0.0193, 0, 15, 23.89,
                                   input_unit_type="Temperature", output_unit_type="Temperature",
                                   name=f"{name} EIRRatioBoundary_Heating")

        # Heating Energy Input Ratio Modifier Function of Low Temperature Curve
        curves["Heating_Energy_Input_Ratio_Modifier_Function_of_Low_Temperature_Curve_Name"] = \
            PerformanceCurve.biquadratic(idf, 0.7224292683, 0.0034566628, 0.0006507028,
                                         -0.0026435362, 0.0012464766, -0.0001009161,
                                         21.1, 27.2, -20, 3.33,
                                         input_unit_type_x="Temperature", input_unit_type_y="Temperature",
                                         name=f"{name} EIRRatioLowTempCurve_Heating")

        # Heating Energy Input Ratio Modifier Function of High Temperature Curve
        curves["Heating_Energy_Input_Ratio_Modifier_Function_of_High_Temperature_Curve_Name"] = \
            PerformanceCurve.biquadratic(idf, 1.3885703646, -0.0229771462, 0.000537274,
                                         -0.0273936962, 0.0004030426, -5.9786e-05,
                                         21.1, 27.2, -4.44, 13.33,
                                         input_unit_type_x="Temperature", input_unit_type_y="Temperature",
                                         name=f"{name} EIRRatioHighTempCurve_Heating")

        # Heating Energy Input Ratio Modifier Function of Low Part-Load Ratio Curve
        curves["Heating_Energy_Input_Ratio_Modifier_Function_of_Low_PartLoad_Ratio_Curve_Name"] = \
            PerformanceCurve.cubic(idf, 0.3924742025, 0.076016374, 0.6983235783, -0.1688407813,
                                   0.15, 1.0, name=f"{name} EIRRatioLowPLR_Heating")

        # Heating Energy Input Ratio Modifier Function of High Part-Load Ratio Curve
        curves["Heating_Energy_Input_Ratio_Modifier_Function_of_High_PartLoad_Ratio_Curve_Name"] = \
            PerformanceCurve.cubic(idf, 1, 0, 0, 0,
                                   1.0, 1.5, name=f"{name} EIRRatioHighPLR_Heating")

        # Heating Combination Ratio Correction Factor Curve
        curves["Heating_Combination_Ratio_Correction_Factor_Curve_Name"] = \
            PerformanceCurve.cubic(idf, 0.7667196604, 0.2617302019, -0.0159110245, -0.0125388376,
                                   1.0, 1.5, name=f"{name} CombinationRatio_Heating")

        # Heating Part-Load Fraction Correlation Curve
        curves["Heating_PartLoad_Fraction_Correlation_Curve_Name"] = \
            PerformanceCurve.linear(idf, 0.85, 0.15, 0, 1, name=f"{name} PLRFractionCorrelation_Heating")

        # Piping
        # ******************************************************************************
        # Piping Correction Factor for Length in Cooling Mode Curve
        curves["Piping_Correction_Factor_for_Length_in_Cooling_Mode_Curve_Name"] = \
            PerformanceCurve.biquadratic(idf, 2.0388158625, -0.0024260645, 3.5512e-06,
                                         -1.6858129772, 0.668703358, -4.5706e-05,
                                         7.62, 182.88, 0.8, 1.5,
                                         name=f"{name} PipingCorrectionFactorCurve_Cooling")

        # Piping Correction Factor for Length in Heating Mode Curve
        curves["Piping_Correction_Factor_for_Length_in_Heating_Mode_Curve_Name"] = \
            PerformanceCurve.biquadratic(idf, 1, 0, 0, 0, 0, 0,
                                         0, 1, 0, 1,
                                         name=f"{name} PipingCorrectionFactorCurve_Heating")

        # Heat Recovery
        # ******************************************************************************
        # Heat Recovery Cooling Capacity Modifier Curve
        curves["Heat_Recovery_Cooling_Capacity_Modifier_Curve_Name"] = \
            PerformanceCurve.biquadratic(idf, 0.9, 0, 0, 0, 0, 0,
                                         0, 1, 0, 1,
                                         name=f"{name} HeatRecoveryCapModifier_Cooling")
        # Heat Recovery Cooling Energy Modifier Curve
        curves["Heat_Recovery_Cooling_Energy_Modifier_Curve_Name"] = \
            PerformanceCurve.biquadratic(idf, 1.1, 0, 0, 0, 0, 0,
                                         0, 1, 0, 1,
                                         name=f"{name} HeatRecoveryEnergyModifier_Cooling")

        # Heat Recovery Heating Capacity Modifier Curve
        curves["Heat_Recovery_Heating_Capacity_Modifier_Curve_Name"] = \
            PerformanceCurve.biquadratic(idf, 0.9, 0, 0, 0, 0, 0,
                                         0, 1, 0, 1,
                                         name=f"{name} HeatRecoveryCapModifier_Heating")
        # Heat Recovery Heating Energy Modifier Curve
        curves["Heat_Recovery_Heating_Energy_Modifier_Curve_Name"] = \
            PerformanceCurve.biquadratic(idf, 1.1, 0, 0, 0, 0, 0,
                                         0, 1, 0, 1,
                                         name=f"{name} HeatRecoveryEnergyModifier_Heating")

        return curves

    @staticmethod
    def vrf_performance_curve_set_2(idf: IDF, name: str = None):

        """
        1.Cooling Capacity Ratio Boundary Curve \n
        2.Cooling Capacity Ratio Modifier Function of Low Temperature Curve \n
        3.Cooling Capacity Ratio Modifier Function of High Temperature Curve \n
        4.Cooling Energy Input Ratio Boundary Curve \n
        5.Cooling Energy Input Ratio Modifier Function of Low Temperature Curve \n
        6.Cooling Energy Input Ratio Modifier Function of High Temperature Curve \n
        7.Cooling Energy Input Ratio Modifier Function of Low Part-Load Ratio Curve \n
        8.Cooling Energy Input Ratio Modifier Function of High Part-Load Ratio Curve \n
        9.Cooling Combination Ratio Correction Factor Curve \n
        10.Cooling Part-Load Fraction Correlation Curve \n
        11.Heating Capacity Ratio Boundary Curve \n
        12.Heating Capacity Ratio Modifier Function of Low Temperature Curve \n
        13.Heating Capacity Ratio Modifier Function of High Temperature Curve \n
        14.Heating Energy Input Ratio Boundary Curve \n
        15.Heating Energy Input Ratio Modifier Function of Low Temperature Curve \n
        16.Heating Energy Input Ratio Modifier Function of High Temperature Curve \n
        17.Heating Energy Input Ratio Modifier Function of Low Part-Load Ratio Curve \n
        18.Heating Energy Input Ratio Modifier Function of High Part-Load Ratio Curve \n
        19.Heating Combination Ratio Correction Factor Curve \n
        20.Heating Part-Load Fraction Correlation Curve \n
        21.Piping Correction Factor for Length in Cooling Mode Curve \n
        22.Piping Correction Factor for Length in Heating Mode Curve \n
        23.Heat Recovery Cooling Capacity Modifier Curve \n
        24.Heat Recovery Cooling Energy Modifier Curve \n
        25.Heat Recovery Heating Capacity Modifier Curve \n
        26.Heat Recovery Heating Energy Modifier Curve
        """

        curves = {}

        name = '' if name is None else name

        # Cooling
        # ******************************************************************************
        # Cooling Capacity Ratio Boundary Curve
        curves["Cooling_Capacity_Ratio_Boundary_Curve_Name"] = \
            PerformanceCurve.cubic(idf, 140.9991, -18.7871, 1.1756, -0.02507, 13.89, 23.89,
                                   input_unit_type="Temperature", output_unit_type="Temperature",
                                   name=f"{name} CapRatioBoundary_Cooling")

        # Cooling Capacity Ratio Modifier Function of Low Temperature Curve
        curves["Cooling_Capacity_Ratio_Modifier_Function_of_Low_Temperature_Curve_Name"] = \
            PerformanceCurve.biquadratic(idf, -0.0901953919, 0.0505070990, 0.0003088882, 0.0031865985, -0.0000130163,
                                         -0.0001563836,
                                         13.89, 23.89, 10, 39.44,
                                         input_unit_type_x="Temperature", input_unit_type_y="Temperature",
                                         name=f"{name} CapRatioLowTempCurve_Cooling")

        # Cooling Capacity Ratio Modifier Function of High Temperature Curve
        curves["Cooling_Capacity_Ratio_Modifier_Function_of_High_Temperature_Curve_Name"] = \
            PerformanceCurve.biquadratic(idf, -3.2081703349, 0.2302688916, -0.0026585963, 0.0960582706, -0.0008516839,
                                         -0.0022864878,
                                         13.89, 23.89, 21.11, 47.78,
                                         input_unit_type_x="Temperature", input_unit_type_y="Temperature",
                                         name=f"{name} CapRatioHighTempCurve_Cooling")

        # Cooling Energy Input Ratio Boundary Curve
        curves["Cooling_Energy_Input_Ratio_Boundary_Curve_Name"] = \
            PerformanceCurve.cubic(idf, 140.9991, -18.7871, 1.1756, -0.02507, 13.89, 23.89,
                                   input_unit_type="Temperature", output_unit_type="Temperature",
                                   name=f"{name} EIRRatioBoundary_Cooling")

        # Cooling Energy Input Ratio Modifier Function of Low Temperature Curve
        curves["Cooling_Energy_Input_Ratio_Modifier_Function_of_Low_Temperature_Curve_Name"] = \
            PerformanceCurve.biquadratic(idf, 0.6888245196, -0.0172281621, 0.0005241366, 0.0009858312, 0.0005792064,
                                         -0.0004213067,
                                         13.89, 23.89, 10, 39.44,
                                         input_unit_type_x="Temperature", input_unit_type_y="Temperature",
                                         name=f"{name} EIRRatioLowTempCurve_Cooling")

        # Cooling Energy Input Ratio Modifier Function of High Temperature Curve
        curves["Cooling_Energy_Input_Ratio_Modifier_Function_of_High_Temperature_Curve_Name"] = \
            PerformanceCurve.biquadratic(idf, 0.4404769569, -0.0439185866, 0.0018265019, 0.0293315774, 0.0003795638,
                                         -0.0011518238,
                                         13.89, 23.89, 21.11, 47.78,
                                         input_unit_type_x="Temperature", input_unit_type_y="Temperature",
                                         name=f"{name} EIRRatioHighTempCurve_Cooling")

        # Cooling Energy Input Ratio Modifier Function of Low Part-Load Ratio Curve
        curves["Cooling_Energy_Input_Ratio_Modifier_Function_of_Low_PartLoad_Ratio_Curve_Name"] = \
            PerformanceCurve.cubic(idf, -1.246792429, 5.155371753, -6.128396226, 3.217813168, 0.15, 1.0,
                                   name=f"{name} EIRRatioLowPLR_Cooling")

        # Cooling Energy Input Ratio Modifier Function of High Part-Load Ratio Curve
        curves["Cooling_Energy_Input_Ratio_Modifier_Function_of_High_PartLoad_Ratio_Curve_Name"] = \
            PerformanceCurve.cubic(idf, -30.6717767898, 86.1535796412, -78.5620113444, 24.0802084930, 1.0,
                                   1.152777778,
                                   name=f"{name} EIRRatioHighPLR_Cooling")

        # Cooling Combination Ratio Correction Factor Curve
        curves["Cooling_Combination_Ratio_Correction_Factor_Curve_Name"] = \
            PerformanceCurve.cubic(idf, -30.6717767898, 86.1535796412, -78.5620113444, 24.0802084930, 1.0,
                                   1.152777778,
                                   name=f"{name} CombinationRatio_Cooling")

        # Cooling Part-Load Fraction Correlation Curve
        curves["Cooling_PartLoad_Fraction_Correlation_Curve_Name"] = \
            PerformanceCurve.linear(idf, 0.85, 0.15, 0, 1, name=f"{name} PLRFractionCorrelation_Cooling")

        # Heating
        # ******************************************************************************
        # Heating Capacity Ratio Boundary Curve
        curves["Heating_Capacity_Ratio_Boundary_Curve_Name"] = \
            PerformanceCurve.cubic(idf, 203.8006305, -26.23815416, 1.097486087, -0.0152378, 16.11, 23.89,
                                   input_unit_type="Temperature", output_unit_type="Temperature",
                                   name=f"{name} CapRatioBoundary_Heating")

        # Heating Capacity Ratio Modifier Function of Low Temperature Curve
        curves["Heating_Capacity_Ratio_Modifier_Function_of_Low_Temperature_Curve_Name"] = \
            PerformanceCurve.biquadratic(idf, 1.0475954826, 0.0299030501, -0.0014437977, 0.0224657841, -0.0005924488,
                                         -0.0008933140,
                                         16.11, 23.89, -20, 2.2,
                                         input_unit_type_x="Temperature", input_unit_type_y="Temperature",
                                         name=f"{name} CapRatioLowTempCurve_Heating")

        # Heating Capacity Ratio Modifier Function of High Temperature Curve
        curves["Heating_Capacity_Ratio_Modifier_Function_of_High_Temperature_Curve_Name"] = \
            PerformanceCurve.biquadratic(idf, 1.2761141679, 0.0105535358, -0.0011110665, 0.0003551723, -0.0000182544,
                                         -0.0000038670,
                                         16.11, 23.89, -4.4, 13.33,
                                         input_unit_type_x="Temperature", input_unit_type_y="Temperature",
                                         name=f"{name} CapRatioHighTempCurve_Heating")

        # Heating Energy Input Ratio Boundary Curve
        curves["Heating_Energy_Input_Ratio_Boundary_Curve_Name"] = \
            PerformanceCurve.cubic(idf, 429.0791605507, -61.4939116463, 2.9055009778, -0.0455092410, 16.11, 23.89,
                                   input_unit_type="Temperature", output_unit_type="Temperature",
                                   name=f"{name} EIRRatioBoundary_Heating")

        # Heating Energy Input Ratio Modifier Function of Low Temperature Curve
        curves["Heating_Energy_Input_Ratio_Modifier_Function_of_Low_Temperature_Curve_Name"] = \
            PerformanceCurve.biquadratic(idf, 1.7317223341, -0.0994807311, 0.0032543423, -0.0232819641, 0.0004068197,
                                         -0.0010269258,
                                         16.11, 23.89, -20, 2.22,
                                         input_unit_type_x="Temperature", input_unit_type_y="Temperature",
                                         name=f"{name} EIRRatioLowTempCurve_Heating")

        # Heating Energy Input Ratio Modifier Function of High Temperature Curve
        curves["Heating_Energy_Input_Ratio_Modifier_Function_of_High_Temperature_Curve_Name"] = \
            PerformanceCurve.biquadratic(idf, 1.8630353188, -0.1084122085, 0.0034798649, -0.0061726628, -0.0002882955,
                                         -0.0005421480,
                                         16.11, 23.89, -4.44, 13.33,
                                         input_unit_type_x="Temperature", input_unit_type_y="Temperature",
                                         name=f"{name} EIRRatioHighTempCurve_Heating")

        # Heating Energy Input Ratio Modifier Function of Low Part-Load Ratio Curve
        curves["Heating_Energy_Input_Ratio_Modifier_Function_of_Low_PartLoad_Ratio_Curve_Name"] = \
            PerformanceCurve.cubic(idf, -0.5528951749, 3.0525728816, -2.4847593777, 0.9829690708,
                                   0.15, 1.0,
                                   name=f"{name} EIRRatioLowPLR_Heating")

        # Heating Energy Input Ratio Modifier Function of High Part-Load Ratio Curve
        curves["Heating_Energy_Input_Ratio_Modifier_Function_of_High_PartLoad_Ratio_Curve_Name"] = \
            PerformanceCurve.cubic(idf, -4.3790604236, 13.0115360115, -10.5447636312, 2.9122880433,
                                   1.0, 1.212962963,
                                   name=f"{name} EIRRatioHighPLR_Heating")

        # Heating Combination Ratio Correction Factor Curve
        curves["Heating_Combination_Ratio_Correction_Factor_Curve_Name"] = \
            PerformanceCurve.cubic(idf, -15.8827160494, 42.7057613169, -36.1111111111, 10.2880658436,
                                   1.0, 1.3,
                                   name=f"{name} CombinationRatio_Heating")

        # Heating Part-Load Fraction Correlation Curve
        curves["Heating_PartLoad_Fraction_Correlation_Curve_Name"] = \
            PerformanceCurve.linear(idf, 0.85, 0.15, 0, 1, name=f"{name} PLRFractionCorrelation_Heating")

        # Piping
        # ******************************************************************************
        # Piping Correction Factor for Length in Cooling Mode Curve
        curves["Piping_Correction_Factor_for_Length_in_Cooling_Mode_Curve_Name"] = \
            PerformanceCurve.cubic(idf, 0.9989504106, -0.0007550999, 0.0000011566, -0.0000000029,
                                   7.62, 220.07, input_unit_type="Distance",
                                   name=f"{name} PipingCorrectionFactorCurve_Cooling")

        # Piping Correction Factor for Length in Heating Mode Curve
        curves["Piping_Correction_Factor_for_Length_in_Heating_Mode_Curve_Name"] = \
            PerformanceCurve.cubic(idf, 1.0022992262, -0.0004389003, 0.0000014007, -0.0000000042,
                                   7.62, 220.07, input_unit_type="Distance",
                                   name=f"{name} PipingCorrectionFactorCurve_Heating")

        # Heat Recovery
        # ******************************************************************************
        # Heat Recovery Cooling Capacity Modifier Curve
        curves["Heat_Recovery_Cooling_Capacity_Modifier_Curve_Name"] = \
            PerformanceCurve.biquadratic(idf, 0.9, 0, 0, 0, 0, 0,
                                         0, 1, 0, 1,
                                         input_unit_type_x="Dimensionless", input_unit_type_y="Dimensionless",
                                         name=f"{name} HeatRecoveryCapModifier_Cooling")
        # Heat Recovery Cooling Energy Modifier Curve
        curves["Heat_Recovery_Cooling_Energy_Modifier_Curve_Name"] = \
            PerformanceCurve.biquadratic(idf, 1.1, 0, 0, 0, 0, 0,
                                         0, 1, 0, 1,
                                         input_unit_type_x="Dimensionless", input_unit_type_y="Dimensionless",
                                         name=f"{name} HeatRecoveryEnergyModifier_Cooling")

        # Heat Recovery Heating Capacity Modifier Curve
        curves["Heat_Recovery_Heating_Capacity_Modifier_Curve_Name"] = \
            PerformanceCurve.biquadratic(idf, 0.9, 0, 0, 0, 0, 0,
                                         0, 1, 0, 1,
                                         input_unit_type_x="Dimensionless", input_unit_type_y="Dimensionless",
                                         name=f"{name} HeatRecoveryCapModifier_Heating")
        # Heat Recovery Heating Energy Modifier Curve
        curves["Heat_Recovery_Heating_Energy_Modifier_Curve_Name"] = \
            PerformanceCurve.biquadratic(idf, 1.1, 0, 0, 0, 0, 0,
                                         0, 1, 0, 1,
                                         input_unit_type_x="Dimensionless", input_unit_type_y="Dimensionless",
                                         name=f"{name} HeatRecoveryEnergyModifier_Heating")

        return curves
