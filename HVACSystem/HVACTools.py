from eppy.modeleditor import IDF
from HVACSystem.PlantLoopComponents import PlantLoopComponent
from HVACSystem.SetpointManager import SetpointManager
from eppy.bunch_subclass import EpBunch


class SomeFields(object):
    """Some fields"""

    c_fields = [
        "Condenser Side Inlet Node Name",
        "Condenser Side Outlet Node Name",
        "Condenser Side Branch List Name",
        "Condenser Side Connector List Name",
        "Demand Side Inlet Node Name",
        "Demand Side Outlet Node Name",
        "Condenser Demand Side Branch List Name",
        "Condenser Demand Side Connector List Name",
    ]
    p_fields = [
        "Plant Side Inlet Node Name",
        "Plant Side Outlet Node Name",
        "Plant Side Branch List Name",
        "Plant Side Connector List Name",
        "Demand Side Inlet Node Name",
        "Demand Side Outlet Node Name",
        "Demand Side Branch List Name",
        "Demand Side Connector List Name",
    ]
    a_fields = [
        "Branch List Name",
        "Connector List Name",
        "Supply Side Inlet Node Name",
        "Demand Side Outlet Node Name",
        "Demand Side Inlet Node Names",
        "Supply Side Outlet Node Names",
    ]


class PlantLoop:
    @staticmethod
    def chilled_water_loop(
            idf: IDF,
            loop_exit_temp=None,
            loop_temp_diff=None,
            secondary_pump_sys: bool = False,
            supply_inlet_branches: dict | list[dict] = None,
            supply_branches: list[list[dict]] | list[dict] = None,
            demand_inlet_branches: dict | list[dict] = None,
            demand_branches: dict | list[dict] = None):
        pass

    @staticmethod
    def chiller_plant(idf: IDF):
        pass
