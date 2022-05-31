# Import required packages
import pandas as pd
import geopandas as gpd
from shapely.geometry import box
import h5py

# Create function that will do everything above and spit out a list of site ids
def get_site_ids(data_path, bounds, column1, column_info1, column2, column_info2):
    """Open NEON metadata file, turn it into a geopandas dataframe, and filter 
    the dataframe to only contain sites within a provided location.

    Parameters
    -----------
    data_path: string 
        A path to the csv to be opened.
    bounds: tuple
        A tuple with the order of minx, miny, maxx, maxy
    column1: pandas.Series
        A column within the dataframe that will be used to filter sites
    column_info1: string
        A string that specifies what information within column 1 you want to 
        use for filtering
    column2: pandas.Series
        A column within the dataframe that will be used to filter sites
    column_info2: string
        A string that specifies what information within column 2 you want to 
        use for filtering
     

    Returns
    -----------
    id_list : list
        A list of site ids

    """

    if os.path.basename(os.path.normpath(metadata_path)) == "NEON_Field_Site_Metadata_20220224.csv":

        # Open csv file
        metadata_df = pd.read_csv(data_path)
        
    else:
        print("Set your directory path to NEON_Field_Site_Metadata_20220224.csv before continuing.")

    # Convert pandas dataframe to a geopandas dataframe
    metadata_gpd = gpd.GeoDataFrame(metadata_df,
                                geometry=gpd.points_from_xy(metadata_df.field_longitude,
                                                            metadata_df.field_latitude))

    # Assign crs to metadata_gpd
    metadata_assigned_crs = metadata_gpd.set_crs(epsg=4326)
    

    # Filter your data with a box to only using the cx method
    filter_box = box(bounds[0], bounds[1], bounds[2], bounds[3])

    # Filter
    spatially_filtered_sites = metadata_assigned_crs.cx[filter_box.bounds[0]:filter_box.bounds[2], 
                                       filter_box.bounds[1]:filter_box.bounds[3]]

    if column1 in spatially_filtered_sites:
    
        # Filter by column1
        column1_gdf = spatially_filtered_sites[(
        spatially_filtered_sites[column1].str.contains(column_info1))]
    
    else:
        print("Oops, looks like the column you selected isn't in the dataframe.")
    
    if column2 in spatially_filtered_sites:
    
        # Filter by column2
        column2_gdf = column1_gdf[(
        column1_gdf[column2].str.contains(column_info2))]
    
    else:
        print("Oops, looks like the column you selected isn't in the dataframe.")
    
    # Create a list of site ids (could be used in a loop for later processing)
    site_ids = column2_gdf["field_site_id"].tolist()

    return site_ids

# Create function to open h5 file, clean reflectance arrays, and expand 
# dataframe
def clean_h5_refl_df(file_path):
    """Reads in a NEON AOP reflectance h5 file and returns a pandas dataframe
        containing one cleaned reflectance array (no data value and scale 
        factor applied) value per row matched to the corresponding wavelength 
        along with a site column.

    --------
    Parameters
    file_path: string
        Full or relative path and name of reflectance h5 file
    --------
    Returns 
    --------
    df_explode: pandas DataFrame
        DataFrame containing clean reflectance array values matched to their
        corresponding wavelengths and a site column.
    """
    
    # Read in file
    h5 = h5py.File(file_path, "r")
    
    # Get the site name
    file_attrs_string = str(list(h5.items()))
    file_attrs_string_split = file_attrs_string.split("'")
    sitename = file_attrs_string_split[1]

    # Access the reflectance "folder"
    site_refl = h5["NIWO"]["Reflectance"]
    
    # Assign reflectance array to a variable
    site_refl_array = site_refl["Reflectance_Data"]

    # Assgign reflectance values to a variable
    refl_raw = site_refl["Reflectance_Data"][:]
    
    # Define the wavelengths variable
    wavelengths = site_refl["Metadata"]["Spectral_Data"]["Wavelength"]
    
    # Extract no data value & scale factor
    scale_factor = site_refl_array.attrs["Scale_Factor"]
    no_data_value = site_refl_array.attrs["Data_Ignore_Value"]
    
    # Apply no data value
    refl_clean = refl_raw.astype(float)
    arr_size = refl_clean.shape
    if no_data_value in refl_raw:
        print("% No Data: ",np.round(np.count_nonzero(refl_clean==metadata["data ignore value"])*100/(arr_size[0]*arr_size[1]*arr_size[2]),1))
        nodata_ind = np.where(refl_clean==no_data_value)
        refl_clean[nodata_ind]=np.nan
    
    # Apply scale factor
    refl_array = refl_clean/scale_factor
    
    try:
        # Loop through reflectance array again to grab whole arrays
        # Create empty list
        full_refl_array = []
        for band in np.arange(refl_array.shape[2]):
            refl_band = refl_array[:,:,band]
            full_refl_array.append(refl_band)
    except DimensionError:
        print("Oops, looks like the array within the file you're trying to use isn't of the correct dimensions.")
        
    # Make dataframe with wavelength, full reflectance array, and site column
    refl_array_df = pd.DataFrame()
    refl_array_df["wavelength"] = wavelengths
    refl_array_df["reflectance"] = full_refl_array
    refl_array_df["site"] = sitename
    
    # Expand reflectance arrays so that there is one reflectance value from 
    # the array per row
    df_explode = (refl_array_df.explode("reflectance")).explode("reflectance")
    
    return df_explode