import copy
import math
from eppy.modeleditor import IDF
from eppy.bunch_subclass import EpBunch
from Obj_Structure import Obj_Tree
from Schedules.Schedules import Schedule


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


def delete_hvac_objs(
        idf_model: IDF,
        delete_keys: str | list = None,
        keep_shw: bool = False,
        keep_refrigeration: bool = False):
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
                       'Water_Heaters_and_Thermal_Storage', 'Water_Use',
                       'Refrigeration',
                       'Condenser_Equipment', 'Air_Distribution', 'Airflow_Network',
                       'Zone_Equipment', 'Air_Terminals', 'Air_Path', 'Zone_Units', 'VRF_Equipments', 'Radiative_Units',
                       'Pumps', 'Coils', 'Fans', 'Humidifiers_Dehumidifiers', 'Unitary',
                       'Availability_Managers', 'Setpoint_Managers',
                       'Controllers', 'Heat_Recovery', 'Performance_Curves', 'Performance_Tables', 'System_Sizing',
                       'Outputs']
        if keep_shw:
            delete_keys.remove('Water_Heaters_and_Thermal_Storage')
            delete_keys.remove('Water_Use')
        if keep_refrigeration:
            delete_keys.remove('Refrigeration')

    keep_keys_water = ['SHW', 'SWH', 'DHW']
    hospital_shw_keys = ['Water Heater', 'Heat Recovery', 'Lp2LpChlr', 'TowerWaterSys', 'CoolSys1']
    keep_keys_refrig = ['Rack', 'Case', 'Freezer', 'Kitchen']
    keep_keys = []
    if keep_shw:
        keep_keys.extend(keep_keys_water)
        keep_keys.extend(hospital_shw_keys)
    if keep_refrigeration:
        keep_keys.extend(keep_keys_refrig)

    name_field_options = ['Name', 'Zone_Name', 'Zone_or_ZoneList_Name', 'AirLoop_Name', 'Plant_or_Condenser_Loop_Name']

    for key in delete_keys:
        obj_names = Obj_Tree[key]
        for name in obj_names:
            try:
                all_targets = all_objs[name.upper()]
                pop_items = []
                pop_names = []
                if len(all_targets) > 0:
                    for target in all_targets:
                        if len(keep_keys) > 0:
                            # Get name attribute of the target object:
                            name_field = 'Name'
                            for field in name_field_options:
                                if field in target.fieldnames:
                                    name_field = field
                                    break
                            obj_name = target[name_field]

                            check = 0
                            for keyword in keep_keys:
                                if keyword.upper() not in obj_name.upper():
                                    check += 1  # if all keywords are not in the object name, then delete it

                            if check == len(keep_keys):
                                if obj_name not in pop_names:
                                    pop_items.append(target)
                                    pop_names.append(obj_name)
                        else:
                            pop_items.append(target)

                    for item in pop_items:
                        all_targets.remove(item)
            except Exception as e:
                pass


def delete_ems_object(idf_model: IDF):
    """
    Delete EMS objects related to hvac systems from a given idf file.
    """
    keywords = ['AHU', 'Boiler', 'Chiller', 'Tower', 'VAV', 'Curve', 'Pump', 'CHWR', 'HX', 'HotWaterDemand']
    all_objs = idf_model.idfobjects

    obj_names = Obj_Tree['EMS']
    for name in obj_names:
        try:
            all_targets = all_objs[name.upper()]
            # print(all_targets)
            pop_items = []
            pop_names = []
            if len(all_targets) > 0:
                for target in all_targets:
                    obj_name = target['Name']
                    for keyword in keywords:
                        if keyword.upper() in obj_name.upper():
                            if obj_name not in pop_names:
                                pop_names.append(obj_name)
                                pop_items.append(target)
                for item in pop_items:
                    all_targets.remove(item)
        except Exception as e:
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


def get_all_targets(idf: IDF, key: str, field: str = 'Name'):
    all_objs = idf.idfobjects
    target_objs = all_objs[key.upper()]

    target_fields = []
    for obj in target_objs:
        target_field = obj[field]
        # name = zone.Name.split(' ')[0]
        target_fields.append(target_field)

    target = {
        'object': target_objs,
        'field': target_fields
    }
    return target


def find_dsoa_by_zone(idf: IDF, zone_name: str):
    zone_names = get_all_targets(idf, 'Zone', 'Name')
    dsoa_names = get_all_targets(idf, 'DesignSpecification:OutdoorAir', 'Name')

    target_dsoa = None
    if zone_name in zone_names:
        for dsoa in dsoa_names:
            if zone_name in dsoa:
                target_dsoa = dsoa
                break
    else:
        raise ValueError(f"{zone_name} is not in the zone list")

    return target_dsoa


def find_always_on(idf: IDF):
    all_constant = get_all_targets(idf, key='Schedule:Constant')
    all_compact = get_all_targets(idf, key='Schedule:Compact')
    all_year = get_all_targets(idf, key='Schedule:Year')

    all_fields = all_constant['field'] + all_compact['field'] + all_year['field']
    all_objs = []
    if len(all_constant['object']) != 0:
        for item in all_constant['object']:
            all_objs.append(item)
    if len(all_compact['object']) != 0:
        for item in all_compact['object']:
            all_objs.append(item)
    if len(all_year['object']) != 0:
        for item in all_year['object']:
            all_objs.append(item)

    target_schedule = []
    for i, field in enumerate(all_fields):
        if 'ALWAYS' in field.upper() and 'ON' in field.upper():
            target_schedule.append(all_objs[i])

    return target_schedule


def set_always_on(
        idf: IDF,
        new_name: str = 'Always On Discrete',
        new_name_hvac: str = 'Always On Discrete hvac_library',
        inplace: bool = False):
    """
    First, find if there is an existing 'always on' schedule in the model,
    if yes, rename it with the given new name,
    if no, create a new 'always on' schedule.
    """
    target_schedule = find_always_on(idf)

    if len(target_schedule) != 0:
        on_schedule = None
        on_schedule_hvac = None
        for target in target_schedule:
            name = target['Name']
            if name == new_name:
                on_schedule = target
            if name == new_name_hvac:
                on_schedule_hvac = target
        if on_schedule is None:
            on_schedule = Schedule.always_on(idf, new_name)
        else:
            print(f'\'{new_name}\' already exists')
        if on_schedule_hvac is None:
            on_schedule_hvac = Schedule.always_on(idf, new_name_hvac)
        else:
            print(f'\'{new_name_hvac}\' already exists')
    else:
        on_schedule = Schedule.always_on(idf, new_name)
        on_schedule_hvac = Schedule.always_on(idf, 'Always On Discrete hvac_library')

    if not inplace:
        return on_schedule, on_schedule_hvac


def sort_zone_by_condition(idf: IDF):
    all_zones = get_all_targets(idf, key='Zone', field='Name')
    all_sizing = get_all_targets(idf, key='Sizing:Zone', field='Zone_or_ZoneList_Name')

    conditioned_zones = {}
    unconditioned_zones = {}
    conditioned_zone_obj = []
    conditioned_zone_field = []
    unconditioned_zone_obj = []
    unconditioned_zone_field = []
    for i, zone_name in enumerate(all_zones['field']):
        zone_obj = all_zones['object'][i]
        zone_field = zone_name
        if zone_name in all_sizing['field']:
            conditioned_zone_obj.append(zone_obj)
            conditioned_zone_field.append(zone_field)
        else:
            unconditioned_zone_obj.append(zone_obj)
            unconditioned_zone_field.append(zone_field)

    conditioned_zones['object'] = conditioned_zone_obj
    conditioned_zones['field'] = conditioned_zone_field
    unconditioned_zones['object'] = unconditioned_zone_obj
    unconditioned_zones['field'] = unconditioned_zone_field

    return conditioned_zones, unconditioned_zones


def sort_zone_by_name(zones: list[str]):
    sorted_zones = {}

    category = []
    unique_index = []
    for zone in zones:
        category_index = zone.split('_')[0][0]
        category.append(category_index)
        if category_index not in unique_index:
            unique_index.append(category_index)
            sorted_zones[category_index] = [zone]
        else:
            sorted_zones[category_index].append(zone)

    return sorted_zones


class SortZoneByFloor:
    @staticmethod
    def sort_zone_by_floor_1(zones: dict[str], display_field: bool = False):
        """
        Used for: ApartmentHighRise, ApartmentMidRise
        """
        zone_objs = zones['object']
        zone_fields = zones['field']

        sorted_zones = {'G': [], 'M': [], 'T': []}
        for i, field in enumerate(zone_fields):
            floor = field.split(' ')[0].upper()
            match floor:
                case 'M':
                    sorted_zones['M'].append(zone_fields[i]) if display_field else sorted_zones['M'].append(
                        zone_objs[i])
                case 'T':
                    sorted_zones['T'].append(zone_fields[i]) if display_field else sorted_zones['T'].append(
                        zone_objs[i])
                case 'G' | _:
                    sorted_zones['G'].append(zone_fields[i]) if display_field else sorted_zones['G'].append(
                        zone_objs[i])

        return sorted_zones

    @staticmethod
    def sort_zone_by_floor_2(zones: dict[str], display_field: bool = False):
        """
        Used for: Hospital, LargeHotel, SchoolPrimary, SchoolSecondary
        """
        zone_objs = zones['object']
        zone_fields = zones['field']

        sorted_zones = {0: [], 1: [], 2: [], 3: [], 4: [], 5: [], 6: [], 7: [], 8: [], 9: [], 10: []}
        for i, field in enumerate(zone_fields):
            try:
                if field.split('_')[-2].upper() == 'FLR':
                    floor = int(field.split('_')[-1])
                    sorted_zones[floor].append(zone_fields[i]) if display_field else sorted_zones[floor].append(
                        zone_objs[i])
                else:
                    raise ValueError('Can\'t find floor info')
            except IndexError:
                if field.upper() == 'BASEMENT':
                    sorted_zones[0].append(zone_fields[i]) if display_field else sorted_zones[0].append(zone_objs[i])

        # Delete the empty list in the dict:
        empty_keys = []
        for key in sorted_zones.keys():
            if len(sorted_zones[key]) == 0:
                empty_keys.append(key)
        for key in empty_keys:
            del sorted_zones[key]

        return sorted_zones

    @staticmethod
    def sort_zone_by_floor_3(zones: dict[str], display_field: bool = False):
        """
        Used for: OfficeLarge, OfficeMedium
        """

        zone_objs = zones['object']
        zone_fields = zones['field']

        sorted_zones = {'other': [], 'bot': [], 'mid': [], 'top': []}
        for i, field in enumerate(zone_fields):
            try:
                floor = field.split('_')[1].lower()
                if floor in 'bottom':
                    floor = 'bot'
                elif floor in 'basement':
                    floor = 'other'
                else:
                    pass
            except IndexError:
                floor = 'other'
            sorted_zones[floor].append(zone_fields[i]) if display_field else sorted_zones[floor].append(zone_objs[i])

        # Delete the empty list in the dict:
        empty_keys = []
        for key in sorted_zones.keys():
            if len(sorted_zones[key]) == 0:
                empty_keys.append(key)
        for key in empty_keys:
            del sorted_zones[key]

        return sorted_zones

    @staticmethod
    def sort_zone_by_floor_4(zones: dict[str], display_field: bool = False):
        """
        Used for: OutPatientHealthCare
        """
        zone_objs = zones['object']
        zone_fields = zones['field']

        sorted_zones = {0: [], 1: [], 2: [], 3: [], 4: [], 5: [], 6: [], 7: [], 8: [], 9: [], 10: []}
        for i, field in enumerate(zone_fields):
            try:
                if field.split(' ')[0].upper() == 'FLOOR':
                    floor = int(field.split(' ')[1])
                    sorted_zones[floor].append(zone_fields[i]) if display_field else sorted_zones[floor].append(
                        zone_objs[i])
                else:
                    sorted_zones[0].append(zone_fields[i]) if display_field else sorted_zones[0].append(zone_objs[i])
            except IndexError:
                if field.upper() == 'BASEMENT':
                    sorted_zones[0].append(zone_fields[i]) if display_field else sorted_zones[0].append(zone_objs[i])

        # Delete the empty list in the dict:
        empty_keys = []
        for key in sorted_zones.keys():
            if len(sorted_zones[key]) == 0:
                empty_keys.append(key)
        for key in empty_keys:
            del sorted_zones[key]

        return sorted_zones

    @staticmethod
    def sort_zone_by_floor_5(zones: dict[str], display_field: bool = False):
        """
        Used for: HotelSmall
        """
        zone_objs = zones['object']
        zone_fields = zones['field']

        sorted_zones = {0: [], 1: [], 2: [], 3: [], 4: [], 5: [], 6: [], 7: [], 8: [], 9: [], 10: []}
        for i, field in enumerate(zone_fields):
            try:
                floor = int(field.split('Flr')[1])
            except:
                floor = int(field.split('Room')[1][0])
            sorted_zones[floor].append(zone_fields[i]) if display_field else sorted_zones[floor].append(zone_objs[i])

        # Delete the empty list in the dict:
        empty_keys = []
        for key in sorted_zones.keys():
            if len(sorted_zones[key]) == 0:
                empty_keys.append(key)
        for key in empty_keys:
            del sorted_zones[key]

        return sorted_zones

    @staticmethod
    def sort_zone_by_floor_6(zones: dict[str], display_field: bool = False):
        """
        Used for: HotelSmall, OfficeSmall, RestaurantFastFood, RestaurantSitDown, RetailStandalone, RetailStripmall, Warehouse
        """
        zone_objs = zones['object']
        zone_fields = zones['field']

        sorted_zones = {0: []}
        for i, field in enumerate(zone_fields):
            sorted_zones[0].append(zone_fields[i]) if display_field else sorted_zones[0].append(zone_objs[i])

        return sorted_zones


def assign_opaque_construction(idf: IDF, surface_type: int, construction: EpBunch):
    """
    Surface type: 1: Exterior Wall 2: Exterior Roof 3: Exterior Floor 4: Interior Wall 5: Interior Floor
    6: Interior Ceiling 7: Drop Ceiling 8: Underground Wall 9: Underground Floor
    """
    criteria = {1: ['Wall', 'Outdoors', 'SunExposed', 'WindExposed'],
                2: ['Roof', 'Outdoors', 'SunExposed', 'WindExposed'],
                3: ['Floor', 'Outdoors', 'SunExposed', 'WindExposed'],
                4: ['Wall', 'Surface', 'NoSun', 'NoWind'],
                5: ['Floor', 'Surface', 'NoSun', 'NoWind'],
                6: ['Ceiling', 'Surface', 'NoSun', 'NoWind'],
                7: ['Ceiling', 'Zone', 'NoSun', 'NoWind'],
                8: ['Wall', 'GroundFCfactorMethod', 'NoSun', 'NoWind'],
                9: ['Floor', 'GroundFCfactorMethod', 'NoSun', 'NoWind']}

    all_srfs = get_all_targets(idf, 'BuildingSurface:Detailed', 'Name')['object']

    for srf in all_srfs:
        if (srf['Surface_Type'] == criteria[surface_type][0] and
                srf['Outside_Boundary_Condition'] == criteria[surface_type][1] and
                srf['Sun_Exposure'] == criteria[surface_type][2] and
                srf['Wind_Exposure'] == criteria[surface_type][3]):
            srf['Construction_Name'] = construction.Name


def assign_fenestration_construction(idf: IDF, surface_type: int, construction: EpBunch):
    """
    Surface type: 1: Window 2: Door 3: GlassDoor 4: TubularDaylightDome 5: TubularDaylightDiffuser
    """
    criteria = {1: 'Window', 2: 'Door', 3: 'GlassDoor', 4: 'TubularDaylightDome', 5: 'TubularDaylightDiffuser'}

    all_srfs = get_all_targets(idf, 'FenestrationSurface:Detailed', 'Name')['object']

    for srf in all_srfs:
        if srf['Surface_Type'] == criteria[surface_type]:
            srf['Construction_Name'] = construction.Name


def newell_method(surface: EpBunch):
    nx, ny, nz = 0, 0, 0
    vertices = [
        [surface['Vertex_1_Xcoordinate'], surface['Vertex_1_Ycoordinate'], surface['Vertex_1_Zcoordinate']],
        [surface['Vertex_2_Xcoordinate'], surface['Vertex_2_Ycoordinate'], surface['Vertex_2_Zcoordinate']],
        [surface['Vertex_3_Xcoordinate'], surface['Vertex_3_Ycoordinate'], surface['Vertex_3_Zcoordinate']],
        [surface['Vertex_4_Xcoordinate'], surface['Vertex_4_Ycoordinate'], surface['Vertex_4_Zcoordinate']]
    ]
    for i in range(len(vertices)):
        p0 = vertices[i]
        p1 = vertices[(i + 1) % len(vertices)]

        nx += (p0[1] - p1[1]) * (p0[2] + p1[2])
        ny += (p0[2] - p1[2]) * (p0[0] + p1[0])
        nz += (p0[0] - p1[0]) * (p0[1] + p1[1])

    dim = math.sqrt(nx ** 2 + ny ** 2 + nz ** 2)
    normal = [nx / dim, ny / dim, nz / dim]

    return normal


def check_orientation(surface: EpBunch):
    angle_threshold = math.pi / 4
    orientation = "east"

    orient_vectors = {
        "east": (1, 0, 0),
        "west": (-1, 0, 0),
        "north": (0, 1, 0),
        "south": (0, -1, 0)}

    normal = newell_method(surface)
    print(normal)

    for key in orient_vectors.keys():
        dot_product = normal[0] * orient_vectors[key][0] + normal[1] * orient_vectors[key][1] + normal[2] * orient_vectors[key][2]
        angle = math.acos(dot_product)

        if angle <= angle_threshold:
            orientation = key
            break
        else:
            orientation = "other"

    return orientation


def move_point_along_vector(
        origin_pt: list | tuple,
        vector_length: list | tuple = (0.0, 0.0, 0.0),
        vector_width: list | tuple = (0.0, 0.0, 0.0),
        distance_length: float = 0.0,
        distance_width: float = 0.0):
    x_end = origin_pt[0] + vector_length[0] * distance_length + vector_width[0] * distance_width
    y_end = origin_pt[1] + vector_length[1] * distance_length + vector_width[1] * distance_width
    z_end = origin_pt[2] + vector_length[2] * distance_length + vector_width[2] * distance_width

    return x_end, y_end, z_end


def calculate_vertices(surface: EpBunch, window_ratio: float):
    if window_ratio <= 0.95:
        vertices = {}
        ratio_length = (1.0 + window_ratio) / 2.0
        ratio_width = window_ratio / ratio_length

        delta_ratio_length = (1.0 - ratio_length) / 2.0
        delta_ratio_width = (1.0 - ratio_width) / 2.0

        length_dim = math.sqrt(pow((surface['Vertex_1_Xcoordinate'] - surface['Vertex_4_Xcoordinate']), 2) +
                               pow((surface['Vertex_1_Ycoordinate'] - surface['Vertex_4_Ycoordinate']), 2) +
                               pow((surface['Vertex_1_Zcoordinate'] - surface['Vertex_4_Zcoordinate']), 2))
        width_dim = math.sqrt(pow((surface['Vertex_1_Xcoordinate'] - surface['Vertex_2_Xcoordinate']), 2) +
                              pow((surface['Vertex_1_Ycoordinate'] - surface['Vertex_2_Ycoordinate']), 2) +
                              pow((surface['Vertex_1_Zcoordinate'] - surface['Vertex_2_Zcoordinate']), 2))
        length_unit_vec = [(surface['Vertex_4_Xcoordinate'] - surface['Vertex_1_Xcoordinate']) / length_dim,
                           (surface['Vertex_4_Ycoordinate'] - surface['Vertex_1_Ycoordinate']) / length_dim,
                           (surface['Vertex_4_Zcoordinate'] - surface['Vertex_1_Zcoordinate']) / length_dim]
        width_unit_vec = [(surface['Vertex_2_Xcoordinate'] - surface['Vertex_1_Xcoordinate']) / width_dim,
                          (surface['Vertex_2_Ycoordinate'] - surface['Vertex_1_Ycoordinate']) / width_dim,
                          (surface['Vertex_2_Zcoordinate'] - surface['Vertex_1_Zcoordinate']) / width_dim]
        length_unit_vec_rev = [-length_unit_vec[0], -length_unit_vec[1], -length_unit_vec[2]]
        width_unit_vec_rev = [-width_unit_vec[0], -width_unit_vec[1], -width_unit_vec[2]]

        delta_length = length_dim * delta_ratio_length
        delta_width = width_dim * delta_ratio_width

        # vertice 1 of the window:
        v1_origin = (surface['Vertex_1_Xcoordinate'], surface['Vertex_1_Ycoordinate'], surface['Vertex_1_Zcoordinate'])
        vertice_1 = move_point_along_vector(v1_origin, length_unit_vec, width_unit_vec, delta_length, delta_width)
        vertices[1] = vertice_1

        # vertice 2 of the window:
        v2_origin = (surface['Vertex_2_Xcoordinate'], surface['Vertex_2_Ycoordinate'], surface['Vertex_2_Zcoordinate'])
        vertice_2 = move_point_along_vector(v2_origin, length_unit_vec, width_unit_vec_rev, delta_length, delta_width)
        vertices[2] = vertice_2

        # vertice 3 of the window:
        v3_origin = (surface['Vertex_3_Xcoordinate'], surface['Vertex_3_Ycoordinate'], surface['Vertex_3_Zcoordinate'])
        vertice_3 = move_point_along_vector(v3_origin, length_unit_vec_rev, width_unit_vec_rev, delta_length, delta_width)
        vertices[3] = vertice_3

        # vertice 4 of the window:
        v4_origin = (surface['Vertex_4_Xcoordinate'], surface['Vertex_4_Ycoordinate'], surface['Vertex_4_Zcoordinate'])
        vertice_4 = move_point_along_vector(v4_origin, length_unit_vec_rev, width_unit_vec, delta_length, delta_width)
        vertices[4] = vertice_4

        return vertices

    else:
        raise ValueError('The window ratio must be less than 0.95.')


def create_window_by_ratio(idf: IDF, window_ratio: float | dict, construction: EpBunch | dict):
    criteria_wall = ['Wall', 'Outdoors', 'SunExposed', 'WindExposed']

    all_srfs = get_all_targets(idf, 'BuildingSurface:Detailed', 'Name')['object']

    # Get all exterior walls:
    ###################################################################
    ext_walls = []
    for srf in all_srfs:
        if (srf['Surface_Type'] == criteria_wall[0] and
                srf['Outside_Boundary_Condition'] == criteria_wall[1] and
                srf['Sun_Exposure'] == criteria_wall[2] and
                srf['Wind_Exposure'] == criteria_wall[3] and
                'Plenum' not in srf['Name'] and
                'Plenum' not in srf['Zone_Name']):
            ext_walls.append(srf)

    # Delete the original windows:
    ###################################################################
    all_objs = idf.idfobjects
    try:
        all_windows = all_objs['FenestrationSurface:Detailed']
        pop_items = []
        if len(all_windows) > 0:
            for window in all_windows:
                pop_items.append(window)

            for item in pop_items:
                all_windows.remove(item)
    except:
        pass

    # Generate new windows based on wwr:
    ###################################################################
    windows = []
    for wall in ext_walls:
        win_srf = idf.newidfobject('FenestrationSurface:Detailed')
        win_srf['Name'] = wall['Name'] + '_Window'
        win_srf['Surface_Type'] = 'Window'
        win_srf['Building_Surface_Name'] = wall['Name']
        win_srf['View_Factor_to_Ground'] = 'AutoCalculate'
        win_srf['Multiplier'] = 1
        win_srf['Number_of_Vertices'] = 4

        orientation = 'north'
        if isinstance(window_ratio, float):
            vertices = calculate_vertices(wall, window_ratio)
        elif isinstance(window_ratio, dict):
            orientation = check_orientation(wall)
            vertices = calculate_vertices(wall, window_ratio[orientation])
        else:
            raise TypeError('The window ratio must be a float or a dict.')

        win_srf['Vertex_1_Xcoordinate'] = vertices[1][0]
        win_srf['Vertex_1_Ycoordinate'] = vertices[1][1]
        win_srf['Vertex_1_Zcoordinate'] = vertices[1][2]
        win_srf['Vertex_2_Xcoordinate'] = vertices[2][0]
        win_srf['Vertex_2_Ycoordinate'] = vertices[2][1]
        win_srf['Vertex_2_Zcoordinate'] = vertices[2][2]
        win_srf['Vertex_3_Xcoordinate'] = vertices[3][0]
        win_srf['Vertex_3_Ycoordinate'] = vertices[3][1]
        win_srf['Vertex_3_Zcoordinate'] = vertices[3][2]
        win_srf['Vertex_4_Xcoordinate'] = vertices[4][0]
        win_srf['Vertex_4_Ycoordinate'] = vertices[4][1]
        win_srf['Vertex_4_Zcoordinate'] = vertices[4][2]

        if isinstance(construction, EpBunch):
            win_srf['Construction_Name'] = construction['Name']
        elif isinstance(construction, dict):
            win_srf['Construction_Name'] = construction[orientation]
        else:
            raise TypeError('The construction must be an EpBunch or a dict.')

        windows.append(win_srf)

    return windows


