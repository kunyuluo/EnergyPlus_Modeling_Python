from eppy.modeleditor import IDF
from eppy.bunch_subclass import EpBunch


def locate_change(values: list = None):
    tol = 0.00001
    start_value = values[0]
    change_index = []
    change_value = []
    for i in range(1, len(values)):
        if abs(values[i] - start_value) > tol:
            if i == 1:
                change_index.append(0)
                change_index.append(1)
                change_value.append(start_value)
                change_value.append(values[1])
                start_value = values[1]
            else:
                change_index.append(i)
                change_value.append(values[i])
                start_value = values[i]
    del change_index[0]
    change_index = [item-1 for item in change_index]
    change_index.append(23)
    return change_index, change_value


class Schedule:
    """
            -Unit_type: \n
            1.Dimensionless
            2.Temperature
            3.DeltaTemperature
            4.PrecipitationRate
            5.Angle
            6.Convection Coefficient
            7.Activity Level
            8.Velocity
            9.Capacity
            10.Power
            11.Availability
            12.Percent
            13.Control
            14.Mode
            15.MassFlowRate

            -Numeric_type: 1.Continuous 2.Discrete
    """
    @staticmethod
    def type_limits(
            idf: IDF,
            name: str = None,
            lower_limit=0,
            upper_limit=100,
            numeric_type: int = 1,
            unit_type: int = 1):
        """
        -Unit_type: \n
        1.Dimensionless
        2.Temperature
        3.DeltaTemperature
        4.PrecipitationRate
        5.Angle
        6.Convection Coefficient
        7.Activity Level
        8.Velocity
        9.Capacity
        10.Power
        11.Availability
        12.Percent
        13.Control
        14.Mode
        15.MassFlowRate

        -Numeric_type: 1.Continuous 2.Discrete
        """

        unit_types = {1: "Dimensionless", 2: "Temperature", 3: "DeltaTemperature", 4: "PrecipitationRate",
                      5: "Angle", 6: "ConvectionCoefficient", 7: "ActivityLevel", 8: "Velocity",
                      9: "Capacity", 10: "Power", 11: "Availability", 12: "Percent",
                      13: "Control", 14: "Mode", 15: "MassFlowRate"}

        numeric_types = {1: "Continuous", 2: "Discrete"}

        name = 'Schedule Type Limits' if name is None else name
        type_limit = idf.newidfobject('ScheduleTypeLimits', Name=name)
        type_limit['Lower_Limit_Value'] = lower_limit
        type_limit['Upper_Limit_Value'] = upper_limit
        type_limit['Numeric_Type'] = numeric_types[numeric_type]
        type_limit['Unit_Type'] = unit_types[unit_type]

        return type_limit

    @staticmethod
    def day(
            idf: IDF,
            name: str = None,
            numeric_type: int = None,
            unit_type: int = None,
            constant_value=None,
            hourly_value: list = None,
            interpolate_to_timestep: int = 1):
        """
        -Interpolate to timestep: 1.No 2.Average 3.Linear
        """
        interpolates = {1: "No", 2: "Average", 3: "Linear"}

        name = 'Schedule Day' if name is None else name
        day = idf.newidfobject('Schedule:Day:Interval', Name=name)

        # Type Limits:
        if numeric_type is not None and unit_type is not None:
            tl_name = f'{name} Type Limits'
            type_limits = Schedule.type_limits(idf, name=tl_name, unit_type=unit_type, numeric_type=numeric_type)
            day['Schedule_Type_Limits_Name'] = type_limits['Name']

        day['Interpolate_to_Timestep'] = interpolates[interpolate_to_timestep]

        if constant_value is not None:
            day['Time_1'] = "24:00"
            day['Value_Until_Time_1'] = constant_value
        else:
            if hourly_value is not None:
                if len(hourly_value) == 24:
                    for i in range(len(hourly_value)):
                        day[f'Time_{i + 1}'] = f"{i + 1}:00"
                        day[f'Value_Until_Time_{i + 1}'] = hourly_value[i]
                else:
                    for i in range(len(hourly_value)):
                        if i != len(hourly_value) - 1:
                            day[f'Time_{i + 1}'] = f"{i + 1}:00"
                            day[f'Value_Until_Time_{i + 1}'] = hourly_value[i]
                        else:
                            day[f'Time_{i + 1}'] = "24:00"
                            day[f'Value_Until_Time_{i + 1}'] = hourly_value[i]

        return day

    @staticmethod
    def week(
            idf: IDF,
            name: str = None,
            numeric_type: int = None,
            unit_type: int = None,
            constant_value=None,
            day_schedules: list[str | EpBunch] = None):

        name = 'Schedule Week' if name is None else name
        week = idf.newidfobject('Schedule:Week:Daily', Name=name)
        if constant_value is not None:
            day_name = f'{name} Day Schedule'
            day = Schedule.day(
                idf,
                name=day_name,
                numeric_type=numeric_type,
                unit_type=unit_type,
                constant_value=constant_value)
            week['Sunday_ScheduleDay_Name'] = day['Name']
            week['Monday_ScheduleDay_Name'] = day['Name']
            week['Tuesday_ScheduleDay_Name'] = day['Name']
            week['Wednesday_ScheduleDay_Name'] = day['Name']
            week['Thursday_ScheduleDay_Name'] = day['Name']
            week['Friday_ScheduleDay_Name'] = day['Name']
            week['Saturday_ScheduleDay_Name'] = day['Name']
            week['Holiday_ScheduleDay_Name'] = day['Name']
            week['SummerDesignDay_ScheduleDay_Name'] = day['Name']
            week['WinterDesignDay_ScheduleDay_Name'] = day['Name']
            week['CustomDay1_ScheduleDay_Name'] = day['Name']
            week['CustomDay2_ScheduleDay_Name'] = day['Name']
        else:
            if day_schedules is not None:
                if len(day_schedules) == 1:
                    week['Sunday_ScheduleDay_Name'] = day_schedules[0]['Name']
                    week['Monday_ScheduleDay_Name'] = day_schedules[0]['Name']
                    week['Tuesday_ScheduleDay_Name'] = day_schedules[0]['Name']
                    week['Wednesday_ScheduleDay_Name'] = day_schedules[0]['Name']
                    week['Thursday_ScheduleDay_Name'] = day_schedules[0]['Name']
                    week['Friday_ScheduleDay_Name'] = day_schedules[0]['Name']
                    week['Saturday_ScheduleDay_Name'] = day_schedules[0]['Name']
                    week['Holiday_ScheduleDay_Name'] = day_schedules[0]['Name']
                    week['SummerDesignDay_ScheduleDay_Name'] = day_schedules[0]['Name']
                    week['WinterDesignDay_ScheduleDay_Name'] = day_schedules[0]['Name']
                    week['CustomDay1_ScheduleDay_Name'] = day_schedules[0]['Name']
                    week['CustomDay2_ScheduleDay_Name'] = day_schedules[0]['Name']
                else:
                    pass

        return week

    @staticmethod
    def year(
            idf: IDF,
            name: str = None,
            constant_value=None,
            numeric_type: int = 1,
            unit_type: int = 1,
            weekly_schedules: list = None,
            start_months: list = None,
            start_days: list = None,
            end_months: list = None,
            end_days: list = None,
            test_mode: bool = False):
        """
        -Unit_type: \n
        1.Dimensionless
        2.Temperature
        3.DeltaTemperature
        4.PrecipitationRate
        5.Angle
        6.Convection Coefficient
        7.Activity Level
        8.Velocity
        9.Capacity
        10.Power
        11.Availability
        12.Percent
        13.Control
        14.Mode
        15.MassFlowRate

        -Numeric_type: 1.Continuous 2.Discrete
        """
        schedule_assembly = []

        name = 'Schedule Year' if name is None else name
        year = idf.newidfobject('Schedule:Year', Name=name)

        type_limits_name = f'{name} Type Limits'
        type_limits = Schedule.type_limits(idf, name=type_limits_name, unit_type=unit_type, numeric_type=numeric_type)
        schedule_assembly.append(type_limits)

        year['Schedule_Type_Limits_Name'] = type_limits_name

        if constant_value is not None:
            # Day Schedule:
            day_name = f'{name} Day Schedule'
            day = Schedule.day(
                idf,
                name=day_name,
                constant_value=constant_value)
            day['Schedule_Type_Limits_Name'] = type_limits['Name']
            schedule_assembly.append(day)

            # Week Schedule:
            week_name = f'{name} Week Schedule'
            week = Schedule.week(
                idf,
                name=week_name,
                day_schedules=[day])
            schedule_assembly.append(week)

            year['ScheduleWeek_Name_1'] = week.Name
            year['Start_Month_1'] = 1
            year['Start_Day_1'] = 1
            year['End_Month_1'] = 12
            year['End_Day_1'] = 31
            schedule_assembly.append(year)
        else:
            if weekly_schedules is not None:
                for i, week in enumerate(weekly_schedules):
                    year[f'ScheduleWeek_Name_{i+1}'] = week['Name']
                    year[f'Start_Month_{i+1}'] = start_months[i]
                    year[f'Start_Day_{i+1}'] = start_days[i]
                    year[f'End_Month_{i+1}'] = end_months[i]
                    year[f'End_Day_{i+1}'] = end_days[i]

        if test_mode:
            return schedule_assembly
        else:
            return year

    @staticmethod
    def compact(
            idf: IDF,
            name: str = None,
            numeric_type: int = 1,
            unit_type: int = 1,
            constant_value=None,
            daily_values: list = None,
            test_mode: bool = False):
        schedule_assembly = []

        name = 'Schedule Compact' if name is None else name
        compact = idf.newidfobject('Schedule:Compact', Name=name)

        type_limits_name = f'{name} Type Limits'
        type_limits = Schedule.type_limits(idf, name=type_limits_name, unit_type=unit_type, numeric_type=numeric_type)
        schedule_assembly.append(type_limits)

        compact['Schedule_Type_Limits_Name'] = type_limits_name

        if constant_value is not None:
            compact['Field_1'] = 'Through: 12/31'
            compact['Field_2'] = 'For: AllDays'
            compact['Field_3'] = 'Until: 24:00,' + str(constant_value)
            schedule_assembly.append(compact)
        else:
            if daily_values is not None:
                compact['Field_1'] = 'Through: 12/31'
                compact['Field_2'] = 'For: AllDays'
                # for i, value in enumerate(daily_values):
                #     compact[f'Field_{i+3}'] = f'Until: {i+1}:00,' + str(daily_values[i])
                changepoints = locate_change(daily_values)
                change_index = changepoints[0]
                change_value = changepoints[1]
                for i in range(len(change_index)):
                    compact[f'Field_{i+3}'] = f'Until: {change_index[i]+1}:00,' + str(change_value[i])

                schedule_assembly.append(compact)

        if test_mode:
            return schedule_assembly
        else:
            return compact

    @staticmethod
    def constant(idf: IDF, name: str, constant_value: int | float = 1):
        name = 'Schedule Constant' if name is None else name
        constant = idf.newidfobject('Schedule:Constant', Name=name)
        constant['Hourly_Value'] = constant_value
        return constant

    @staticmethod
    def always_on(idf: IDF, name: str = None):
        name = 'Schedule Compact' if name is None else name
        compact = idf.newidfobject('Schedule:Compact', Name=name)
        compact['Schedule_Type_Limits_Name'] = 'On/Off'
        compact['Field_1'] = 'Through: 12/31'
        compact['Field_2'] = 'For: AllDays'
        compact['Field_3'] = 'Until: 24:00,1'

        return compact


