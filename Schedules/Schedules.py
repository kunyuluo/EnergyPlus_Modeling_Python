from eppy.modeleditor import IDF
from eppy.bunch_subclass import EpBunch


class Schedule:
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

