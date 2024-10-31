import copy

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
        "Branch List Name",
        "Connector List Name",
        "Supply Side Inlet Node Name",
        "Demand Side Outlet Node Name",
        "Demand Side Inlet Node Names",
        "Supply Side Outlet Node Names",
    ]


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
                       'Controllers', 'Heat_Recovery', 'Performance_Curves', 'System_Sizing',
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


def makepipecomponent(idf, pname):
    """make a pipe component
    generate inlet outlet names"""
    apipe = idf.newidfobject("Pipe:Adiabatic".upper(), Name=pname)
    apipe.Inlet_Node_Name = "%s_inlet" % (pname,)
    apipe.Outlet_Node_Name = "%s_outlet" % (pname,)
    return apipe


def makepipebranch(idf, bname):
    """make a branch with a pipe
    use standard inlet outlet names"""
    # make the pipe component first
    pname = "%s_pipe" % (bname,)
    apipe = makepipecomponent(idf, pname)
    # now make the branch with the pipe in it
    abranch = idf.newidfobject("BRANCH", Name=bname)
    abranch.Component_1_Object_Type = "Pipe:Adiabatic"
    abranch.Component_1_Name = pname
    abranch.Component_1_Inlet_Node_Name = apipe.Inlet_Node_Name
    abranch.Component_1_Outlet_Node_Name = apipe.Outlet_Node_Name
    # abranch.Component_1_Branch_Control_Type = "Bypass"
    return abranch

