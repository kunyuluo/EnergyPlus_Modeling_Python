from eppy.modeleditor import IDF
from eppy.bunch_subclass import EpBunch
from Helper import get_all_targets
import math


class GeometryTool:
    @staticmethod
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

    @staticmethod
    def check_orientation(surface: EpBunch):
        angle_threshold = math.pi / 4
        orientation = None

        orient_vectors = {
            "east": (1, 0, 0),
            "west": (-1, 0, 0),
            "north": (0, 1, 0),
            "south": (0, -1, 0)}

        normal = GeometryTool.newell_method(surface)
        # print(normal)

        for key in orient_vectors.keys():
            dot_product = normal[0] * orient_vectors[key][0] + normal[1] * orient_vectors[key][1] + normal[2] * \
                          orient_vectors[key][2]
            angle = math.acos(dot_product)

            if angle <= angle_threshold:
                orientation = key
                break
            else:
                orientation = "other"

        return orientation

    @staticmethod
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

    @staticmethod
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
            v1_origin = (
                surface['Vertex_1_Xcoordinate'], surface['Vertex_1_Ycoordinate'], surface['Vertex_1_Zcoordinate'])
            vertice_1 = GeometryTool.move_point_along_vector(
                v1_origin, length_unit_vec, width_unit_vec, delta_length, delta_width)
            vertices[1] = vertice_1

            # vertice 2 of the window:
            v2_origin = (
                surface['Vertex_2_Xcoordinate'], surface['Vertex_2_Ycoordinate'], surface['Vertex_2_Zcoordinate'])
            vertice_2 = GeometryTool.move_point_along_vector(
                v2_origin, length_unit_vec, width_unit_vec_rev, delta_length, delta_width)
            vertices[2] = vertice_2

            # vertice 3 of the window:
            v3_origin = (
                surface['Vertex_3_Xcoordinate'], surface['Vertex_3_Ycoordinate'], surface['Vertex_3_Zcoordinate'])
            vertice_3 = GeometryTool.move_point_along_vector(
                v3_origin, length_unit_vec_rev, width_unit_vec_rev, delta_length, delta_width)
            vertices[3] = vertice_3

            # vertice 4 of the window:
            v4_origin = (
                surface['Vertex_4_Xcoordinate'], surface['Vertex_4_Ycoordinate'], surface['Vertex_4_Zcoordinate'])
            vertice_4 = GeometryTool.move_point_along_vector(
                v4_origin, length_unit_vec_rev, width_unit_vec, delta_length, delta_width)
            vertices[4] = vertice_4

            return vertices

        else:
            raise ValueError('The window ratio must be less than 0.95.')

    @staticmethod
    def create_window_by_ratio(idf: IDF, window_ratio: float | dict, construction: EpBunch | dict = None):
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
                vertices = GeometryTool.calculate_vertices(wall, window_ratio)
            elif isinstance(window_ratio, dict):
                try:
                    orientation = GeometryTool.check_orientation(wall)
                    vertices = GeometryTool.calculate_vertices(wall, window_ratio[orientation])
                except:
                    vertices = GeometryTool.calculate_vertices(wall, 0.4)
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
