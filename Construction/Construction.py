from eppy.modeleditor import IDF
from eppy.bunch_subclass import EpBunch
from Helper import get_all_targets


class Construction:
    @staticmethod
    def opaque_no_mass_cons(
            idf: IDF,
            name: str = None,
            thermal_resistance=None,
            roughness: int = 2,
            thermal_absorptance=0.9,
            solar_absorptance=0.7,
            visible_absorptance=0.7,
            test_mode: bool = False):
        """
        Roughness: 0: 'VeryRough', 1: 'Rough', 2: 'MediumRough', 3: 'MediumSmooth', 4: 'Smooth', 5: 'VerySmooth'
        """
        roughness_options = {0: 'VeryRough', 1: 'Rough', 2: 'MediumRough', 3: 'MediumSmooth',
                             4: 'Smooth', 5: 'VerySmooth'}

        name = "Opaque_No_Mass_Cons" if name is None else name
        mat_name = name + '_Mat'

        material = idf.newidfobject("Material:NoMass")
        material['Name'] = mat_name
        material['Roughness'] = roughness_options[roughness]
        material['Thermal_Resistance'] = thermal_resistance
        material['Thermal_Absorptance'] = thermal_absorptance
        material['Solar_Absorptance'] = solar_absorptance
        material['Visible_Absorptance'] = visible_absorptance

        cons = idf.newidfobject("Construction")
        cons['Name'] = name
        cons['Outside_Layer'] = mat_name

        cons_assambly = {
            'Construction': cons,
            'Material': material
        }

        if test_mode:
            return cons_assambly
        else:
            return cons

    @staticmethod
    def window_cons_simple(
            idf: IDF,
            name: str = None,
            u_factor=0.5,
            shgc=0.5,
            vt=0.7,
            test_mode: bool = False):

        name = "Window_Simple" if name is None else name
        mat_name = name + '_Mat'

        material = idf.newidfobject('WindowMaterial:SimpleGlazingSystem')
        material['Name'] = mat_name
        material['UFactor'] = u_factor
        material['Solar_Heat_Gain_Coefficient'] = shgc
        material['Visible_Transmittance'] = vt

        win = idf.newidfobject('Construction')
        win['Name'] = name
        win['Outside_Layer'] = mat_name

        win_assambly = {
            'Construction': win,
            'Material': material
        }

        if test_mode:
            return win_assambly
        else:
            return win


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