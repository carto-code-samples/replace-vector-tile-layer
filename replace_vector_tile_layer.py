"""
Name: replace_vector_tile_layer.py
Description: Replace a hosted vector tile layer with an updated version
from a map in a project while retaining the item name, id, and url. 
"""
import os
import datetime
import arcpy
from arcgis.gis import GIS

now = datetime.datetime.now()
date_time = "%d_%d_%d_%d_%d" % (now.year, now.month, now.day, now.hour, now.minute)

# Enter the URL and login credentials to the ArcGIS Online or Enterprise account containing the layer to be updated. 
gis = GIS("<your url>", "<your username", "<your password>")

# The id of the service to be replaced, a string like '223525bd6dd344e3b405cba33f30947d'
published_service_id = ''

# The local folder, project file, and map containing the updated data.
root_dir = "C:/projects/MyProject"
in_aprx = "MyProject.aprx"
map_name = "MyMap"

# Open the project with the updated map, prepare to package it as a vtpk
project = arcpy.mp.ArcGISProject(os.path.join(root_dir, in_aprx))
updated_map = project.listMaps(map_name)[0]
updated_vtpk = os.path.join(root_dir, updated_map.name + "_" + date_time+ ".vtpk") 

# Create a new vtpk from the map
print("Packaging map: " + updated_map.name)
arcpy.CreateVectorTilePackage_management(updated_map, updated_vtpk, "ONLINE")

# Add the updated vtpk to the portal content and publish it as a hosted tile layer service.
updated_service_title = map_name + "_updated_" + date_time
vtpk_properties = {
    'title': updated_service_title,
    'description': 'Updated/staged version of ' + map_name,
    'tags': 'update'
}
vtpk_item = gis.content.add(item_properties=vtpk_properties, data=updated_vtpk)
print("Publishing updated tile layer...")
vtpk_service_item = vtpk_item.publish()

# Replace the old hosted tile layer service with the updated one.
print("Replacing service...")
gis.content.replace_service(published_service_id, vtpk_service_item.id)    
    
print("")
print("done")
