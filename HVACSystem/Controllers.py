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
        controller = idf.newidfobject('Controller:WaterCoil'.upper(), Name=name)

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