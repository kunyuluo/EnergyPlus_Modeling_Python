from eppy.modeleditor import IDF
from eppy.bunch_subclass import EpBunch
from Schedules.Schedules import Schedule
from Helper import UnitConverter


class SetpointManager:
    @staticmethod
    def scheduled(
            idf: IDF,
            control_variable: int = 1,
            constant_value: float = None,
            schedule: str | EpBunch = None,
            node: str | EpBunch = None,
            name: str = None,
            test_mode: bool = False):
        """
        -Control variable:
        1.Temperature
        2.MaximumTemperature
        3.MinimumTemperature
        4.HumidityRatio
        5.MaximumHumidityRatio
        6.MinimumHumidityRatio
        7.MassFlowRate
        8.MaximumMassFlowRate
        9.MinimumMassFlowRate
        """

        variables = {1: "Temperature", 2: "MaximumTemperature", 3: "MinimumTemperature",
                     4: "HumidityRatio", 5: "MaximumHumidityRatio", 6: "MinimumHumidityRatio",
                     7: "MassFlowRate", 8: "MaximumMassFlowRate", 9: "MinimumMassFlowRate"}

        assembly = []
        name = 'Setpoint Manager Scheduled' if name is None else name
        spt = idf.newidfobject("SetpointManager:Scheduled", Name=name)
        spt.Control_Variable = variables[control_variable]

        if constant_value is not None:
            match control_variable:
                case 1 | 2 | 3:
                    numeric_type = 1
                    unit_type = 2
                case 4 | 5 | 6:
                    numeric_type = 1
                    unit_type = 1
                case 7 | 8 | 9:
                    numeric_type = 1
                    unit_type = 15
                case _:
                    numeric_type = 1
                    unit_type = 1
            schedule = Schedule.year(
                idf,
                name=name,
                constant_value=constant_value,
                numeric_type=numeric_type,
                unit_type=unit_type,
                test_mode=test_mode)
            if test_mode:
                spt.Schedule_Name = schedule[-1].Name
            else:
                spt.Schedule_Name = schedule.Name
        else:
            if schedule is not None:
                if isinstance(schedule, str):
                    spt.Schedule_Name = schedule
                elif isinstance(schedule, EpBunch):
                    spt.Schedule_Name = schedule.Name
                else:
                    raise TypeError("schedule must be a string or EpBunch")

        if node is not None:
            if isinstance(node, str):
                spt.Setpoint_Node_or_NodeList_Name = node
            elif isinstance(node, EpBunch):
                spt.Setpoint_Node_or_NodeList_Name = node.Name
            else:
                raise TypeError("node must be a string or EpBunch")

        if test_mode:
            assembly.append(spt)
            assembly.extend(schedule)
            return assembly
        else:
            return spt

    @staticmethod
    def mixed_air(
            idf: IDF,
            name: str = None):
        name = 'SPM MixedAir' if name is None else name
        spm = idf.newidfobject("SetpointManager:MixedAir", Name=name)

        return spm

    @staticmethod
    def follow_outdoor_air_temp(
            idf: IDF,
            name: str = None,
            control_variable: int = 1,
            reference_temp_type: int = 1,
            offset_temp_diff=None,
            max_setpoint_temp=None,
            min_setpoint_temp=None,
            ashrae_default: bool = False):
        """
        -Control_variable: 1:Temperature 2:MaximumTemperature 3:MinimumTemperature \n
        -Reference_temperature_type: 1:OutdoorAirWetBulb 2:OutdoorAirDryBulb
        """

        control_variables = {1: "Temperature", 2: "MaximumTemperature", 3: "MinimumTemperature"}
        reference_temp_types = {1: "OutdoorAirWetBulb", 2: "OutdoorAirDryBulb"}

        name = 'SPM Follow OAT' if name is None else name
        spm = idf.newidfobject("SetpointManager:FollowOutdoorAirTemperature", Name=name)

        spm["Control_Variable"] = control_variables[control_variable]

        if ashrae_default:
            spm["Reference_Temperature_Type"] = reference_temp_types[1]
            spm['Offset_Temperature_Difference'] = UnitConverter.delta_temp_f_to_c(5)
            spm['Maximum_Setpoint_Temperature'] = UnitConverter.f_to_c(90)
            spm['Minimum_Setpoint_Temperature'] = UnitConverter.f_to_c(70)
        else:
            spm["Reference_Temperature_Type"] = reference_temp_types[reference_temp_type]
            spm['Offset_Temperature_Difference'] = offset_temp_diff
            spm['Maximum_Setpoint_Temperature'] = max_setpoint_temp
            spm['Minimum_Setpoint_Temperature'] = min_setpoint_temp

        return spm
