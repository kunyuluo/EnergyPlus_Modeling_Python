import eppy
from Obj_Structure import Obj_Tree
from eppy.modeleditor import IDF
from eppy import hvacbuilder
from Helper import delete_hvac_objs
from Helper import SomeFields, flattencopy, makepipebranch
from HVACSystem.HVACTools import PlantLoop
from HVACSystem.PlantLoopComponents import PlantLoopComponent
from HVACSystem.SetpointManager import SetpointManager

idd_file = 'Data/Energy+.idd'
try:
    IDF.setiddname(idd_file)
except eppy.modeleditor.IDDAlreadySetError as e:
    pass

# file_path = 'Data/CIB-Office.idf'
file_path = 'Data/TestOffice.idf'

my_model = IDF(file_path)
# my_model = IDF(file_path)
# my_model.printidf()

# all_objs = my_model.idfobjects
# print(all_objs.keys())
# bldg = all_objs['BUILDING'][0]
# print(bldg.Name)
# print(bldg.North_Axis)

# zones = all_objs['Sizing:System']
# print(zones)
# print(len(zones))

# Get all setpoint managers:
#####################################################################
# all_spms = all_objs['SetpointManager:MixedAir'.upper()]
# print(all_spms)

# Deleting existing defined objects:
#####################################################################
delete_hvac_objs(my_model)

# all_plantloop = all_objs['Chiller:Electric:EIR'.upper()]
# print(all_plantloop)

# Creating new plant loop:
#####################################################################
pipe1 = PlantLoopComponent.pipe(my_model, name='pipe1')
pipe2 = PlantLoopComponent.pipe(my_model, name='pipe2')
pipe3 = PlantLoopComponent.pipe(my_model, name='pipe3')
pipe4 = PlantLoopComponent.pipe(my_model, name='pipe4')
spm = SetpointManager.scheduled(my_model, name='spm')

newplantloop = PlantLoop.chilled_water_loop(
    my_model,
    name='Test Chilled Water Loop',
    supply_inlet_branches=pipe1,
    supply_branches=[[pipe2], [pipe3]],
    demand_branches=pipe4,
    setpoint_manager=spm)

# print(spm)
print(newplantloop)

# branch = my_model.newidfobject("BRANCH", Name='my_branch')
# comp1 = my_model.newidfobject('Pipe:Adiabatic'.upper(), Name='pipe1')
# comp2 = my_model.newidfobject('Pipe:Adiabatic'.upper(), Name='pipe2')
# branch['Component_1_Name'] = comp1.Name
# branch['Component_2_Name'] = comp2.Name
#
# branch2 = my_model.newidfobject("BRANCH", Name='my_branch2')
# connector = my_model.newidfobject("CONNECTOR:SPLITTER", Name='connector')
# connector.obj.append(branch.Name)
# connector.obj.append(branch2.Name)
#
# connectorlist = my_model.newidfobject("CONNECTORLIST", Name='connectorlist')
# print(connectorlist.fieldnames)
# # connectorlist['Connector_Type_1'] = 'Connector:Splitter'
# # connectorlist['Connector_1_Name'] = connector.Name
#
# # print(type(branch))
# print(branch)
# print(connector)
# print(connectorlist)

# # make the branch lists for this plant loop
# sbranchlist = my_model.newidfobject("BRANCHLIST", Name=newplantloop.Plant_Side_Branch_List_Name)
# dbranchlist = my_model.newidfobject("BRANCHLIST", Name=newplantloop.Demand_Side_Branch_List_Name)
#
# # add branch names to the branchlist
# sloop = ['chw_supply_inlet', ['chw_supply_branch1', 'chw_supply_branch2'], 'chw_supply_outlet']
# sbranchnames = flattencopy(sloop)
# for branchname in sbranchnames:
#     sbranchlist.obj.append(branchname)
#
# dloop = ['chw_demand_inlet', ['chw_demand_branch1', 'chw_demand_branch2'], 'chw_demand_outlet']
# dbranchnames = flattencopy(dloop)
# for branchname in dbranchnames:
#     dbranchlist.obj.append(branchname)
#
# # supply side
# sbranchs = []
# for bname in sbranchnames:
#     branch = makepipebranch(my_model, bname)
#     sbranchs.append(branch)
# print(sbranchs)
#
# # rename inlet outlet of endpoints of loop
# anode = "Component_1_Inlet_Node_Name"
# sameinnode = "Plant_Side_Inlet_Node_Name"
# sbranchs[0][anode] = newplantloop[sameinnode]
# anode = "Component_1_Outlet_Node_Name"
# sameoutnode = "Plant_Side_Outlet_Node_Name"
# sbranchs[-1][anode] = newplantloop[sameoutnode]
#
# # rename inlet outlet of endpoints of loop - rename in pipe
# pname = sbranchs[0]["Component_1_Name"]  # get the pipe name
# apipe = my_model.getobject("Pipe:Adiabatic".upper(), pname)  # get pipe
# apipe.Inlet_Node_Name = newplantloop[sameinnode]
# pname = sbranchs[-1]["Component_1_Name"]  # get the pipe name
# apipe = my_model.getobject("Pipe:Adiabatic".upper(), pname)  # get pipe
# apipe.Outlet_Node_Name = newplantloop[sameoutnode]

# # Get all plant loops:
# all_plantloop = all_objs['PlantLoop'.upper()]
# all_plantloop[1].Maximum_Loop_Temperature = 25
# print(all_plantloop)


# Save to a new file:
#####################################################################
# my_model.saveas('Data/TestOffice_empty.idf')
