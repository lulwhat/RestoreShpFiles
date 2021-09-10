### Restore broken ArcGIS .shp files

Working with shapefiles in AutoCAD Civil/Map and moving objects from layer to layer regularly break the shapes. 
This program simply takes all objects in chosen shp, removes last one, which most likely is the cause of trouble, and creates a new restored shapefile 1 element shorter.

Runs on *Python 3*

.shp reading and writing is executed with *Fiona* package

UI is executed with *PyQt5* package

Requirements are listed in [requirements.txt](/requirements.txt)

**To run the app use** `python app_restore_shp.py`