# Import required packages
import pandas as pd
import geopandas as gpd
from shapely.geometry import box

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
    site_ids : list
        A list of site ids
    column2_gdf: pandas dataframe
        Dataframe containing metadata for sites that make it past filtering.

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

    return site_ids, column2_gdf

# Import required packages
import requests

def get_data_dates(site_id):
    """Output the dates that there is available NEON data.

    Parameters
    -----------
    site_id: string or list of strings
        A single NEON site ID or a list of NEON site IDs.
     

    Returns
    -----------
    data_dates : list
        A list of dates where NEON data is available for spectrometer orthorectified surface directional reflectance - mosaic data.

    """
    
    # Server URL
    server = "http://data.neonscience.org/api/v0/"
    
    # Assign product code of interest to a variable
    dataset_code = "DP3.30006.001"
    request = requests.get(server+"products/"+dataset_code)
    json = request.json()
    
    # View available months and corresponding API urls, then save desired URL
    data_dates = []
    for site in json["data"]["siteCodes"]:
        if(site["siteCode"] == site_id):
            for month in zip(site["availableMonths"],site["availableDataUrls"]): #Loop through the list of months and URLs
                dates = month[0]
                data_dates.append(dates)
                
    return data_dates

# Import required packages
def get_data_files(sitecode, dates):
    """Get a list of data files available for a date or dates for NEON 
    spectrometer orthorectified surface directional reflectance - mosaic data.

    Parameters
    -----------
    sitecode: string or list of strings
        A single NEON site ID or a list of NEON site IDs.
    dates: string or list of strings 
        A date or list of dates where NEON data is available for spectrometer 
        orthorectified surface directional reflectance - mosaic data.
     
    Returns
    -----------
    file_list : list
        A list of files.

    """
    
    # Server URL
    server = "http://data.neonscience.org/api/v0/"
    
    # Assign product code of interest to a variable
    dataset_code = "DP3.30006.001"

    # Make Request
    request = requests.get(server+"data/"+dataset_code+"/"+sitecode+"/"+dates)
    json = request.json()

    # Put available file names into a list
    file_list = []
    for file in json["data"]["files"]:
        if "h5" in file["name"]:
            file_name = file["name"]
            file_list.append(file_name)
        
    return file_list

# Import required packages
import pandas as pd
import geopandas as gpd
from shapely.geometry import box
import requests
import os

# Create function that will do everything above and spit out a list of site ids
def get_site_dict(data_path, bounds, column1, column_info1, column2, column_info2):
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
    files_dict : dictionary
        A dictionary containing sites that match the input parameters, dates where data is available for those sites, and a list of files that are available for each date.

    """

    if os.path.basename(os.path.normpath(data_path)) == "NEON_Field_Site_Metadata_20220224.csv":

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
    
    # Server URL
    server = "http://data.neonscience.org/api/v0/"
    
    # Assign product code of interest to a variable
    dataset_code = "DP3.30006.001"
    dataset_request = requests.get(server+"products/"+dataset_code)
    dataset_json = dataset_request.json()
    
    # Create a dictionary to put site names and available data dates in
    dates_dict = {}
    for site in site_ids:
        # View available months and corresponding API urls, then save desired URL
        data_dates = []
        for site_name in dataset_json["data"]["siteCodes"]:
            if(site_name["siteCode"] == site):
                for month in zip(site_name["availableMonths"],site_name["availableDataUrls"]): # Loop through the list of months and URLs
                    dates = month[0]
                    data_dates.append(dates)
        dates_dict[site] = data_dates

    
    files_dict = {}
    for key in dates_dict:
        # Put available file names into a list
        file_list = []
        files_dict[key] = {} 
        for a_date in dates_dict[key]:
            # Make Request
            date_request = requests.get(server+"data/"+dataset_code+"/"+key+"/"+a_date)
            date_json = date_request.json()
            for file in date_json["data"]["files"]:
                if "h5" in file["name"]:
                    file_name = file["name"]
                    file_list.append(file_name)
                    files_dict[key][a_date] = file_list
        
    return files_dict

# Import required packages
import numpy as np
import h5py

def clean_h5_refl(file_path):
    """Reads in a NEON AOP reflectance h5 file and returns cleaned reflectance data (scale factor and no data value applied) and metadata.

    --------
    Parameters
    file_path: string
        Full or relative path and name of reflectance h5 file
    --------
    Returns 
    --------
    refl_array:
        Array of reflectance data
    metadata:
        dictionary containing the following metadata:
            epsg: coordinate system code (float)
            spatial extent: spatial extent information
            wavelength: wavelength values (float)
            sitename: Location sitename
    map_info: coordinate system, datum & ellipsoid, pixel dimensions, and origin coordinates (string)
    """
    
    # Read in file
    h5 = h5py.File(file_path, "r")
    
    # Get the site name
    file_attrs_string = str(list(h5.items()))
    file_attrs_string_split = file_attrs_string.split("'")
    sitename = file_attrs_string_split[1]

    # Access the reflectance "folder"
    site_refl = h5[sitename]["Reflectance"]
    
    # Assign reflectance array to a variable
    site_refl_data = site_refl["Reflectance_Data"]

    # Assgign reflectance values to a variable
    refl_raw = site_refl["Reflectance_Data"][()]
    
    # Create dictionary containing relevant metadata information
    metadata = {}
    metadata["wavelength"] = site_refl["Metadata"]["Spectral_Data"]["Wavelength"]
    
    # Define the wavelengths variable
    wavelengths = site_refl["Metadata"]["Spectral_Data"]["Wavelength"]
    
    # Extract no data value & scale factor
    scale_factor = site_refl_data.attrs["Scale_Factor"]
    no_data_value = site_refl_data.attrs["Data_Ignore_Value"]
    
    # Apply no data value
    refl_clean = refl_raw.astype(float)
    arr_size = refl_clean.shape
    if no_data_value in refl_raw:
        print("% No Data: ",np.round(np.count_nonzero(refl_clean==metadata["data ignore value"])*100/(arr_size[0]*arr_size[1]*arr_size[2]),1))
        nodata_ind = np.where(refl_clean==no_data_value)
        refl_clean[nodata_ind]=np.nan
    
    # Apply scale factor
    refl_array = refl_clean/scale_factor
    
    # Extract spatial extent from attributes
    metadata["spatial extent"] = site_refl_data.attrs["Spatial_Extent_meters"]
    
    # Extract projection information
    metadata["projection"] = site_refl["Metadata"]["Coordinate_System"]["Proj4"][()]
    metadata["epsg"] = int(site_refl["Metadata"]["Coordinate_System"]["EPSG Code"][()])
    
    # Extract map information: spatial extent & resolution (pixel size)
    map_info = (site_refl["Metadata"]["Coordinate_System"]["Map_Info"][()])
    
    # Put sitename into metadata
    metadata["sitename"] = sitename
    
    h5.close
    
    return refl_array, metadata, map_info

# Import required packages
import numpy as np

def list_arrays(refl_array):
    """Reads in the reflectance array output from the clean_h5_refl function and returns the arrays in a list.

    --------
    Parameters
    refl_array: numpy.ndarray
         Fixed-size multidimensional container of items of the same type and size, in this case, arrays
    --------
    Returns 
    --------
    array_list: list
        List of arrays
    """    
    
    try:
        # Loop through reflectance array again to grab whole arrays (pull them out of the ndarray)
        # Create empty list
        array_list = []
        for band in np.arange(refl_array.shape[2]):
            refl_band = refl_array[:,:,band]
            array_list.append(refl_band)
    except DimensionError:
        print("Oops, looks like the array within the file you're trying to use isn't of the correct dimensions.")
        
    return array_list

# Import required packages
import pandas as pd

def explode_array_list(array_list, metadata):
    """Reads in a list of reflectance arrays and returns a pandas dataframe
        containing one value per row matched to the corresponding wavelength 
        along with a site column.

    --------
    Parameters
    array_list: list
        List of reflectance arrays
    metadata: metadata dictionary output from clean_h5_refl function
    --------
    Returns 
    --------
    df_explode: pandas DataFrame
        DataFrame containing clean reflectance array values matched to their
        corresponding wavelengths and a site column.
    """
    
    # Make dataframe with wavelength, full reflectance array, and site column
    refl_array_df = pd.DataFrame()
    refl_array_df["wavelength"] = metadata["wavelenghth"]
    refl_array_df["reflectance"] = array_list
    refl_array_df["site"] = metadata["sitename"]
    
    # Expand reflectance arrays so that there is one reflectance value from 
    # the array per row
    df_explode = (refl_array_df.explode("reflectance")).explode("reflectance")
    
    return df_explode

# Import required packages
import h5py
import pandas as pd
import numpy as np

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
    refl_array_df: pandas DataFrame
        DataFrame containing clean reflectance array values matched to the 
        corresponding wavelength and a site column.
    """
    
  # Read in file
    h5 = h5py.File(file_path, "r")
    
    # Get the site name
    file_attrs_string = str(list(h5.items()))
    file_attrs_string_split = file_attrs_string.split("'")
    sitename = file_attrs_string_split[1]

    # Access the reflectance "folder"
    site_refl = h5[sitename]["Reflectance"]
    
    # Assign reflectance array to a variable
    site_refl_data = site_refl["Reflectance_Data"]

    # Assgign reflectance values to a variable
    refl_raw = site_refl["Reflectance_Data"][()]
    
    # Create dictionary containing relevant metadata information
    metadata = {}
    metadata["wavelength"] = site_refl["Metadata"]["Spectral_Data"]["Wavelength"]
    
    # Define the wavelengths variable
    wavelengths = site_refl["Metadata"]["Spectral_Data"]["Wavelength"]
    
    # Extract no data value & scale factor
    scale_factor = site_refl_data.attrs["Scale_Factor"]
    no_data_value = site_refl_data.attrs["Data_Ignore_Value"]
    
    # Apply no data value
    refl_clean = refl_raw.astype(float)
    arr_size = refl_clean.shape
    if no_data_value in refl_raw:
        print("% No Data: ",np.round(np.count_nonzero(refl_clean==metadata["data ignore value"])*100/(arr_size[0]*arr_size[1]*arr_size[2]),1))
        nodata_ind = np.where(refl_clean==no_data_value)
        refl_clean[nodata_ind]=np.nan
    
    # Apply scale factor
    refl_array = refl_clean/scale_factor
    
    # Extract spatial extent from attributes
    metadata["spatial extent"] = site_refl_data.attrs["Spatial_Extent_meters"]
    
    # Extract projection information
    metadata['projection'] = site_refl['Metadata']['Coordinate_System']['Proj4'][()]
    metadata['epsg'] = int(site_refl['Metadata']['Coordinate_System']['EPSG Code'][()])
    
    # Extract map information: spatial extent & resolution (pixel size)
    mapInfo = (site_refl["Metadata"]["Coordinate_System"]["Map_Info"][()])
    
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
    
    return refl_array_df

# Create function to expand dataframe
def select_wavelength(dataframe, wavelength_range):
    """Reads in a NEON AOP reflectance h5 file and returns a pandas dataframe
        containing one cleaned reflectance array (no data value and scale 
        factor applied) value per row matched to the corresponding wavelength 
        along with a site column.

    --------
    Parameters
    dataframe: pandas dataframe
        Pandas dataframe output from clean_h5_refl_df function. Has whole
        reflectance array in a row and associated wavelength.
    wavelength_range: tuple
        Range of wavelengths from the h5 file for which reflectance data will be extracted
    
    --------
    Returns 
    --------
    wavelength_explode_array_df: pandas DataFrame
        DataFrame containing reflectance array values for entered 
        wavelength ranges matched to their corresponding wavelengths and a 
        site column.
    """
    
    # Extract wavelengths in the wavelengt_range and associated reflectance arrays
    wavelength_range_with_refl_array = dataframe[dataframe["wavelength"].between(wavelength_range[0], 
                                                                                         wavelength_range[1])]
    # Expand each arrays so that there is one reflectance value from the array per row
    wavelength_explode_array_df = (wavelength_range_with_refl_array.explode("reflectance")).explode("reflectance")
    
    return wavelength_explode_array_df