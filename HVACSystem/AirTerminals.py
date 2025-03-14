from eppy.modeleditor import IDF
from eppy.bunch_subclass import EpBunch
from HVACSystem.AirLoopComponents import AirLoopComponent
from configs import *


class AirTerminal:
    @staticmethod
    def air_distribution_unit(idf: IDF, name: str = None):
        name = 'Air Distribution Unit' if name is None else name
        air_distribute = idf.newidfobject('ZoneHVAC:AirDistributionUnit', Name=name)

        comp = {
            'object': air_distribute,
            'type': 'ZoneHVAC:AirDistributionUnit',
        }
        return comp

    @staticmethod
    def single_duct_constant_volume_no_reheat(
            idf: IDF,
            schedule: EpBunch | str = None,
            name: str = None,
            max_air_flow_rate='Autosize',
            design_specification_outdoor_air: EpBunch | str = None,
            per_person_ventilation_rate_mode=None):
        """
        -Per_Person_Ventilation_Rate_Mode: \n
        1.CurrentOccupancy 2.DesignOccupancy
        """
        modes = {1: 'CurrentOccupancy', 2: 'DesignOccupancy'}

        name = 'SingleDuctConstantVolumeNoReheat' if name is None else name
        terminal = idf.newidfobject('AirTerminal:SingleDuct:ConstantVolume:NoReheat'.upper(), Name=name)

        if schedule is None:
            terminal['Availability_Schedule_Name'] = schedule_always_on_hvac
        else:
            if isinstance(schedule, str):
                terminal['Availability_Schedule_Name'] = schedule
            elif isinstance(schedule, EpBunch):
                terminal['Availability_Schedule_Name'] = schedule.Name
            else:
                raise TypeError('schedule must be a string or EpBunch')

        terminal['Maximum_Air_Flow_Rate'] = max_air_flow_rate

        if design_specification_outdoor_air is not None:
            if isinstance(design_specification_outdoor_air, str):
                terminal['Design_Specification_Outdoor_Air_Object_Name'] = design_specification_outdoor_air
            elif isinstance(design_specification_outdoor_air, EpBunch):
                terminal['Design_Specification_Outdoor_Air_Object_Name'] = design_specification_outdoor_air.Name
            else:
                raise TypeError('design_specification_outdoor_air must be a string or EpBunch')

            if per_person_ventilation_rate_mode is not None:
                terminal['Per_Person_Ventilation_Rate_Mode'] = modes[per_person_ventilation_rate_mode]

        terminal['Air_Inlet_Node_Name'] = f'{name} air inlet'
        terminal['Air_Outlet_Node_Name'] = f'{name} air outlet'

        component = {
            'object': terminal,
            'type': 'AirTerminal:SingleDuct:ConstantVolume:NoReheat',
            'air_inlet_field': 'Air_Inlet_Node_Name',
            'air_outlet_field': 'Air_Outlet_Node_Name',
        }

        return component

    @staticmethod
    def single_duct_vav_no_reheat(
            idf: IDF,
            schedule: EpBunch | str = None,
            name: str = None,
            max_air_flow_rate='Autosize',
            min_air_flow_input_method: int = 1,
            constant_min_air_flow_fraction=0.3,
            fixed_min_air_flow_rate=None,
            min_air_flow_fraction_schedule: EpBunch | str = None,
            design_specification_outdoor_air: EpBunch | str = None,
            min_air_flow_turndown_schedule: EpBunch | str = None):
        """
        -Zone minimum Air Flow Input Method: \n
        1.Constant \n
        2.FixedFlowRate \n
        3.Scheduled
        """
        methods = {1: "Constant", 2: "FixedFlowRate", 3: "Scheduled"}

        name = 'SingleDuctVAVNoReheat' if name is None else name
        terminal = idf.newidfobject('AirTerminal:SingleDuct:VAV:NoReheat'.upper(), Name=name)

        if schedule is None:
            terminal['Availability_Schedule_Name'] = schedule_always_on_hvac
        else:
            if isinstance(schedule, str):
                terminal['Availability_Schedule_Name'] = schedule
            elif isinstance(schedule, EpBunch):
                terminal['Availability_Schedule_Name'] = schedule.Name
            else:
                raise TypeError('schedule must be a string or EpBunch')

        terminal['Maximum_Air_Flow_Rate'] = max_air_flow_rate
        terminal['Zone_Minimum_Air_Flow_Input_Method'] = methods[min_air_flow_input_method]
        terminal['Constant_Minimum_Air_Flow_Fraction'] = constant_min_air_flow_fraction
        if fixed_min_air_flow_rate is not None:
            terminal['Fixed_Minimum_Air_Flow_Rate'] = fixed_min_air_flow_rate

        if min_air_flow_fraction_schedule is not None:
            if isinstance(min_air_flow_fraction_schedule, str):
                terminal['Minimum_Air_Flow_Fraction_Schedule_Name'] = min_air_flow_fraction_schedule
            elif isinstance(min_air_flow_fraction_schedule, EpBunch):
                terminal['Minimum_Air_Flow_Fraction_Schedule_Name'] = min_air_flow_fraction_schedule.Name
            else:
                raise TypeError('min_air_flow_fraction_schedule must be a string or EpBunch')

        if design_specification_outdoor_air is not None:
            if isinstance(design_specification_outdoor_air, str):
                terminal['Design_Specification_Outdoor_Air_Object_Name'] = design_specification_outdoor_air
            elif isinstance(design_specification_outdoor_air, EpBunch):
                terminal['Design_Specification_Outdoor_Air_Object_Name'] = design_specification_outdoor_air.Name
            else:
                raise TypeError('design_specification_outdoor_air must be a string or EpBunch')

        if min_air_flow_turndown_schedule is not None:
            if isinstance(min_air_flow_turndown_schedule, str):
                terminal['Minimum_Air_Flow_Turndown_Schedule_Name'] = min_air_flow_turndown_schedule
            elif isinstance(min_air_flow_turndown_schedule, EpBunch):
                terminal['Minimum_Air_Flow_Turndown_Schedule_Name'] = min_air_flow_turndown_schedule.Name
            else:
                raise TypeError('min_air_flow_turndown_schedule must be a string or EpBunch')

        terminal['Air_Inlet_Node_Name'] = f'{name} air inlet'
        terminal['Air_Outlet_Node_Name'] = f'{name} air outlet'

        component = {
            'object': terminal,
            'type': 'AirTerminal:SingleDuct:VAV:NoReheat',
            'air_inlet_field': 'Air_Inlet_Node_Name',
            'air_outlet_field': 'Air_Outlet_Node_Name',
        }

        return component

    @staticmethod
    def single_duct_vav_reheat(
            idf: IDF,
            schedule: EpBunch | str = None,
            reheat_coil_type: int = 3,
            name: str = None,
            max_air_flow_rate='Autosize',
            min_air_flow_input_method: int = 1,
            constant_min_air_flow_fraction=0.3,
            fixed_min_air_flow_rate=None,
            min_air_flow_fraction_schedule: EpBunch | str = None,
            max_hot_water_flow_rate='Autosize',
            min_hot_water_flow_rate=0,
            convergence_tolerance=0.001,
            reheat_control_strategy: int = 1,
            damper_heating_action: int = 1,
            max_flow_per_area_reheat='Autosize',
            max_flow_fraction_reheat=None,
            max_reheat_air_temp=35,
            design_specification_outdoor_air: EpBunch | str = None,
            min_air_flow_turndown_schedule: EpBunch | str = None):

        """
        -Zone minimum Air Flow Input Method: \n
        1.Constant \n
        2.FixedFlowRate \n
        3.Scheduled \n

        -Reheat_coil_type:  \n
        1.Water 2.Fuel 3.Electric 4.Steam \n

        -Damper heating action: \n
        1.Normal, 2.Reverse, 3.ReverseWithLimits

        -Reheat_control_strategy:  \n
        1.SingleMaximum 2.DualMaximum
        """
        methods = {1: "Constant", 2: "FixedFlowRate", 3: "Scheduled"}
        reheat_coil_types = {1: 'Water', 2: 'Fuel', 3: 'Electric', 4: 'Steam'}
        damper_heating_actions = {1: 'Normal', 2: 'Reverse', 3: 'ReverseWithLimits'}

        name = 'SingleDuctVAVReheat' if name is None else name
        terminal = idf.newidfobject('AirTerminal:SingleDuct:VAV:Reheat'.upper(), Name=name)

        if schedule is None:
            terminal['Availability_Schedule_Name'] = schedule_always_on_hvac
        else:
            if isinstance(schedule, str):
                terminal['Availability_Schedule_Name'] = schedule
            elif isinstance(schedule, EpBunch):
                terminal['Availability_Schedule_Name'] = schedule.Name
            else:
                raise TypeError('schedule must be a string or EpBunch')

        # Create reheat coil object:
        coil_type = reheat_coil_types[reheat_coil_type]
        coil_key = f'Coil:Heating:{coil_type}'
        coil_func_name = f'heating_coil_{coil_type.lower()}'
        coil_name = f'{name} {coil_type} Reheat Coil'
        terminal['Reheat_Coil_Object_Type'] = coil_key
        terminal['Reheat_Coil_Name'] = coil_name

        # reheat_coil = idf.newidfobject(coil_key.upper(), Name=coil_name)
        func = getattr(AirLoopComponent, coil_func_name)
        try:
            reheat_coil = func(idf, name=coil_name, need_controller=False)
        except:
            reheat_coil = func(idf, name=coil_name)

        terminal['Maximum_Air_Flow_Rate'] = max_air_flow_rate
        terminal['Zone_Minimum_Air_Flow_Input_Method'] = methods[min_air_flow_input_method]
        terminal['Constant_Minimum_Air_Flow_Fraction'] = constant_min_air_flow_fraction
        if fixed_min_air_flow_rate is not None:
            terminal['Fixed_Minimum_Air_Flow_Rate'] = fixed_min_air_flow_rate
        if min_air_flow_fraction_schedule is not None:
            if isinstance(min_air_flow_fraction_schedule, str):
                terminal['Availability_Schedule_Name'] = min_air_flow_fraction_schedule
            elif isinstance(min_air_flow_fraction_schedule, EpBunch):
                terminal['Availability_Schedule_Name'] = min_air_flow_fraction_schedule.Name
            else:
                raise TypeError('min_air_flow_fraction_schedule must be a string or EpBunch')

        terminal['Maximum_Hot_Water_or_Steam_Flow_Rate'] = max_hot_water_flow_rate
        terminal['Minimum_Hot_Water_or_Steam_Flow_Rate'] = min_hot_water_flow_rate
        terminal['Convergence_Tolerance'] = convergence_tolerance

        if reheat_control_strategy == 1:
            terminal['Damper_Heating_Action'] = 'Normal'
        else:
            terminal['Damper_Heating_Action'] = damper_heating_actions[damper_heating_action]
            if damper_heating_action == 3:
                if max_flow_fraction_reheat is not None:
                    terminal['Maximum_Flow_Fraction_During_Reheat'] = max_flow_fraction_reheat
                else:
                    terminal['Maximum_Flow_Fraction_During_Reheat'] = 0.5

        terminal['Maximum_Flow_per_Zone_Floor_Area_During_Reheat'] = max_flow_per_area_reheat
        terminal['Maximum_Reheat_Air_Temperature'] = max_reheat_air_temp

        if design_specification_outdoor_air is not None:
            if isinstance(design_specification_outdoor_air, str):
                terminal['Design_Specification_Outdoor_Air_Object_Name'] = design_specification_outdoor_air
            elif isinstance(design_specification_outdoor_air, EpBunch):
                terminal['Design_Specification_Outdoor_Air_Object_Name'] = design_specification_outdoor_air.Name
            else:
                raise TypeError('design_specification_outdoor_air must be a string or EpBunch')

        if min_air_flow_turndown_schedule is not None:
            if isinstance(min_air_flow_turndown_schedule, str):
                terminal['Minimum_Air_Flow_Turndown_Schedule_Name'] = min_air_flow_turndown_schedule
            elif isinstance(min_air_flow_turndown_schedule, EpBunch):
                terminal['Minimum_Air_Flow_Turndown_Schedule_Name'] = min_air_flow_turndown_schedule.Name
            else:
                raise TypeError('min_air_flow_turndown_schedule must be a string or EpBunch')

        damper_air_out_name = f'{name} damper air outlet'
        air_in_name = f'{name} air inlet'
        air_out_name = f'{name} air outlet'
        terminal['Damper_Air_Outlet_Node_Name'] = damper_air_out_name
        terminal['Air_Inlet_Node_Name'] = air_in_name
        terminal['Air_Outlet_Node_Name'] = air_out_name

        reheat_coil['object']['Air_Inlet_Node_Name'] = damper_air_out_name
        reheat_coil['object']['Air_Outlet_Node_Name'] = air_out_name

        # reheat_coil_comp = {
        #     'object': reheat_coil,
        #     'type': coil_key,
        #     'water_inlet_field': 'Water_Inlet_Node_Name',
        #     'water_outlet_field': 'Water_Outlet_Node_Name',
        #     'air_inlet_field': 'Air_Inlet_Node_Name',
        #     'air_outlet_field': 'Air_Outlet_Node_Name',
        # }

        component = {
            'object': terminal,
            'type': 'AirTerminal:SingleDuct:VAV:Reheat',
            'air_inlet_field': 'Air_Inlet_Node_Name',
            'air_outlet_field': 'Air_Outlet_Node_Name',
            'reheat_coil': reheat_coil
        }

        return component




