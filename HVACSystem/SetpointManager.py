from eppy.modeleditor import IDF
from eppy.bunch_subclass import EpBunch
from Schedules.Schedules import Schedule


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
        spt = idf.newidfobject("SetpointManager:Scheduled".upper(), Name=name)
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
        spm = idf.newidfobject("SetpointManager:MixedAir".upper(), Name=name)

        return spm
