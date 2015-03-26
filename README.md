# ReadMe

***NEEDS WORK***

Topics that need to be covered in read me:
Basic Intro: What it does and works

*** Getting Started *** 
Needs to be placed

Installation
============

It is assumed that you already have ArcGIS installed.

Place the "aquaterra.gdb" folder directly under your local "ArcGIS" folder
(Probably in Documents). This is the geodatabase that will be used with
AquaTerra(temporarily?).

Place the "AquaTerra.pyt" file in your "My Toolboxes" folder which is located
in the "AppData\Roaming\ESRI\Desktop10.2\ArcToolbox" directory. OR run the
"mover.bat" script while it is in the same location as the .pyt file. This is
the Python Toolbox that IS AquaTerra.

Using the Toolbox
=================

Upon opening ArcCatalog you should find aquaterra.gdb under Folder
Connections and AquaTerra.pyt under "Toolboxes/My Toolboxes" if you have
completed the Installation section above.

Double click on and run the Tool. In the window that appears fill in all the
fields using data from the aquaterra geodatabase. *Important:* The "DEM of
AOI" must be set to "aoidem" and "Wind Raster" must be set to
"krig_apr_0600". Under the Environment settings the current workspace must be
set to Default.gbd as this is where the work will be done.

You may now run the script! It can take a very long time to calculate. 
