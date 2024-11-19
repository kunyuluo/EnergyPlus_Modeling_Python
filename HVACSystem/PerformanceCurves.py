class PerformanceCurve:
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
