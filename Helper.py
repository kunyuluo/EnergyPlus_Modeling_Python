import copy
import math
from eppy.modeleditor import IDF
from Obj_Structure import Obj_Tree


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
        "Controller List Name",
        'Availability Manager List Name',
        "Branch List Name",
        # "Connector List Name",
        "Supply Side Inlet Node Name",
        "Demand Side Outlet Node Name",
        "Demand Side Inlet Node Names",
        "Supply Side Outlet Node Names",
    ]


class UnitConverter:
    @staticmethod
    def infiltration_calculator(
            standard_flow_rate,
            standard_pressure: int = 75,
            target_pressure: int = 4,
            input_in_ip_unit: bool = True):

        # ASHRAE 90.1 2013: 0.4 cfm/sf@75Pa
        # Passive house: 0.1 cfm/sf@75Pa
        flow_rate_at_target_pressure = standard_flow_rate * math.pow((target_pressure / standard_pressure), 0.67)
        if input_in_ip_unit:
            # convert result from cfm/sf to m3_s/m2
            result = flow_rate_at_target_pressure * 0.00047195 * 10.76
        else:
            result = flow_rate_at_target_pressure

        return result

    @staticmethod
    def pump_power_calculator_ip(head, flow, motor_efficiency=0.9, pump_efficiency=0.7):
        """
        :param head: pump head in ft
        :param flow: pump water flow rate in gpm
        :param motor_efficiency: default is 0.9
        :param pump_efficiency: default is 0.7
        :return: pump power in watts (W)
        """
        hp = head * flow * 8.33 / (33000 * motor_efficiency * pump_efficiency)
        return hp * 745.7

    @staticmethod
    def pump_power_calculator_si(head, flow, motor_efficiency=0.9, pump_efficiency=0.7, kilowatts: bool = False):
        """
        :param head: pump head in meter
        :param flow: pump water flow rate in m3/h
        :param motor_efficiency: default is 0.9
        :param pump_efficiency: default is 0.7
        :param kilowatts: set to True if kilowatts to be output. Default is False.
        :return: pump power in watts (W)
        """
        kw = head * flow * 1000 * 9.81 / (3600000 * motor_efficiency * pump_efficiency)
        if kilowatts:
            return kw
        else:
            return kw * 1000

    # Convertor:
    # *************************************************************************************
    @staticmethod
    def f_to_c(temperature):
        return (temperature - 32) / 1.8

    @staticmethod
    def c_to_f(temperature):
        return temperature * 1.8 + 32

    @staticmethod
    def delta_temp_f_to_c(delta):
        return delta / 1.8

    @staticmethod
    def delta_temp_c_to_f(delta):
        return delta * 1.8

    @staticmethod
    def m3h_to_m3s(flow):
        return flow / 3600

    @staticmethod
    def cfm_to_m3s(flow):
        return flow * 0.0004719474

    @staticmethod
    def gpm_to_m3s(flow):
        return flow * 0.0000630902

    @staticmethod
    def mh2o_to_pa(head):
        """
        Convert pump head from mH2O to Pa
        """
        return head * 9806.65

    @staticmethod
    def inh2o_to_pa(head):
        """
        Convert pump head from inH2O to Pa
        """
        return head * 248.84

    @staticmethod
    def u_ip_to_si(u_value):
        """
        Convert U-Values in IP (BTU/hft2F) to U-Values in SI (W/Km2)
        """
        return u_value * 5.678263337

    @staticmethod
    def u_si_to_ip(u_value):
        """
        Convert U-Values in SI (W/Km2) to U-Values in IP (BTU/hft2F)
        """
        return u_value / 5.678263337

    @staticmethod
    def r_ip_to_si(r_value):
        """
        Convert R-Values in IP (hft2F/BTU) to R-Values in SI (Km2/W)
        """
        return r_value / 5.678263337

    @staticmethod
    def r_si_to_ip(r_value):
        """
        Convert R-Values in SI (Km2/W) to R-Values in IP (hft2F/BTU)
        """
        return r_value * 5.678263337

    @staticmethod
    def m2ppl_to_pplm2(values):
        """
        Convert people density from m2/people to people/m2
        """
        if isinstance(values, float):
            return 1 / values
        elif isinstance(values, list):
            new_values = []
            for value in values:
                new_value = 1 / value
                new_values.append(new_value)
            return new_values
        else:
            raise TypeError("Invalid input type of values")

    @staticmethod
    def ft2ppl_to_pplm2(values):
        """
        Convert people density from ft2/people to people/m2
        """
        if isinstance(values, float):
            return 1 / values / 0.0929
        elif isinstance(values, list):
            new_values = []
            for value in values:
                new_value = 1 / value / 0.0929
                new_values.append(new_value)
            return new_values
        else:
            raise TypeError("Invalid input type of values")

    @staticmethod
    def ppl1000ft2_to_pplm2(values):
        """
        Convert people density from people/1000ft2 to people/m2
        """
        if isinstance(values, float):
            return values / 0.0929
        elif isinstance(values, list):
            new_values = []
            for value in values:
                new_value = value / 0.0929
                new_values.append(new_value)
            return new_values
        else:
            raise TypeError("Invalid input type of values")


def delete_hvac_objs(idf_model: IDF, delete_keys: str | list=None):
    """
    Delete pre-defined groups of component from a given idf file.
    """
    all_objs = idf_model.idfobjects

    if delete_keys is not None:
        if isinstance(delete_keys, str):
            delete_keys = [delete_keys]
        elif isinstance(delete_keys, list):
            delete_keys = delete_keys
        else:
            raise ValueError("delete_keys should be a string or a list of strings")
    else:
        delete_keys = ['HVAC_Branch', 'PlantLoops', 'Plant_Equipment', 'Plant_Controls',
                       'Water_Heaters_and_Thermal_Storage',
                       'Condenser_Equipment', 'Air_Distribution', 'Airflow_Network',
                       'Zone_Equipment', 'Air_Terminals', 'Air_Path', 'Zone_Units', 'VRF_Equipments', 'Radiative_Units',
                       'Pumps', 'Coils', 'Fans', 'Humidifiers_Dehumidifiers',
                       'Availability_Managers', 'Setpoint_Managers',
                       'Controllers', 'Heat_Recovery', 'Performance_Curves', 'Performance_Tables', 'System_Sizing',
                       'Outputs']
    for key in delete_keys:
        obj_names = Obj_Tree[key]
        for name in obj_names:
            try:
                all_targets = all_objs[name.upper()]
                if len(all_targets) > 0:
                    for i in range(len(all_targets)):
                        idf_model.popidfobject(name.upper(), 0)
            except Exception as e:
                # print(e)
                pass


def flattencopy(lst):
    """flatten and return a copy of the list
    indefficient on large lists"""
    # modified from
    # http://stackoverflow.com/questions/2158395/flatten-an-irregular-list-of-lists-in-python
    thelist = copy.deepcopy(lst)
    list_is_nested = True
    while list_is_nested:  # outer loop
        keepchecking = False
        atemp = []
        for element in thelist:  # inner loop
            if isinstance(element, list):
                atemp.extend(element)
                keepchecking = True
            else:
                atemp.append(element)
        list_is_nested = keepchecking  # determine if outer loop exits
        thelist = atemp[:]
    return thelist


def get_all_zones(idf: IDF):
    all_objs = idf.idfobjects
    zones = all_objs['Zone']

    zone_names = []
    for zone in zones:
        name = zone.Name
        # name = zone.Name.split(' ')[0]
        zone_names.append(name)

    return zone_names


