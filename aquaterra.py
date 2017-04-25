# ---------------------------------------------------------------------------
#Aquaterra creates a uniformed cost surface model that can be used to project potential routes. 
#It addresses the issue of high geographical dependency of the existing tools.

#The model calculates the walking distance and effort based on parameters provided by a user.

#Bug: Raster calculator line# 218: str + float concatenation. The inputs for the function need to be looked at.
#The function was taken from the original ArcGis code, so the issue is either with the user parameter types or somewhere in the 
#body of the code.
# ---------------------------------------------------------------------------

# Import arcpy module
import arcpy

# Local variables:
origin_shp = "O:\\argolida\\data\\shapefiles\\origin.shp"
destination_shp = "O:\\argolida\\data\\shapefiles\\destination.shp"
enter_the_DEM = "O:\\argolida\\data\\databases\\argolida.gdb\\aoidem"
aquaterra_gdb = "C:\\"
Point_of_Origin = "O:\\argolida\\data\\databases\\argolida.gdb\\korphos"
aoidem_copy = "c:\\aquaterra.gdb\\aoidem_copy"
land_mask = "C:\\aquaterra.gdb\\land_mask"
flow_acc = "C:\\aquaterra.gdb\\flow_acc"
flow_accum_1 = "C:\\aquaterra.gdb\\flow_accum_1"
slope__2_ = "C:\\aquaterra.gdb\\slope"
slope_plus1 = "C:\\aquaterra.gdb\\slope_plus1"
flow_div_slop = "C:\\aquaterra.gdb\\flow_div_slop"
moist_index = "C:\\aquaterra.gdb\\moist_index"
Greater_mois1 = "C:\\aquaterra.gdb\\greater_mois1"
boggy_bits = "C:\\aquaterra.gdb\\boggy_bits"
Times_boggy = "C:\\aquaterra.gdb\\Times_boggy"
dem_n_bog = "C:\\aquaterra.gdb\\dem_n_bog"
dem_n_bog_slp = "C:\\aquaterra.gdb\\dem_n_bog_slp"
dem_x_pi = "C:\\aquaterra.gdb\\dem_x_pi"
demxpi_by_180 = "C:\\aquaterra.gdb\\demxpi_by_180"
Tan_demxpi_b1 = "C:\\aquaterra.gdb\\Tan_demxpi_b1"
effort = "C:\\aquaterra.gdb\\effort"
Plus_demxpi_1 = "C:\\aquaterra.gdb\\Plus_demxpi_1"
Abs_Plus_dem1 = "C:\\aquaterra.gdb\\Abs_Plus_dem1"
Times_Abs_Pl1 = "C:\\aquaterra.gdb\\Times_Abs_Pl1"
Exp_Times_Ab1 = "C:\\aquaterra.gdb\\Exp_Times_Ab1"
walking_dist = "C:\\aquaterra.gdb\\walking_dist"
Output_raster__3_ = "C:\\aquaterra.gdb\\Greater_dem_1"
LessThan12 = "C:\\aquaterra.gdb\\LessThan12"
mor5less12slp = "C:\\aquaterra.gdb\\mor5less12slp"
v5to12_penalty = "C:\\aquaterra.gdb\\ms5to12"
rise_of_all_aoi = "C:\\aquaterra.gdb\\rise_of_all_aoi"
nais_penalties_5to12 = "C:\\aquaterra.gdb\\nais_penalties_5to12"
Greaterthan12 = "C:\\aquaterra.gdb\\Greaterthan12"
ms_more12 = "C:\\aquaterra.gdb\\ms_more12"
nais_penalties_more12 = "C:\\aquaterra.gdb\\nais_penalties_more12"
naismith_rule = "C:\\aquaterra.gdb\\naismith_rule"
terra_cost_rev = "C:\\aquaterra.gdb\\terra_cost_rev"
terra_cost_masked = "C:\\aquaterra.gdb\\terra_cost_masked"
krig_apr_0600 = "O:\\argolida\\data\\databases\\argolida.gdb\\krig_apr_0600"
wind_rast_n_ = "C:\\aquaterra.gdb\\wind_rast%n%"
windata_mask_n_ = "C:\\aquaterra.gdb\\windata_mask%n%"
wind_knots2ms_n_ = "C:\\aquaterra.gdb\\wind_knots2ms%n%"
ovrwindeffrt = "C:\\aquaterra.gdb\\ovrwindeffrt"
terra_marine_cost = "C:\\aquaterra.gdb\\terra_marine_cost"
cd_apr2 = "C:\\aquaterra.gdb\\cd_apr2"
cost_backlnkapr2 = "C:\\aquaterra.gdb\\cost_backlnkapr2"
path_dec_naismith = "C:\\aquaterra.gdb\\path_dec_naismith"
a2b__no_cultural_effects = "O:\\argolida\\data\\databases\\epidauria_human.gdb\\balancedeffort_korphos2mykenai"
korphos = "O:\\argolida\\data\\databases\\argolida.gdb\\korphos"
CostDis_dest2 = "C:\\aquaterra.gdb\\CostDis_dest2"
effbklnkmyk = "C:\\aquaterra.gdb\\effbklnkmyk"
effortpthkorphmyk = "O:\\argolida\\marine_terrestrial_model\\marine_terrestrial_model\\Default.gdb\\effortpthkorphmyk"
effort_path_korph2myc = "C:\\aquaterra.gdb\\effort_path_korph2myc_bounded.shp"
naismith_masked = "C:\\aquaterra.gdb\\naismith_masked"
CostDis_dest1 = "C:\\aquaterra.gdb\\CostDis_dest1"
timebklnkmyk = "C:\\aquaterra.gdb\\timebklnkmyk"
CostPat_korp2 = "C:\\aquaterra.gdb\\CostPat_korp2"
time_path_korph2myc = "C:\\aquaterra.gdb\\time_path_korph2myc.shp"
walkDis_myki1 = "C:\\aquaterra.gdb\\walkDis_myki1"
walkbklnkmyk = "C:\\aquaterra.gdb\\walkbklnkmyk"
walkpthkorphmyk = "C:\\aquaterra.gdb\\walkpthkorphmyk"
Effort_Path___Terrestrial_Only = "O:\\argolida\\marine_terrestrial_model\\marine_terrestrial_model\\walk_path_korph2myc.shp"
korphos__2_ = "O:\\argolida\\data\\databases\\argolida.gdb\\korphos"
mykinai__2_ = "O:\\argolida\\data\\databases\\argolida.gdb\\mykinai"
CostDisterra_myki = "C:\\aquaterra.gdb\\CostDisterra_myki"
terrabklnkmyk = "O:\\argolida\\marine_terrestrial_model\\marine_terrestrial_model\\Default.gdb\\terrabklnkmyk"
terrapthkorphmyk = "C:\\aquaterra.gdb\\terrapthkorphmyk"
effort_path_korph2myc__3_ = "C:\\aquaterra.gdb\\terra_path_50nais50effort.shp"
naismith_wind_cost = "O:\\argolida\\marine_terrestrial_model\\marine_terrestrial_model\\Default.gdb\\naismith_wind_cost"
costdist_korphos = "C:\\aquaterra.gdb\\costdist_korphos"
costdist_korphos_zero = "O:\\argolida\\marine_terrestrial_model\\marine_terrestrial_model\\Default.gdb\\costdist_korphos_zero"
dist_percent_korphos__2_ = "O:\\argolida\\marine_terrestrial_model\\marine_terrestrial_model\\Default.gdb\\dist_percent_korphos"
costdist_korphos_weighted = "C:\\aquaterra.gdb\\costdist_korphos_weighted"
costdist_korphos_onesies = "O:\\argolida\\marine_terrestrial_model\\marine_terrestrial_model\\Default.gdb\\costdist_korphos_onesies"
costdist_attractors_mosaicd_noisthmia = costdist_korphos_onesies
epidavros = "O:\\argolida\\data\\databases\\argolida.gdb\\epidavros"
costdist_epidavros = "C:\\aquaterra.gdb\\costdist_epidavros"
costdist_epidavros_zero = "O:\\argolida\\marine_terrestrial_model\\marine_terrestrial_model\\default.gdb\\costdist_epidavros_zero"
dist_percent_epidavros__2_ = "O:\\argolida\\marine_terrestrial_model\\marine_terrestrial_model\\default.gdb\\dist_percent_epidavros"
costdist_epidavros_weighted = "C:\\aquaterra.gdb\\costdist_epidavros_weighted"
costdist_epidavros_onesies = "O:\\argolida\\marine_terrestrial_model\\marine_terrestrial_model\\default.gdb\\costdist_epidavros_onesies"
default_gdb__2_ = "O:\\argolida\\marine_terrestrial_model\\marine_terrestrial_model\\default.gdb"
costsurf_main_culturally_adjustedtimes = "O:\\argolida\\marine_terrestrial_model\\marine_terrestrial_model\\default.gdb\\costsurf_main_culturally_adjustedtimes"
land1water0 = "O:\\argolida\\marine_terrestrial_model\\marine_terrestrial_model\\default.gdb\\land1water0"
costsurf_main_cultadjusted_land = "O:\\argolida\\marine_terrestrial_model\\marine_terrestrial_model\\default.gdb\\costsurf_main_cultadjusted_land"
land0water1 = "O:\\argolida\\marine_terrestrial_model\\marine_terrestrial_model\\default.gdb\\land0water1"
costsurf_main_water = "C:\\aquaterra.gdb\\costsurf_main_water"
costsurf_mainadjusted = "O:\\argolida\\marine_terrestrial_model\\marine_terrestrial_model\\default.gdb\\costsurf_mainadjusted"
costdist_main = "O:\\argolida\\marine_terrestrial_model\\marine_terrestrial_model\\default.gdb\\costdist_main"
backlink_main = "O:\\argolida\\marine_terrestrial_model\\marine_terrestrial_model\\default.gdb\\backlink_main"
costpath_cultweighted = "O:\\argolida\\marine_terrestrial_model\\marine_terrestrial_model\\default.gdb\\costpath_cultweighted"
costpath_cultweighted_line = "O:\\argolida\\marine_terrestrial_model\\marine_terrestrial_model\\default.gdb\\costpath_cultweighted_line"
isthmia = "O:\\argolida\\data\\databases\\argolida.gdb\\isthmia"
costdist_isthmia = "C:\\aquaterra.gdb\\costdist_isthmia"
costdist_isthmia_zero = "O:\\argolida\\marine_terrestrial_model\\marine_terrestrial_model\\default.gdb\\costdist_isthmia_zero"
dist_percent_isthmia = "O:\\argolida\\marine_terrestrial_model\\marine_terrestrial_model\\default.gdb\\dist_percent_isthmia"
costdist_isthmia_weighted = "C:\\aquaterra.gdb\\costdist_isthmia_weighted"
costdist_isthmia_onesies = "O:\\argolida\\marine_terrestrial_model\\marine_terrestrial_model\\default.gdb\\costdist_isthmia_onesies"
dist_detractpercent_epidavros = "O:\\argolida\\marine_terrestrial_model\\marine_terrestrial_model\\default.gdb\\dist_detractpercent_epidavros"
costdist_detractepidavros = "O:\\argolida\\marine_terrestrial_model\\marine_terrestrial_model\\default.gdb\\costdist_detractepidavros"
dist_detractpercent_korphos = "O:\\argolida\\marine_terrestrial_model\\marine_terrestrial_model\\default.gdb\\dist_detractpercent_korphos"
costdist_detractkorphos = "O:\\argolida\\marine_terrestrial_model\\marine_terrestrial_model\\default.gdb\\costdist_detractkorphos"
dist_detractpercent_isthmia = "O:\\argolida\\marine_terrestrial_model\\marine_terrestrial_model\\default.gdb\\dist_detractpercent_isthmia"
costdist_detractisthmia = "O:\\argolida\\marine_terrestrial_model\\marine_terrestrial_model\\default.gdb\\costdist_detractisthmia"
costdist_detractors_mosaicd_isthmia = costdist_detractisthmia
costsurf_main_detractculturally_adjustedtimes = "O:\\argolida\\marine_terrestrial_model\\marine_terrestrial_model\\default.gdb\\costsurf_main_detractculturally_adjustedtimes"
costsurf_main_detractcultadjusted_land = "O:\\argolida\\marine_terrestrial_model\\marine_terrestrial_model\\default.gdb\\costsurf_main_detractcultadjusted_land"
costsurf_maindetractadjusted = "O:\\argolida\\marine_terrestrial_model\\marine_terrestrial_model\\default.gdb\\costsurf_maindetractadjusted"
costdistdetract_main = "O:\\argolida\\marine_terrestrial_model\\marine_terrestrial_model\\default.gdb\\costdistdetract_main"
backlinkdetract_main = "O:\\argolida\\marine_terrestrial_model\\marine_terrestrial_model\\default.gdb\\backlinkdetract_main"
costpath_detractcultweighted = "O:\\argolida\\marine_terrestrial_model\\marine_terrestrial_model\\default.gdb\\costpath_detractcultweighted"
costpath_detractcultweighted_line = "O:\\argolida\\marine_terrestrial_model\\marine_terrestrial_model\\default.gdb\\costpath_detractcultweighted_line"
costdist_detractors_zeroed = "O:\\argolida\\marine_terrestrial_model\\marine_terrestrial_model\\default.gdb\\costdist_detractors_zeroed"
costdist_attractdetractors_mosaicd = costdist_detractors_zeroed
costdist_attractors_zeroed = "O:\\argolida\\marine_terrestrial_model\\marine_terrestrial_model\\default.gdb\\costdist_attractors_zeroed"
default_gdb__3_ = "O:\\argolida\\marine_terrestrial_model\\marine_terrestrial_model\\default.gdb"
costdist_attractdetract_onesies = "O:\\argolida\\marine_terrestrial_model\\marine_terrestrial_model\\default.gdb\\costdist_attractdetract_onesies"
costsurf_main_attractdetract_adjustedtimes = "O:\\argolida\\marine_terrestrial_model\\marine_terrestrial_model\\default.gdb\\costsurf_main_attractdetract_adjustedtimes"
costsurf_main_attractdetract_land = "O:\\argolida\\marine_terrestrial_model\\marine_terrestrial_model\\default.gdb\\costsurf_main_attractdetract_land"
costsurf_main_attractdetractadjusted = "O:\\argolida\\marine_terrestrial_model\\marine_terrestrial_model\\default.gdb\\costsurf_main_attractdetractadjusted"
costdist_main_attractdetract = "O:\\argolida\\marine_terrestrial_model\\marine_terrestrial_model\\default.gdb\\costdist_main_attractdetract"
backlink_main_attractdetract = "O:\\argolida\\marine_terrestrial_model\\marine_terrestrial_model\\default.gdb\\backlink_main_attractdetract"
costpath_attractdetract = "O:\\argolida\\marine_terrestrial_model\\marine_terrestrial_model\\default.gdb\\costpath_attractdetract"
costpath_attractdetract_line = "O:\\argolida\\marine_terrestrial_model\\marine_terrestrial_model\\default.gdb\\costpath_attractdetract_line"
    

#Provide the DEM 
dem = arcpy.GetParameterAsText(0)
if dem == '#' or not dem:
    dem = "O:\argolida\data\databases\argolida.gdb\aoidem" # provide a default value if unspecified

mykinai = arcpy.GetParameterAsText(8)
if mykinai == '#' or not mykinai:
    mykinai = "O:\\argolida\\data\\databases\\argolida.gdb\\mykinai" # provide a default value if unspecified

#Copy features, create File GDB and copy raster
origin = arcpy.CopyFeatures_management(Point_of_Origin, origin_shp, "", "0", "0", "0")
arcpy.CopyFeatures_management(mykinai, destination_shp, "", "0", "0", "0")
arcpy.CreateFileGDB_management("C:\\", "aquaterra.gdb", "CURRENT")
arcpy.CopyRaster_management(dem, aoidem_copy, "", "", "2147483647", "NONE", "NONE", "", "NONE", "NONE", "", "NONE")

#Ask user if marshy areas need to be avoided
marshy_areas = arcpy.GetParameterAsText(1)
if marshy_areas == '#' or not marshy_areas:
    marshy_areas = False # provide a default value if unspecified

#If marshy areas are to be avoided, take user input for the barrier height in meters
if marshy_areas == True:
    barrier = arcpy.GetParameterAsText(3)
    if barrier == "#" or not barrier:
        barrier = "10" # provide a default value if unspecified
else:
    barrier = "10"

# Process: Compare Raster values to 0 and sort out those that are >0 (Greater Than (2))
land_mask_var = arcpy.gp.GreaterThan_sa(aoidem_copy, "0", land_mask)

# Ln(Flow Accumulation plus 1 devided by Slope plus 1)
# Process: Flow Accumulation, Plus, Slope, Plus(2), Divide, Ln
moisture_index = arcpy.gp.Ln_sa(arcpy.gp.Divide_sa(arcpy.gp.Plus_sa(arcpy.gp.FlowAccumulation_sa(aoidem_copy, flow_acc, "", "FLOAT"), "1", flow_accum_1), arcpy.gp.Plus_sa(arcpy.gp.Slope_sa(aoidem_copy, slope__2_, "DEGREE", "1"), "1", slope_plus1), flow_div_slop), moist_index)

# All the raster values in Moisture Index that are less than 0  are set to 0 and multiplied by the user-selected augment factor for lowland features. This augment factor is then added to the Digital Elevation Model,
# resulting in a DEM that includes an augmentation factor that accentuates lowland places. When a slope calculation is made, the lowland areas will have an increased slope value, making them 'unsavory' to LCP modeling.
# Process: Greater Than, Times, Times(2), Plus(3)
dem = arcpy.gp.Plus_sa(arcpy.gp.Times_sa(arcpy.gp.Times_sa(arcpy.gp.GreaterThan_sa(moisture_index, "0", Greater_mois1), moisture_index, boggy_bits), barrier, Times_boggy), aoidem_copy, dem_n_bog)

# Build a slope of the surface that is a combination of elevation and the augmented lowland features
# Process: Slope (4)
dem_n_bog_slp = arcpy.gp.Slope_sa(dem, dem_n_bog_slp, "DEGREE", "1")


# Land travel how much weight (as %) is given to the quickest route
weight = arcpy.GetParameterAsText(6)
if weight == "#" or not weight:
    weight = "0" # provide a default value if unspecified

if weight == 0:
    # tan(dem_n_bog_slp*Pi/180)
    # Process: Times (3), Divide (2), Tan
    div = arcpy.gp.Divide_sa(arcpy.gp.Times_sa(dem_n_bog_slp, "3.141592654", dem_x_pi), "180", demxpi_by_180)

    # Effort = tan/0.017455065
    # Process: Divide (3)
    tan = arcpy.gp.Tan_sa(div, Tan_demxpi_b1)
    effort = arcpy.gp.Divide_sa(tan, "0.017455065", effort)    

elif weight == 1:
    method = arcpy.GetParameterAsText(7)
    if method == "Naismith":      
        greater_than_five = arcpy.gp.GreaterThanEqual_sa(dem_n_bog_slp, "5", Output_raster__3_)
        less_than_twelve = arcpy.gp.LessThan_sa(dem_n_bog_slp, "12", LessThan12)
        five_to_twelve = arcpy.gp.Times_sa(arcpy.gp.Times_sa(greater_than_five, less_than_twelve,
                                                             mor5less12slp), "1.998", v5to12_penalty)
	# tan(dem_n_bog_slp*Pi/180)
    	# Process: Times (3), Divide (2), Tan
    	div = arcpy.gp.Divide_sa(arcpy.gp.Times_sa(dem_n_bog_slp, "3.141592654", dem_x_pi), "180", demxpi_by_180)

    	# Effort = tan/0.017455065
    	# Process: Divide (3)
    	tan = arcpy.gp.Tan_sa(div, Tan_demxpi_b1)
    	effort = arcpy.gp.Divide_sa(tan, "0.017455065", effort) 

        # Find sum of all penalties for the Naismith Rule
        # Process: Greater Than Equal, Times (13), Times (12), Times (16), Times (9)
        rise_of_aoi = arcpy.gp.Times_sa(tan, "21.58828612", rise_of_all_aoi)
        penalties_more_12 = arcpy.gp.Times_sa(rise_of_aoi, arcpy.gp.Times_sa("6", arcpy.gp.GreaterThanEqual_sa
                                                                             (dem_n_bog_slp, "12", Greaterthan12), ms_more12), nais_penalties_more12)
        penalties_five_to_twelve = arcpy.gp.Times_sa(five_to_twelve, rise_of_aoi, nais_penalties_5to12)
        walk_dist = arcpy.gp.RasterCalculator_sa("\"%nais_penalties_5to12%\" + \"%nais_penalties_more12%\" + 15.12", naismith_rule)

    elif method == "Tobler":
        # Walking Distance = (abs(Div + 0.05)*input raster)exp * stride per sec
        # Process: Plus (4), Abs, Times (5), Exp, Times (6)
        walk_dist = arcpy.gp.Times_sa(arcpy.gp.Exp_sa(arcpy.gp.Times_sa(arcpy.gp.Abs_sa
                                                                        (arcpy.gp.Plus_sa(div, "0.05", Plus_demxpi_1), Abs_Plus_dem1), "-3.5", Times_Abs_Pl1),
                                                      Exp_Times_Ab1), "3", walking_dist)

else:

    method = arcpy.GetParameterAsText(7)
    if method == "Naismith":      
        greater_than_five = arcpy.gp.GreaterThanEqual_sa(dem_n_bog_slp, "5", Output_raster__3_)
        less_than_twelve = arcpy.gp.LessThan_sa(dem_n_bog_slp, "12", LessThan12)
        five_to_twelve = arcpy.gp.Times_sa(arcpy.gp.Times_sa(greater_than_five, less_than_twelve, mor5less12slp), "1.998", v5to12_penalty)
	
	# tan(dem_n_bog_slp*Pi/180)
    	# Process: Times (3), Divide (2), Tan
    	div = arcpy.gp.Divide_sa(arcpy.gp.Times_sa(dem_n_bog_slp, "3.141592654", dem_x_pi), "180", demxpi_by_180)

    	# Effort = tan/0.017455065
    	# Process: Divide (3)
    	tan = arcpy.gp.Tan_sa(div, Tan_demxpi_b1)
    	effort = arcpy.gp.Divide_sa(tan, "0.017455065", effort) 


        # Find sum of all penalties for the Naismith Rule
        # Process: Greater Than Equal, Times (13), Times (12), Times (16), Times (9)
        rise_of_aoi = arcpy.gp.Times_sa(tan, "21.58828612", rise_of_all_aoi)
        penalties_more_12 = arcpy.gp.Times_sa(rise_of_aoi, arcpy.gp.Times_sa("6", arcpy.gp.GreaterThanEqual_sa(dem_n_bog_slp, "12", Greaterthan12), ms_more12), nais_penalties_more12)
        penalties_five_to_twelve = arcpy.gp.Times_sa(five_to_twelve, rise_of_aoi, nais_penalties_5to12)
        walk_dist = arcpy.gp.RasterCalculator_sa("\"%nais_penalties_5to12%\" + \"%nais_penalties_more12%\" + 15.12", naismith_rule)

    elif method == "Tobler":
        # Walking Distance = (abs(Div + 0.05)*input raster)exp * stride per sec
        # Process: Plus (4), Abs, Times (5), Exp, Times (6)
        walk_dist = arcpy.gp.Times_sa(arcpy.gp.Exp_sa(arcpy.gp.Times_sa(arcpy.gp.Abs_sa(arcpy.gp.Plus_sa(div, "0.05", Plus_demxpi_1), Abs_Plus_dem1), "-3.5", Times_Abs_Pl1), Exp_Times_Ab1), "3", walking_dist)

    # tan(dem_n_bog_slp*Pi/180)
    # Process: Times (3), Divide (2), Tan
    div = arcpy.gp.Divide_sa(arcpy.gp.Times_sa(dem_n_bog_slp, "3.141592654", dem_x_pi), "180", demxpi_by_180)

    # Effort = tan/0.017455065
    # Process: Divide (3)
    tan = arcpy.gp.Tan_sa(div, Tan_demxpi_b1)
    effort = arcpy.gp.Divide_sa(tan, "0.017455065", effort)
    terra_cost_rev_var = arcpy.gp.WeightedSum_sa("C:\\aquaterra.gdb\\effort VALUE 1-weight;C:\\aquaterra.gdb\\walking_dist VALUE weight;C:\\aquaterra.gdb\\naismith_rule VALUE 0", terra_cost_rev)
    


#Provide Wind Speed Raster
wind_speed = arcpy.GetParameterAsText(2)
if wind_speed == "#" or not wind_speed:
    wind_speed = "0" # provide a default value if unspecified

wind_measurement = arcpy.GetParameterAsText(4)
if wind_measurement == "#" or not wind_measurement:
    wind_measurement = True # provide a default value if unspecified

#Ask user for the gridcell size
gridcell_size = arcpy.GetParameterAsText(5)

if wind_measurement == True:
    arcpy.gp.Times_sa(windata_mask_n_, "0.514444444444444", wind_knots2ms_n_)  
wind_speed = arcpy.gp.Divide_sa(gridcell_size, wind_knots2ms_n_, ovrwindeffrt)

