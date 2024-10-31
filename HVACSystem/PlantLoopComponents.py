from eppy.modeleditor import IDF
from eppy.bunch_subclass import EpBunch


class PlantLoopComponent:
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
