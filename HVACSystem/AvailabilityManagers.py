from eppy.modeleditor import IDF
from eppy.bunch_subclass import EpBunch


class AvailabilityManager:
    @staticmethod
    def scheduled(idf: IDF, name: str = None, schedule: EpBunch | str = None):
        name = 'Scheduled Availability Manager' if name is None else name
        avail_manager = idf.newidfobject('AvailabilityManager:Scheduled', Name=name)
        if schedule is not None:
            if isinstance(schedule, str):
                avail_manager['Schedule_Name'] = schedule
            elif isinstance(schedule, EpBunch):
                avail_manager['Schedule_Name'] = schedule.Name
            else:
                raise TypeError('Schedule must be EpBunch or str')
        else:
            avail_manager['Schedule_Name'] = 'Always On Discrete'

        return avail_manager

    @staticmethod
    def night_cycle(
            idf: IDF,
            name: str = None,
            schedule: EpBunch | str = None,
            fan_schedule: EpBunch | str = None,
            control_type: int = 2,
            thermostat_tol=1.0,
            cycling_run_time_control_type: int = 1,
            cycling_run_time=1800,):
        """
        -Control Type: 1.StayOff, 2.CycleOnAny, 3.CycleOnControlZone, 4.CycleOnAnyZoneFansOnly,
        5.CycleOnAnyCoolingOrHeatingZone, 6.CycleOnAnyCoolingZone, 7.CycleOnAnyHeatingZone,
        8.CycleOnAnyHeatingZoneFansOnly \n
        -Cycling Run Time Control Type: 1.FixedRunTime, 2.Thermostat, 3.ThermostatWithMinimumRunTime
        """
        control_types = {1: 'StayOff', 2: 'CycleOnAny', 3: 'CycleOnControlZone', 4: 'CycleOnAnyZoneFansOnly',
                         5: 'CycleOnAnyCoolingOrHeatingZone', 6: 'CycleOnAnyCoolingZone', 7: 'CycleOnAnyHeatingZone',
                         8: 'CycleOnAnyHeatingZoneFansOnly'}
        cycling_control_types = {1: 'FixedRunTime', 2: 'Thermostat', 3: 'ThermostatWithMinimumRunTime'}

        name = 'Night Cycle Availability Manager' if name is None else name
        avail_manager = idf.newidfobject('AvailabilityManager:NightCycle', Name=name)
        if schedule is not None:
            if isinstance(schedule, str):
                avail_manager['Schedule_Name'] = schedule
            elif isinstance(schedule, EpBunch):
                avail_manager['Schedule_Name'] = schedule.Name
            else:
                raise TypeError('Schedule must be EpBunch or str')
        else:
            avail_manager['Schedule_Name'] = 'Always On Discrete'

        if fan_schedule is not None:
            if isinstance(fan_schedule, str):
                avail_manager['Fan_Schedule_Name'] = fan_schedule
            elif isinstance(fan_schedule, EpBunch):
                avail_manager['Fan_Schedule_Name'] = fan_schedule.Name
            else:
                raise TypeError('Fan_Schedule must be EpBunch or str')
        else:
            avail_manager['Fan_Schedule_Name'] = 'Always On Discrete'

        avail_manager['Control_Type'] = control_types[control_type]
        avail_manager['Cycling_Run_Time_Control_Type'] = cycling_control_types[cycling_run_time_control_type]
        avail_manager['Thermostat_Tolerance'] = thermostat_tol
        avail_manager['Cycling_Run_Time'] = cycling_run_time

        return avail_manager
