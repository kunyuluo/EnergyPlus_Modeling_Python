from eppy.modeleditor import IDF
from eppy.bunch_subclass import EpBunch


class Controller:
    @staticmethod
    def controller_watercoil(
            idf: IDF,
            name: str = None,
            control_variable: int = 1,
            action: int = 1,
            convergence_tolerance=None,
            max_actuated_flow=None,
            min_actuated_flow=None):
        """
        -Control_variable: \n
        1.Temperature \n
        2.HumidityRatio \n
        3.TemperatureAndHumidityRatio \n

        -Action: 1.Normal 2.Reverse
        """

        control_variables = {1: "Temperature", 2: "HumidityRatio", 3: "TemperatureAndHumidityRatio"}
        actions = {1: "Normal", 2: "Reverse"}

        name = 'Controller Water Coil' if name is None else name
        controller = idf.newidfobject('Controller:WaterCoil', Name=name)

        controller['Control_Variable'] = control_variables[control_variable]
        controller['Action'] = actions[action]
        controller['Actuator_Variable'] = 'Flow'

        if convergence_tolerance is not None:
            controller['Controller_Convergence_Tolerance'] = convergence_tolerance
        if max_actuated_flow is not None:
            controller['Maximum_Actuated_Flow'] = max_actuated_flow
        if min_actuated_flow is not None:
            controller['Minimum_Actuated_Flow'] = min_actuated_flow

        return controller

    @staticmethod
    def controller_outdoor_air(
            idf: IDF,
            name: str = None,
            min_outdoor_air_flow_rate=0,
            max_outdoor_air_flow_rate='Autosize',
            economizer_control_type: int = 0,
            economizer_control_action_type: int = 0,
            max_limit_dry_bulb_temp=28,
            max_limit_enthalpy=64000,
            max_limit_dewpoint_temp=None,
            min_limit_dry_bulb_temp=-100,
            electronic_enthalpy_limit_curve: EpBunch | str = None,
            lockout_type: int = 0,
            min_limit_type: int = 1,
            min_outdoor_air_schedule: EpBunch | str = None,
            min_fraction_outdoor_air_schedule: EpBunch | str = None,
            max_fraction_outdoor_air_schedule: EpBunch | str = None,
            time_of_day_economizer_control_schedule: EpBunch | str = None,
            high_humidity_control: bool = False,
            humidistat_control_zone=None,
            high_humidity_outdoor_air_flow_ratio=None,
            control_high_indoor_humidity: bool = True,
            heat_recovery_bypass_control_type: int = 1):
        """
        -Economizer Control Type: \n
        0.NoEconomizer \n
        1.FixedDryBulb \n
        2.FixedDewPointAndDryBulb \n
        3.FixedEnthalpy \n
        4.DifferentialDryBulb \n
        5.DifferentialEnthalpy \n
        6.DifferentialDryBulbAndEnthalpy \n
        7.ElectronicEnthalpy \n

        -Economizer Control Action Type: \n
        1.ModulateFlow \n
        2.MinimumFlowWithBypass \n

        -Lockout Type: \n
        0.NoLockout \n
        1.LockoutWithHeating \n
        2.LockoutWithCompressor \n

        -Minimum Limit Type: \n
        1.FixedMinimum \n
        2.ProportionalMinimum \n

        -Heat_Recovery_Bypass_Control_Type: \n
        1.BypassWhenWithinEconomizerLimits \n
        2.BypassWhenOAFlowGreaterThanMinimum
        """

        economizer_types = {0: "NoEconomizer", 1: "FixedDryBulb", 2: "FixedDewPointAndDryBulb", 3: "FixedEnthalpy",
                            4: "DifferentialDryBulb", 5: "DifferentialEnthalpy",
                            6: "DifferentialDryBulbAndEnthalpy", 7: "ElectronicEnthalpy"}
        economizer_action_types = {0: "ModulateFlow", 1: "MinimumFlowWithBypass"}
        lockout_types = {0: 'NoLockout', 1: 'LockoutWithHeating', 2: 'LockoutWithCompressor'}
        min_limit_types = {1: 'FixedMinimum', 2: 'ProportionalMinimum'}
        bypass_control_types = {1: 'BypassWhenWithinEconomizerLimits', 2: 'BypassWhenOAFlowGreaterThanMinimum'}

        name = 'Controller Outdoor Air' if name is None else name
        controller = idf.newidfobject('Controller:OutdoorAir', Name=name)

        controller['Minimum_Outdoor_Air_Flow_Rate'] = min_outdoor_air_flow_rate
        controller['Maximum_Outdoor_Air_Flow_Rate'] = max_outdoor_air_flow_rate

        controller['Economizer_Control_Type'] = economizer_types[economizer_control_type]
        controller['Economizer_Control_Action_Type'] = economizer_action_types[economizer_control_action_type]
        controller['Lockout_Type'] = lockout_types[lockout_type]
        controller['Minimum_Limit_Type'] = min_limit_types[min_limit_type]

        if max_limit_dry_bulb_temp is not None:
            controller['Economizer_Maximum_Limit_DryBulb_Temperature'] = max_limit_dry_bulb_temp
        if max_limit_enthalpy is not None:
            controller['Economizer_Maximum_Limit_Enthalpy'] = max_limit_enthalpy
        if max_limit_dewpoint_temp is not None:
            controller['Economizer_Maximum_Limit_Dewpoint_Temperature'] = max_limit_dewpoint_temp
        if min_limit_dry_bulb_temp is not None:
            controller['Economizer_Minimum_Limit_DryBulb_Temperature'] = min_limit_dry_bulb_temp

        if electronic_enthalpy_limit_curve is not None:
            if isinstance(electronic_enthalpy_limit_curve, EpBunch):
                controller['Electronic_Enthalpy_Limit_Curve_Name'] = electronic_enthalpy_limit_curve.Name
            elif isinstance(electronic_enthalpy_limit_curve, str):
                controller['Electronic_Enthalpy_Limit_Curve_Name'] = electronic_enthalpy_limit_curve
            else:
                raise TypeError('Electronic Enthalpy Limit Curve must be EpBunch or str')
        if min_outdoor_air_schedule is not None:
            if isinstance(min_outdoor_air_schedule, EpBunch):
                controller['Minimum_Outdoor_Air_Schedule_Name'] = min_outdoor_air_schedule.Name
            elif isinstance(min_outdoor_air_schedule, str):
                controller['Minimum_Outdoor_Air_Schedule_Name'] = min_outdoor_air_schedule
            else:
                raise TypeError('Minimum Outdoor Air Schedule must be EpBunch or str')
        if min_fraction_outdoor_air_schedule is not None:
            if isinstance(min_fraction_outdoor_air_schedule, EpBunch):
                controller['Minimum_Fraction_of_Outdoor_Air_Schedule_Name'] = min_fraction_outdoor_air_schedule.Name
            elif isinstance(min_fraction_outdoor_air_schedule, str):
                controller['Minimum_Fraction_of_Outdoor_Air_Schedule_Name'] = min_fraction_outdoor_air_schedule
            else:
                raise TypeError('Minimum_Fraction_of_Outdoor_Air_Schedule_Name must be EpBunch or str')
        if max_fraction_outdoor_air_schedule is not None:
            if isinstance(max_fraction_outdoor_air_schedule, EpBunch):
                controller['Maximum_Fraction_of_Outdoor_Air_Schedule_Name'] = max_fraction_outdoor_air_schedule.Name
            elif isinstance(max_fraction_outdoor_air_schedule, str):
                controller['Maximum_Fraction_of_Outdoor_Air_Schedule_Name'] = max_fraction_outdoor_air_schedule
            else:
                raise TypeError('Maximum_Fraction_of_Outdoor_Air_Schedule_Name must be EpBunch or str')
        if time_of_day_economizer_control_schedule is not None:
            if isinstance(time_of_day_economizer_control_schedule, EpBunch):
                controller['Time_of_Day_Economizer_Control_Schedule_Name'] = time_of_day_economizer_control_schedule.Name
            elif isinstance(time_of_day_economizer_control_schedule, str):
                controller['Time_of_Day_Economizer_Control_Schedule_Name'] = time_of_day_economizer_control_schedule
            else:
                raise TypeError('Time_of_Day_Economizer_Control_Schedule_Name must be EpBunch or str')

        controller['High_Humidity_Control'] = 'Yes' if high_humidity_control else 'No'
        controller['Control_High_Indoor_Humidity_Based_on_Outdoor_Humidity_Ratio'] = 'Yes' if control_high_indoor_humidity else 'No'

        if humidistat_control_zone is not None:
            controller['Humidistat_Control_Zone_Name'] = humidistat_control_zone
        if high_humidity_outdoor_air_flow_ratio is not None:
            controller['High_Humidity_Outdoor_Air_Flow_Ratio'] = high_humidity_outdoor_air_flow_ratio

        controller['Heat_Recovery_Bypass_Control_Type'] = bypass_control_types[heat_recovery_bypass_control_type]

        return controller
