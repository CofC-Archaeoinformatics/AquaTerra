import arcpy
from arcpy import env

arcpy.CheckOutExtension("spatial")

class Toolbox(object):
    def __init__(self):
        """Define the toolbox (the name of the toolbox is the name of the
        .pyt file)."""
        self.label = "AquaTerra"
        self.alias = "aquaterra"

        # List of tool classes associated with this toolbox
        self.tools = [Tool]


class Tool(object):
    def __init__(self):
        """Define the tool (tool name is the name of the class)."""
        self.label = "Tool"
        self.description = ""
        self.canRunInBackground = False

    def getParameterInfo(self):
        """Define parameter definitions"""        
        # Point of Origin
        param0 = arcpy.Parameter(
            displayName="Point of Origin",
            name="point_of_origin",
            datatype="DEFeatureClass",
            parameterType="Required",
            direction="Input")
        
        # Point of Arrival
        param1 = arcpy.Parameter(
            displayName="Point of Arrival",
            name="point_of_arival",
            datatype="DEFeatureClass",
            parameterType="Required",
            direction="Input")
        
        # Isthmia
        param2 = arcpy.Parameter(
            displayName="Isthmia",
            name="isthmia",
            datatype="DEFeatureClass",
            parameterType="Required",
            direction="Input")
        
        # Epidavros
        param3 = arcpy.Parameter(
            displayName="Epidavros",
            name="epidavros",
            datatype="DEFeatureClass",
            parameterType="Required",
            direction="Input")
        
        # Korphos
        param4 = arcpy.Parameter(
            displayName="Korphos",
            name="korphos",
            datatype="DEFeatureClass",
            parameterType="Required",
            direction="Input")
        
        # DEM of AOI
        param5 = arcpy.Parameter(
            displayName="DEM of AOI",
            name="aoidem",
            datatype="DERasterDataset",
            parameterType="Required",
            direction="Input")
        
        # Wind Raster
        param6 = arcpy.Parameter(
            displayName="Wind Raster",
            name="wind_map",
            datatype="DERasterDataset",
            parameterType="Required",
            direction="Input")
        
        # Lowland Feature Augment Factor
        param7 = arcpy.Parameter(
            displayName="Lowland Feature Augment Factor",
            name="lowland_aug_factor",
            datatype="GPLong",
            parameterType="Required",
            direction="Input")
        param7.value = 10
            
        # Effort / Speed
        param8 = arcpy.Parameter(
            displayName="Ratio of Ease v. Speed (between 0 and 1)",
            name="ease_v_speed",
            datatype="GPDouble",
            parameterType="Required",
            direction="Input")
        param8.value = 0.7
        
        # Maximum Effect Distance
        param9 = arcpy.Parameter(
            displayName="Maximum Effect Distance (in hours)",
            name="max_effect_dist",
            datatype="GPLong",
            parameterType="Required",
            direction="Input")
        param9.value = 2
        
        # TODO: Read previous input from recent_config file
        
        params = [param0, param1, param2, param3, param4, param5, param6, param7, param8, param9]
        
        return params

    def isLicensed(self):
        """Set whether tool is licensed to execute."""
        return True

    def updateParameters(self, parameters):
        """Modify the values and properties of parameters before internal
        validation is performed.  This method is called whenever a parameter
        has been changed."""
        return

    def updateMessages(self, parameters):
        """Modify the messages created by internal validation for each tool
        parameter.  This method is called after internal validation."""
        return

    def execute(self, parameters, messages):
        """The source code of the tool."""        
        arcpy.env.overwriteOutput = True
        
        point_of_origin = parameters[0].valueAsText
        point_of_arrival = parameters[1].valueAsText
        isthmia = parameters[2].valueAsText   # Needs to be replaced with multi-input 
        epidavros = parameters[3].valueAsText # Needs to be replaced with multi-input 
        korphos = parameters[4].valueAsText   # Needs to be replaced with multi-input 
        aoidem = parameters[5].valueAsText
        wind_map = parameters[6].valueAsText
        aug_factor = parameters[7].valueAsText
        cost_weight = parameters[8].valueAsText
        max_effect_dist = parameters[9].valueAsText
        
        # TODO: Write current parameter values to recent_config file
        
        # Check if workspace is set (if not, exit)
        if(arcpy.env.workspace == None):
            arcpy.AddError("\narc.env.workspace (the current workspace) is not set.\nIf working in Catalog, please set the current workspace in \"Environments...\" to continue\n")
            raise SystemExit
        wspace = arcpy.env.workspace
        
        # Start Logic
        # Copy raster        
        aoidem_copy = wspace + "\\aoidem_copy"
        arcpy.AddMessage("Copying Raster...")
        arcpy.CopyRaster_management(aoidem, aoidem_copy)
        
        # Slope
        slope = wspace + "\\slope"
        arcpy.AddMessage("Calculating Slope...")
        arcpy.gp.Slope_sa(aoidem_copy, slope, "DEGREE", "1")
        
        # Flow Accumulation
        flow_acc = wspace + "\\flow_acc"
        arcpy.AddMessage("Accumulating Flow...")
        arcpy.gp.FlowAccumulation_sa(aoidem_copy, flow_acc, "", "FLOAT")
        
        # Add 1 to flow_acc and slope
        slope_plus = wspace + "\\slope_plus"
        arcpy.AddMessage("Incrementing Slope...")
        arcpy.gp.Plus_sa(slope, 1, slope_plus)
        
        flow_acc_plus = wspace + "\\flow_acc_plus"
        arcpy.AddMessage("Incrementing Flow Accumulation...")
        arcpy.gp.Plus_sa(flow_acc, 1, flow_acc_plus)
        
        # Divide flow_acc_plus by slope_plus
        flow_div_slope = wspace + "\\flow_div_slope"
        arcpy.AddMessage("Dividing Flow Accumulation by Slope...")
        arcpy.gp.Divide_sa(flow_acc_plus, slope_plus, flow_div_slope)
        
        # Calculate Moisture Index
        moist_index = wspace + "\\moist_index"
        arcpy.AddMessage("Calculating Moisture Index...")
        arcpy.gp.Ln_sa(flow_div_slope, moist_index)
        
        # Derive land_mask
        land_mask = wspace + "\\land_mask"
        arcpy.AddMessage("Deriving Land Mask...")
        arcpy.gp.GreaterThan_sa(aoidem_copy, 0, land_mask)
        
        # Calculate Greater Moisture Index
        great_moist_index = wspace + "\\great_moist_index"
        arcpy.AddMessage("Calculating Greater Moisture Index...")
        arcpy.gp.GreaterThan_sa(moist_index, 0, great_moist_index)
        
        # Compute Boggy Bits
        boggy_bits = wspace + "\\boggy_bits"
        arcpy.AddMessage("Computing the Boggy Bits...")
        arcpy.gp.Times_sa(great_moist_index, moist_index, boggy_bits)
        
        # Augment Boggy Bits
        aug_boggy_bits = wspace + "\\aug_boggy_bits"
        arcpy.AddMessage("Augmenting the Boggy Bits...")
        arcpy.gp.Times_sa(boggy_bits, aug_factor, aug_boggy_bits)
        
        # Add the Augmented Boggy Bits to the DEM of AOI
        dem_n_bog = wspace + "\\dem_n_bog"
        arcpy.AddMessage("Adding the Boggy bits to the DEM...")
        arcpy.gp.Plus_sa(aug_boggy_bits, aoidem_copy, dem_n_bog)
        
        # Get the slope of the DEM and Bog
        slope_dem_n_bog = wspace + "\\slope_dem_n_bog"
        arcpy.AddMessage("Recalculating Slope...")
        arcpy.gp.Slope_sa(dem_n_bog, slope_dem_n_bog, "DEGREE", "1")
        
        # Copy wind map
        wind_map_copy = wspace + "\\wind_map_copy"
        arcpy.AddMessage("Copying Wind Map...")
        arcpy.CopyRaster_management(wind_map, wind_map_copy)
        
        # Multiply DEM and Bog Slope by PI
        pi_slope = wspace + "\\pi_slope"
        arcpy.AddMessage("Multiplying Slope by π...")
        arcpy.gp.Times_sa(slope, math.pi, pi_slope)
        
        # Extract Wind Data
        wind_data = wspace + "\\wind_data"
        arcpy.AddMessage("Extracting Wind Data...")
        arcpy.gp.ExtractByMask_sa(wind_map_copy, aoidem_copy, wind_data)
        
        # Divide slope by 180
        rad_slope = wspace + "\\rad_slope"
        arcpy.AddMessage("Dividing Slope by 180...")
        arcpy.gp.Divide_sa(pi_slope, 180, rad_slope)
        
        # Check slope >= 5
        greater_slope = wspace + "\\greater_slope"
        arcpy.AddMessage("Checking Slope >= 5...")
        arcpy.gp.GreaterThanEqual_sa(slope, 5, greater_slope)
        
        # Check slope < 12
        less_slope = wspace + "\\less_slope"
        arcpy.AddMessage("Checking Slope < 12...")
        arcpy.gp.LessThan_sa(slope, 12, less_slope)
        
        # Check slope >= 12
        greater_slope = wspace + "\\greater_slope"
        arcpy.AddMessage("Checking Slope >= 12...")
        arcpy.gp.GreaterThanEqual_sa(slope, 5, greater_slope)
        
        # Convert Knots to m/s (.514 is the conversion rate)
        wind_data_ms = wspace + "\\wind_data_ms"
        arcpy.AddMessage("Converting Knots to Meters per Seconds")
        arcpy.gp.Times_sa(wind_data, 0.514444444444444, wind_data_ms)
        
        # Compute tangent of slope
        tan_slope = wspace + "\\tan_slope"
        arcpy.AddMessage("Computing Tangent of Slope...")
        arcpy.gp.Tan_sa(slope, tan_slope)
        
        # Multiply slope >= 5 by slope < 12
        more_less_slope = wspace + "\\more_less_slope"
        arcpy.AddMessage("Multiplying results together...")
        arcpy.gp.Times_sa(greater_slope, less_slope, more_less_slope)
        
        # Multiply slope >= 12 by 6 (number origin)
        ms_more_slope = wspace + "\\ms_more_slope"
        arcpy.AddMessage("Multiplying Slope >= 12 by 6...")
        arcpy.gp.Times_sa(6, greater_slope, ms_more_slope)
        
        # Divide Wind Data in m/s by 21.58828612 (number origin)
        over_wind_effort = wspace + "\\over_wind_effort"
        arcpy.AddMessage("Dividing Wind Data by a number...")
        arcpy.gp.Divide_sa(21.58828612, wind_data_ms, over_wind_effort)
        
        # Divide tan_slope by 0.017455065 (number origin) (Convert radians to degrees)
        effort = wspace + "\\effort"
        arcpy.AddMessage("Computing Effort...")
        arcpy.gp.Divide_sa(tan_slope, 0.017455065, effort)
        
        # Multiply tan_slope by 21.58828612 (Raster resolution; needs dynamicizing)
        rise_of_aoi = wspace + "\\rise_of_aoi"
        arcpy.AddMessage("Multiplying Slope by a number...")
        arcpy.gp.Times_sa(tan_slope, 21.58828612, rise_of_aoi)
        
        # Calculate 5-12 penalty with 1.998 (number origin) from Naismith's Rule
        penalty_5_12 = wspace + "\\penalty_5_12"
        arcpy.AddMessage("Calculating 5-12 penalty...")
        arcpy.gp.Times_sa(more_less_slope, 1.998, penalty_5_12)
        
        # Multiply rise of aoi by 5-12 penalty
        naismith_penalty_5_12 = wspace + "\\naismith_penalty_5_12_5_12"
        arcpy.AddMessage("Calculating Naismith Penalties 5-12...")
        arcpy.gp.Times_sa(penalty_5_12, rise_of_aoi, naismith_penalty_5_12)
        
        # Multiply rise of aoi by >=12 penalty
        naismith_penalty_12 = wspace + "\\naismith_penalty_12"
        arcpy.AddMessage("Calculating Naismith Penalties >=12...")
        arcpy.gp.Times_sa(rise_of_aoi, ms_more_slope, naismith_penalty_12)
        
        # Calculate Naismith's Rule (number origin)
        naismith_rule = wspace + "\\naismith_rule"
        full = 'OutRas = "{0}" + "{1}" + 15.12'.format(naismith_penalty_5_12, naismith_penalty_12)
        arcpy.AddMessage("Calculating Naismith's Rule")
        arcpy.gp.RasterCalculator_sa(full, naismith_rule)
        
        # Mask Naismith's Rule with land mask
        naismith_masked = wspace + "\\naismith_masked"
        arcpy.AddMessage("Masking Naismith's Rule Calculation...")
        arcpy.gp.Times_sa(naismith_rule, land_mask, naismith_masked)
        
        # Calculate Naismith with Wind
        naismith_wind_cost = wspace + "\\naismith_wind_cost"
        full = 'OutRas = Con("{0}" > 0, "{0}", "{1}")'.format(naismith_masked, over_wind_effort)
        arcpy.AddMessage("Calculating Naismith's Rule with Wind Cost...")
        arcpy.gp.RasterCalculator_sa(full, naismith_wind_cost)
        
        
        
        # Calculate Detractors
        # Calculate Cost Distance for Isthmia (Refactoring Needed)
        costdist_isthmia = wspace + "\\costdist_isthmia"
        backlink_isthmia = wspace + "\\backlink_isthmia"
        arcpy.AddMessage("Calculating Cost Distance for Isthmia...")
        arcpy.gp.CostDistance_sa(isthmia, naismith_wind_cost, costdist_isthmia, "", backlink_isthmia)
        
        # Level Cost Distance for Isthmia to 0 for anything less than the max effect distance
        costdist_isthmia_zero = wspace + "\\costdist_isthmia_zero"
        arcpy.AddMessage("Leveling Cost Distance for Isthmia to 0 for anything less than the max effect distance...")
        full = 'OutRas = Con("{0}" < float({1} * 3600 * 21.58828612), "{0}", 0)'.format(costdist_isthmia, max_effect_dist)
        arcpy.gp.RasterCalculator_sa(full, costdist_isthmia_zero)
        
        # Calculate Detract Percentage
        detract_percent_isthmia = wspace + "\\detract_percent_isthmia"
        arcpy.AddMessage("Calculating Detract Percentage for Isthmia...")
        full = 'OutRas = Con("{0}" > 0, (1 - ("{0}" / ({1} * 3600 * 21.58828612))), 0)'.format(costdist_isthmia_zero, max_effect_dist)
        arcpy.gp.RasterCalculator_sa(full, detract_percent_isthmia)
        
        # Adjust Detract Percentage by Cost Weight factor
        costdist_detract_isthmia = wspace + "\\costdist_detract_isthmia"
        arcpy.AddMessage("Adjusting Detract Percentage by Cost Weight factor for Isthmia...")
        full = 'OutRas = 1 + (float("{0}") * "{1}")'.format(cost_weight, detract_percent_isthmia)
        arcpy.gp.RasterCalculator_sa(full, costdist_detract_isthmia)
        
        # Combine detractors into a single raster
        detractor_mosaic = wspace + "\\detractor_mosaic"
		arcpy.AddMessage("Combine detractors into a single raster for Isthmia...")
        arcpy.MosaicToNewRaster_management(costdist_detract_isthmia, wspace, "detractor_mosaic", "PROJCS['WGS_1984_Cylindrical_Equal_Area',GEOGCS['GCS_WGS_1984',DATUM['D_WGS_1984',SPHEROID['WGS_1984',6378137.0,298.257223563]],PRIMEM['Greenwich',0.0],UNIT['Degree',0.0174532925199433]],PROJECTION['Cylindrical_Equal_Area'],PARAMETER['False_Easting',0.0],PARAMETER['False_Northing',0.0],PARAMETER['Central_Meridian',0.0],PARAMETER['Standard_Parallel_1',0.0],UNIT['Meter',1.0]]", "32_BIT_FLOAT", "", "1", "MAXIMUM", "FIRST")
        
        
        
        # Calculate Attractors
        # Calculate Cost Distance for Epidavros
        costdist_epidavros = wspace + "\\costdist_epidavros"
        backlink_epidavros = wspace + "\\backlink_epidavros"
        arcpy.AddMessage("Calculating Cost Distance for Epidavros...")
        arcpy.gp.CostDistance_sa(epidavros, naismith_wind_cost, costdist_epidavros, "", backlink_epidavros)
        
        # Level Cost Distance for Epidavros to 0 for anything less than the max effect distance
        costdist_epidavros_zero = wspace + "\\costdist_epidavros_zero"
        arcpy.AddMessage("Leveling Cost Distance for Epidavros to 0 for anything less than the max effect distance...")
        full = 'OutRas = Con("{0}" < float({1} * 3600 * 21.58828612), "{0}", 0)'.format(costdist_epidavros, max_effect_dist)
        arcpy.gp.RasterCalculator_sa(full, costdist_epidavros_zero)
        
        # Calculate Attract Percentage
        attract_percent_epidavros = wspace + "\\attract_percent_epidavros"
        arcpy.AddMessage("Calculating Attract Percentage for Epidavros...")
        full = 'OutRas = Con("{0}" > 0, ("{0}" / ({1} * 3600 * 21.58828612)), 0)'.format(costdist_epidavros_zero, max_effect_dist)
        arcpy.gp.RasterCalculator_sa(full, attract_percent_epidavros)
        
        # Adjust Attract Percentage by Cost Weight factor
        costdist_attract_epidavros_weighted = wspace + "\\costdist_attract_epidavros_weighted"
        arcpy.AddMessage("Adjusting Attract Percentage by Cost Weight factor for Epidavros...")
        arcpy.gp.Times_sa(cost_weight, attract_percent_epidavros, costdist_attract_epidavros_weighted)
        
        # Calculate Onesies
        costdist_attract_epidavros = wspace + "\\costdist_attract_epidavros"
        arcpy.AddMessage("Calculating Onesies for Epidavros...")
        full = 'OutRas = Con("{0}" < 0.0001, 1, "{0}")'.format(costdist_attract_epidavros_weighted)
        arcpy.gp.RasterCalculator_sa(full, costdist_attract_epidavros)
        
        # Calculate Cost Distance for Korphos
        costdist_korphos = wspace + "\\costdist_korphos"
        backlink_korphos = wspace + "\\backlink_korphos"
        arcpy.AddMessage("Calculating Cost Distance for Korphos...")
        arcpy.gp.CostDistance_sa(korphos, naismith_wind_cost, costdist_korphos, "", backlink_korphos)
        
        # Level Cost Distance for Korphos to 0 for anything less than the max effect distance
        costdist_korphos_zero = wspace + "\\costdist_korphos_zero"
        arcpy.AddMessage("Leveling Cost Distance for Korphos to 0 for anything less than the max effect distance...")
        full = 'OutRas = Con("{0}" < float({1} * 3600 * 21.58828612), "{0}", 0)'.format(costdist_korphos, max_effect_dist)
        arcpy.gp.RasterCalculator_sa(full, costdist_korphos_zero)
        
        # Calculate Attract Percentage
        attract_percent_korphos = wspace + "\\attract_percent_korphos"
        arcpy.AddMessage("Calculating Attract Percentage for Korphos...")
        full = 'OutRas = Con("{0}" > 0, ("{0}" / ({1} * 3600 * 21.58828612)), 0)'.format(costdist_korphos_zero, max_effect_dist)
        arcpy.gp.RasterCalculator_sa(full, attract_percent_korphos)
        
        # Adjust Attract Percentage by Cost Weight factor
        costdist_attract_korphos_weighted = wspace + "\\costdist_attract_korphos_weighted"
        arcpy.AddMessage("Adjusting Attract Percentage by Cost Weight factor for Korphos...")
        arcpy.gp.Times_sa(cost_weight, attract_percent_korphos, costdist_attract_korphos_weighted)
        
        # Calculate Onesies
        costdist_attract_korphos = wspace + "\\costdist_attract_korphos"
        arcpy.AddMessage("Calculating Onesies for Korphos...")
        full = 'OutRas = Con("{0}" < 0.0001, 1, "{0}")'.format(costdist_attract_korphos_weighted)
        arcpy.gp.RasterCalculator_sa(full, costdist_attract_korphos)
        
        # Combine Attractors into a single raster
        attractor_mosaic = wspace + "\\attractor_mosaic"
		arcpy.AddMessage("Combining attractors into a single raster for Epidavros and Korphos...")
        arcpy.MosaicToNewRaster_management(costdist_attract_epidavros + ";" + costdist_attract_korphos, wspace, "attractor_mosaic", "PROJCS['WGS_1984_Cylindrical_Equal_Area',GEOGCS['GCS_WGS_1984',DATUM['D_WGS_1984',SPHEROID['WGS_1984',6378137.0,298.257223563]],PRIMEM['Greenwich',0.0],UNIT['Degree',0.0174532925199433]],PROJECTION['Cylindrical_Equal_Area'],PARAMETER['False_Easting',0.0],PARAMETER['False_Northing',0.0],PARAMETER['Central_Meridian',0.0],PARAMETER['Standard_Parallel_1',0.0],UNIT['Meter',1.0]]", "32_BIT_FLOAT", "", "1", "MINIMUM", "FIRST")
        
        
        
        # Level Attractors
        attractor_zero = wspace + "\\attractor_zero"
        arcpy.AddMessage("Leveling Attractors...")
        full = 'OutRas = Con("{0}" == 1, 0, "{0}")'.format(attractor_mosaic)
        arcpy.gp.RasterCalculator_sa(full, attractor_zero)
        
        
        
        # Level Detractors
        detractor_zero = wspace + "\\detractor_zero"
        arcpy.AddMessage("Leveling Detractors...")
        full = 'OutRas = Con("{0}" == 1, 0, "{0}")'.format(detractor_mosaic)
        arcpy.gp.RasterCalculator_sa(full, detractor_zero)
        
        
        
        # Combine Attractors and Detractors into a single raster
        attract_detract_mosaic = wspace + "\\attract_detract_mosaic"
        arcpy.AddMessage("Combining Attractors and Detractors into a single raster...")
        arcpy.MosaicToNewRaster_management(attractor_zero + ";" + detractor_zero, wspace, "attract_detract_mosaic", "PROJCS['WGS_1984_Cylindrical_Equal_Area',GEOGCS['GCS_WGS_1984',DATUM['D_WGS_1984',SPHEROID['WGS_1984',6378137.0,298.257223563]],PRIMEM['Greenwich',0.0],UNIT['Degree',0.0174532925199433]],PROJECTION['Cylindrical_Equal_Area'],PARAMETER['False_Easting',0.0],PARAMETER['False_Northing',0.0],PARAMETER['Central_Meridian',0.0],PARAMETER['Standard_Parallel_1',0.0],UNIT['Meter',1.0]]", "32_BIT_FLOAT", "", "1", "MINIMUM", "FIRST")
        
        
        
        # Calculate Onesies
        attract_detract = wspace + "\\attract_detract"
        arcpy.AddMessage("Calculating Onesies...")
        full = 'OutRas = Con("{0}" == 0, 1, "{0}")'.format(attract_detract_mosaic)
        arcpy.gp.RasterCalculator_sa(full, attract_detract)
        
        
        
        # Combine Effort and Naismith's Rule
        terra_cost = wspace + "\\terra_cost"
        arcpy.AddMessage("Combining Effort and Naismith's Rule...")
        arcpy.gp.WeightedSum_sa(effort + " VALUE 0.5;" + naismith_rule + " VALUE 0.5", terra_cost)
        
        # Multiply Attract Detract Onesies by Terra Cost
        main_attractdetract_adjustedtimes = wspace + "\\main_attractdetract_adjustedtimes"
        arcpy.AddMessage("Multiplying Attract Detract Onesies by Terra Cost...")
        arcpy.gp.Times_sa(attract_detract, terra_cost, main_attractdetract_adjustedtimes)
		
		# Calculate Water Mask
        land0water1 = wspace + "\\land0water1"
        arcpy.AddMessage("Calculating Water Mask...")
        full = 'OutRas = Con("{0}" == 0, 0, 1)'.format(naismith_masked)
        arcpy.gp.RasterCalculator_sa(full, land0water1)
		
		# Calculate Land Mask
        land1water0 = wspace + "\\land1water0"
        arcpy.AddMessage("Calculating Land Mask...")
        full = 'OutRas = Con("{0}" == 0, 1, 0)'.format(naismith_masked)
        arcpy.gp.RasterCalculator_sa(full, land0water1)
		
		# Multiply Attract Detract Adjusted Times by Land Mask
        main_attractdetract_land = wspace + "\\main_attractdetract_land"
        arcpy.AddMessage("Multiplying Attract Detract Adjusted Times by Land Mask...")
        arcpy.gp.Times_sa(land1water0, main_attractdetract_adjustedtimes, main_attractdetract_land)
        
        # Multiply Over Wind Effort by Water Mask
        main_water = wspace + "\\main_water"
        arcpy.AddMessage("Multiplying Over Wind Effort by Water Mask...")
        arcpy.gp.Times_sa(land0water1, over_wind_effort, main_water)
		
		# Add Main Water to Main Land
        main_attractdetract_adjusted = wspace + "\\main_attractdetract_adjusted"
        arcpy.AddMessage("Adding Main Water to Main Land...")
        arcpy.gp.Plus_sa(main_water, main_attractdetract_land, main_attractdetract_adjusted)
		
		# Calculate Cost Distance for End Point
        costdist_main_attractdetract = wspace + "\\costdist_main_attractdetract"
        backlink_main_attractdetract = wspace + "\\backlink_main_attractdetract"
        arcpy.AddMessage("Calculating Cost Distance for Korphos...")
        arcpy.gp.CostDistance_sa(point_of_arrival, main_attractdetract_adjusted, costdist_main_attractdetract, "", backlink_main_attractdetract)
		
		# Calculate Best Path From Origin to End Point
		costpath_attractdetract = wspace + "\\costpath_attractdetract"
		arcpy.AddMessage("Calculating Best Path From Origin to End Point...")
		arcpy.gp.CostPath_sa(point_of_origin, costdist_main_attractdetract, backlink_main_attractdetract, costpath_attractdetract, "EACH_CELL", "Id")
		
		# Convert Best Path From Raster to Polyline
		costpath_attractdetract_line = wspace + "\\costpath_attractdetract_line"
		arcpy.AddMessage("Converting Best Path From Raster to Polyline...")
		arcpy.RasterToPolyline_conversion(costpath_attractdetract, costpath_attractdetract_line, "ZERO", "0", "SIMPLIFY", "Value")
		
		
        
        return