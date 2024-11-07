from eppy.modeleditor import IDF
from eppy.bunch_subclass import EpBunch


class PlantLoopComponent:

    @staticmethod
    def sizing(
            idf: IDF,
            plantloop: EpBunch | str,
            loop_type: int = 1,
            loop_exit_temp=None,
            loop_temp_diff=None,
            sizing_option: int = None,
            zone_timesteps_in_averaging_window=None,
            coincident_sizing_factor_mode: int = 1):
        """
        -Loop_type: 1:Cooling 2:Heating 3:Condenser 4:Steam \n

        -Sizing_option:
        1: Coincident
        2: NonCoincident
        (Default is NonCoincident) \n

        -Coincident_sizing_factor_mode: \n
        1: None \n
        2: GlobalCoolingSizingFactor \n
        3: GlobalHeatingSizingFactor \n
        4: LoopComponentSizingFactor
        """

        loop_types = {1: "Cooling", 2: "Heating", 3: "Condenser", 4: "Steam"}
        sizing_options = {1: "Coincident", 2: "NonCoincident"}
        sizing_factor_modes = {1: "None", 2: "GlobalCoolingSizingFactor",
                               3: "GlobalHeatingSizingFactor", 4: "LoopComponentSizingFactor"}
        sizing = idf.newidfobject('Sizing:Plant'.upper())

        if isinstance(plantloop, EpBunch):
            sizing['Plant_or_Condenser_Loop_Name'] = plantloop.Name
        elif isinstance(plantloop, str):
            sizing['Plant_or_Condenser_Loop_Name'] = plantloop
        else:
            raise TypeError('Invalid input type of plantloop.')

        sizing['Loop_Type'] = loop_types[loop_type]

        if loop_exit_temp is not None:
            sizing['Design_Loop_Exit_Temperature'] = loop_exit_temp
        if loop_temp_diff is not None:
            sizing['Loop_Design_Temperature_Difference'] = loop_temp_diff
        if zone_timesteps_in_averaging_window is not None:
            sizing['Zone_Timesteps_in_Averaging_Window'] = zone_timesteps_in_averaging_window

        sizing['Sizing_Option'] = sizing_options[sizing_option]
        sizing['Coincident_Sizing_Factor_Mode'] = sizing_factor_modes[coincident_sizing_factor_mode]

        return sizing

    @staticmethod
    def pipe(idf: IDF, name=None, pipe_type: int = 1):
        """
        -Pipe_type:
            1:Adiabatic 2:Indoor 3:Outdoor 4:Adiabatic:Steam 5: Underground
        """
        pipe_types = {1: "Pipe:Adiabatic", 2: "Pipe:Indoor", 3: "Pipe:Outdoor",
                      4: "Pipe:Adiabatic:Steam", 5: "Pipe:Underground"}

        name = f'Pipe_{pipe_types[pipe_type].split(":")[-1]}' if name is None else name
        pipe = idf.newidfobject(pipe_types[pipe_type].upper(), Name=name)
        pipe.Inlet_Node_Name = f'{name}_inlet'
        pipe.Outlet_Node_Name = f'{name}_outlet'

        component = {
            'object': pipe,
            'type': pipe_types[pipe_type]
        }

        return component
