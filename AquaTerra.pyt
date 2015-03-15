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
        
        # DEM of AOI
        param2 = arcpy.Parameter(
            displayName="DEM of AOI",
            name="aoidem",
            datatype=["DERasterDataset", "DERasterCatalog"],
            parameterType="Required",
            direction="Input")
        
        # Wind Raster
        param3 = arcpy.Parameter(
            displayName="Wind Raster",
            name="wind_map",
            datatype=["DERasterDataset", "DERasterCatalog"],
            parameterType="Required",
            direction="Input")
        
        # Lowland Feature Augment Factor
        param4 = arcpy.Parameter(
            displayName="Lowland Feature Augment Factor",
            name="lowland_aug_factor",
            datatype="GPLong",
            parameterType="Required",
            direction="Input")
        param3.value = 10
            
        # Effort / Speed
        param5 = arcpy.Parameter(
            displayName="Ratio of Ease v. Speed (between 0 and 1)",
            name="ease_v_speed",
            datatype="GPDouble",
            parameterType="Required",
            direction="Input")
        param4.value = 0.7
        
        # Maximum Effect Distance
        param6 = arcpy.Parameter(
            displayName="Maximum Effect Distance (in hours)",
            name="max_effect_dist",
            datatype="GPLong",
            parameterType="Required",
            direction="Input")
        param6.value = 2
        
        # TODO: Read previous input from recent_config file
        
        params = [param0, param1, param2, param3, param4, param5]
        
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
        aoidem = parameters[2].valueAsText
        wind_map = parameters[3].valueAsText
        aug_factor = parameters[4].valueAsText
        cost_weight = parameters[5].valueAsText
        max_effect_dist = parameters[6].valueAsText
        
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
        arcpy.AddMessage("Recalculating Slope...")
        arcpy.gp.Slope_sa(dem_n_bog, slope, "DEGREE", "1")
        
        # 
        
        # Multiply slope by PI
        pi_slope = wspace + "\\pi_slope"
        arcpy.AddMessage("Multiplying Slope by π...")
        arcpy.gp.Times_sa(slope, math.pi, pi_slope)
        
        # Divide slope by 180
        arcpy.AddMessage("Dividing Slope by 180...")
        arcpy.gp.Divide_sa(pi_slope, 180, slope)
        
        # Compute tangent of slope
        tan_slope = wspace + "\\tan_slope"
        arcpy.AddMessage("Computing Tangent of Slope...")
        arcpy.gp.Tan_sa(slope, tan_slope)
        
        # Divide slope by 0.017455065 (Not sure where that number came from)
        effort = wspace + "\\effort"
        arcpy.AddMessage("Computing Effort...")
        arcpy.gp.Divide_sa(tan_slope, 0.017455065, effort)
        
        # Check slope > 
        
        return