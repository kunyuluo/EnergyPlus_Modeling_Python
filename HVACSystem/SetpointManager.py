from eppy.modeleditor import IDF
from eppy.bunch_subclass import EpBunch


class SetpointManager:
    @staticmethod
    def scheduled(
            idf: IDF,
            control_variable: int = 1,
            schedule: str | EpBunch = None,
            node: str | EpBunch = None,
            name: str = None):
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

        name = 'Setpoint Manager Scheduled' if name is None else name
        spt = idf.newidfobject("SetpointManager:Scheduled".upper(), Name=name)
        spt.Control_Variable = variables[control_variable]

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

        # comp = {'object': spt, 'type': 'SetpointManager:Scheduled'}

        return spt
