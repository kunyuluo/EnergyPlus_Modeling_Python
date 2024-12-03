from eppy.modeleditor import IDF
from eppy.bunch_subclass import EpBunch


class ZoneRadiativeUnit:
    @staticmethod
    def baseboard_convective_water(
            idf: IDF,
            name: str = None,
            available_schedule: EpBunch | str = None,
            heating_capacity_method: int = 1,
            heating_design_capacity='AutoSize',
            heating_design_capacity_per_floor_area=None,
            fraction_of_autosized_capacity=None,
            u_factor_times_area_value='AutoSize',
            max_water_flow_rate='AutoSize',
            convergence_tol=0.001):
        """
        Heating Capacity Methods: 1.HeatingDesignCapacity, 2.CapacityPerFloorArea, 3.FractionOfAutosizedHeatingCapacity
        """
        capacity_methods = {1: 'HeatingDesignCapacity', 2: 'CapacityPerFloorArea',
                            3: 'FractionOfAutosizedHeatingCapacity'}

        name = 'Baseboard Convective Water' if name is None else name
        equip = idf.newidfobject('ZoneHVAC:Baseboard:Convective:Water', Name=name)

        if available_schedule is None:
            equip['Availability_Schedule_Name'] = 'Always On Discrete hvac_library'
        else:
            if isinstance(available_schedule, EpBunch):
                equip['Availability_Schedule_Name'] = available_schedule.Name
            elif isinstance(available_schedule, str):
                equip['Availability_Schedule_Name'] = available_schedule
            else:
                raise TypeError('Invalid type of schedule.')

        equip['Heating_Design_Capacity_Method'] = capacity_methods[heating_capacity_method]
        equip['Heating_Design_Capacity'] = heating_design_capacity
        if heating_design_capacity_per_floor_area is not None:
            equip['Heating_Design_Capacity_Per_Floor_Area'] = heating_design_capacity_per_floor_area
        if fraction_of_autosized_capacity is not None:
            equip['Fraction_of_Autosized_Heating_Design_Capacity'] = fraction_of_autosized_capacity
        equip['U_Factor_Times_Area_Value'] = u_factor_times_area_value
        equip['Maximum_Water_Flow_Rate'] = max_water_flow_rate
        equip['Convergence_Tolerance'] = convergence_tol

        equip['Inlet_Node_Name'] = f'{name}_water_inlet'
        equip['Outlet_Node_Name'] = f'{name}_water_outlet'

        virtual_htg_coil = {
            'object': equip,
            'type': 'ZoneHVAC:Baseboard:Convective:Water',
            'water_inlet_field': 'Inlet_Node_Name',
            'water_outlet_field': 'Outlet_Node_Name',
        }

        comp = {
            'object': equip,
            'type': 'ZoneHVAC:Baseboard:Convective:Water',
            'heating_coil': virtual_htg_coil,
            'water_inlet_field': 'Inlet_Node_Name',
            'water_outlet_field': 'Outlet_Node_Name',
        }
        return comp

    @staticmethod
    def baseboard_convective_electric(
            idf: IDF,
            name: str = None,
            available_schedule: EpBunch | str = None,
            heating_capacity_method: int = 1,
            heating_design_capacity='AutoSize',
            heating_design_capacity_per_floor_area=None,
            fraction_of_autosized_capacity=None,
            efficiency=1.0):
        """
        Heating Capacity Methods: 1.HeatingDesignCapacity, 2.CapacityPerFloorArea, 3.FractionOfAutosizedHeatingCapacity
        """
        capacity_methods = {1: 'HeatingDesignCapacity', 2: 'CapacityPerFloorArea',
                            3: 'FractionOfAutosizedHeatingCapacity'}

        name = 'Baseboard Convective Electric' if name is None else name
        equip = idf.newidfobject('ZoneHVAC:Baseboard:Convective:Electric', Name=name)

        if available_schedule is None:
            equip['Availability_Schedule_Name'] = 'Always On Discrete hvac_library'
        else:
            if isinstance(available_schedule, EpBunch):
                equip['Availability_Schedule_Name'] = available_schedule.Name
            elif isinstance(available_schedule, str):
                equip['Availability_Schedule_Name'] = available_schedule
            else:
                raise TypeError('Invalid type of schedule.')

        equip['Heating_Design_Capacity_Method'] = capacity_methods[heating_capacity_method]
        equip['Heating_Design_Capacity'] = heating_design_capacity
        if heating_design_capacity_per_floor_area is not None:
            equip['Heating_Design_Capacity_Per_Floor_Area'] = heating_design_capacity_per_floor_area
        if fraction_of_autosized_capacity is not None:
            equip['Fraction_of_Autosized_Heating_Design_Capacity'] = fraction_of_autosized_capacity
        equip['Efficiency'] = efficiency

        comp = {
            'object': equip,
            'type': 'ZoneHVAC:Baseboard:Convective:Electric',
        }

        return comp

