import os
os.environ["PROJ_LIB"] = "C:\\Users\\baidak\\Miniconda3\\pkgs\\proj-7.2.0-h1cfcee9_2\\Library\\share\\proj"
os.environ["GDAL_DATA"] = "C:\\Users\\baidak\\Miniconda3\\pkgs\\proj-7.2.0-h1cfcee9_2\\Library\\share"
import fiona
import pandas as pd

class ShpNotFoundError(Exception):
	pass

class LayersStructureNotFoundError(Exception):
	pass

class WrongLayerNameError(Exception):
	pass

class UtilityShpFilesError(Exception):
	pass

class RestoreShp:
	def __init__(self):
		pass

	def restore(self, shp_path):
		if not os.path.exists("layers_structure.xlsx"):
			raise LayersStructureNotFoundError
		if not os.path.exists(shp_path):
			raise ShpNotFoundError(".shp not found, fix the path")

		# get dataftame with shp layer_df structure
		layer_name = os.path.basename(shp_path).split(".")[0]
		try:
			layer_df = pd.read_excel("layers_structure.xlsx", sheet_name = layer_name)
		except ValueError:
			raise WrongLayerNameError

		# replace data types with fiona types
		layer_df["ТИП ДАННЫХ"] = layer_df["ТИП ДАННЫХ"].replace({
			"Text": "str",
			"Float": "float",
			"Long Integer": "int",
			"Short Integer": "int",
			"data": "date"
		})

		# build fiona schema
		properties = {}
		for i in range(1,len(layer_df)):
			properties[layer_df["АТРИБУТ"][i]] = layer_df["ТИП ДАННЫХ"][i] + ": " + str(layer_df["ШИРИНА"][i])
		layer_type = layer_name[-3:]
		fiona_geometry_types = {"LIN": "LineString", "POL": "Polygon", "PNT": "Point", "TXT": "Point"}
		schema = {"geometry": fiona_geometry_types[layer_type], "properties": properties}

		# store initial shp objects in list
		with fiona.open(shp_path, "r") as shp:
			objects_list = []
			for i in range(len(shp)):
				objects_list.append(shp[i])

		# create restored shps folder if doesn't exist
		restored_folder_path = os.path.abspath(shp_path).replace(os.path.basename(shp_path), "") + "восстановленные"
		if not os.path.exists(restored_folder_path):
			os.makedirs(restored_folder_path)

		# create empty shp
		with fiona.open(restored_folder_path + "\\" + os.path.basename(shp_path),"w", "ESRI Shapefile", schema = schema, encoding="WINDOWS-1251") as shp:
			pass

		# add objects from list to shp w/o last one (which presumably breaks the shp)
		try:
			with fiona.open(restored_folder_path + "\\" + os.path.basename(shp_path),"a", "ESRI Shapefile", schema = schema, encoding="WINDOWS-1251") as shp:
				for i in range(len(objects_list) - 1):
					shp.write({"geometry": objects_list[i]["geometry"], "properties": objects_list[i]["properties"]})
		except ValueError:
			raise UtilityShpFilesError
		