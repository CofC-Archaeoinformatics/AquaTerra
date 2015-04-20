# ReadMe

***NEEDS WORK***

Topics that need to be covered in read me:
Basic Intro: What it does and works

Getting Started
---------------
***NEEDS WORK***

Installation
------------

It is assumed that you already have ArcGIS installed.

Place the "aquaterra.gdb" folder directly under your local "ArcGIS" folder
(Probably in Documents). This is the geodatabase that will be used with
AquaTerra(temporarily?).

Place the "AquaTerra.pyt" file in your "My Toolboxes" folder which is located
in the "AppData\Roaming\ESRI\Desktop10.2\ArcToolbox" directory. OR run the
"mover.bat" script while it is in the same location as the .pyt file. This is
the Python Toolbox that IS AquaTerra.

Using the Toolbox
-----------------

**NOTE:** To simplify the instructions it is assumed that you already know your way around ArcGIS.

In order to run the Tool in the toolbox, your GeoDatabase will need to contain at least the following:

- A Digital Elevation Model for the area of interest
- A Wind Speed Raster (not wind velocity or direction)
  - The Wind Raster and DEM need to have the same grid cell size
  - The Wind Raster and DEM need to habe the same map projection
  - The Wind Raster and DEM should (preferably) cover the same map area (i.e. have the same dimensions)
- A minimum of 2 points on the map (to go from point A to point B, there need to exist points A and B)

If you'd like to just take it for a testdrive and don't have a .GDB that happens to meet all of the requirements, no sweat! A sample database is included in the sourcecode.

Simply input all of the parameters into the tool, set the workspace, and run it.

**WARNING:** It *WILL* take a long time, but it might take several hours to complete with a sizable database.
