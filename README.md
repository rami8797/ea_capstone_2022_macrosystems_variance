# macrosystems_spectral_variance

### Project Description
The purpose of this repository is to document the progress of my Earth Analytics capstone project as well as to safely store related data and items. The project goal is to calculate the variance of hyperspectral imagery between National Ecological Observatory Network (NEON) sites located throughout the western part of the United States. This will be used to support a larger project in which vegetation on the ground will be identified via remote sensing data depending on the wavelengths absorbed/reflected by the vegetation. Others may wish to use the workflow presented in this repository to perform a similar analysis for other NEON sites located outside of the western United States.

### Project Background
Using remote sensing to identify plants for the purposes above is actively being explored.

1. [Multispectral Approach for Identifying Invasive Plant Species Based on Flowering Phenology Characteristics](https://www.mdpi.com/2072-4292/11/8/953/htm)
2. [No place to hide: Rare plant detection through remote sensing](https://onlinelibrary.wiley.com/doi/full/10.1111/ddi.13244) 

While identifying plants using remote sensing is being researched, there are great [advantages to conducting this type of work at long-term ecological monitoring sites](https://www.sciencedirect.com/science/article/pii/S0048969717321095#:~:text=Long%2Dterm%20ecological%20research%20can,trends%20(M%C3%BCller%20et%20al.%2C) such as NEON. For example, due to available historical data, the impacts of extreme or rare events on plant communities could be determined, and both long-term and short-term trends can be monitored and explored over time. 

### Workflow
Follow the instructions [here](https://www.earthdatascience.org/workshops/setup-earth-analytics-python/) to set up your python, git, and bash environment on your computer.

#### Workflow Visualization

![Project Workflow Diagram](/images/ea_capstone_22_workflow.png)

#### Required Packages
1. os
2. pandas
3. earthpy
4. geopandas
5. matplotlib (and pyplot module)
6. numpy
7. earthpy (and plot module)
8. h5py
9. json
10. requests
11. shapely (and geometry module and box function)
12. joypy (and joyplot module)

#### Running the Workflow
Begin by running the macrosystems_blog.ipynb file located in notebooks/class directory of this repository. This will get you up to speed on the current status of the project as well as prompt you to download an h5 file that will be used in the other notebooks contained within the repository.

### Example Usage
Data formats needed to apply this workflow are csv and h5 files. The csv file needed is located in the data directory and the h5 file used throughout the repository can be downloaded by running the macrosystems_blog.ipynb file located in notebooks/class directory. To find similar data that could be used in this workflow, refer to the api_exploration_data_url_retrieval.ipynb file located in the notebooks/ty directory. That notebook will take you through how to find other h5 files that are managed by NEON. 

#### Using the .csv File in this Repository
An example of how to use the csv file located in this repository is below. NOTE: Make sure to set the path to the csv file prior to running this code.

```python
import pandas as pd
import geopandas as gpd

# Read in metadata
metadata_df = pd.read_csv(metadata_path)

# Convert pandas dataframe to a geopandas dataframe
metadata_gdf = gpd.GeoDataFrame(metadata_df,
                    geometry=gpd.points_from_xy(metadata_df.field_longitude,
                                                metadata_df.field_latitude))

# Assign crs to metadata_gpd
metadata_assigned_crs = metadata_gdf.set_crs(epsg=4326)
```

### Other Files in this Repository
1. The RedEdge-MX-Dual-Camera-Whitepaper.pdf file located in the documents directory is documentation on the drone-equipped spectral sensor used during sampling at NEON sites. 
2. The images directory contains images that have been used in reports and presentations related to this project.
3. The notebooks directory contains two subdirectories, class and ty. The class subdirectory contains notebooks that are strictly for class purposes. In other words, they have been submitted for grading. The ty subdirectory contains notebooks that I created to work through tasks that were given to me by my project mentor, Dr. Ty Tuff and have advanced this project. I created a filtering function to identify NEON sites that meet a certain criteria in filtering-metadata-machinery-rlm.ipynb that uses the file in the data directory, and in create_niwo_h5_waveform.ipynb, I plot the waveform of one h5 file and begin to extract and analyze the bands outlined in the RedEdge-MX-Dual-Camera-Whitepaper.pdf file located in the documents directory.
4. The environment.yml file is included in this repository so that users may update their base environment or create an environment using it. It contains the h5py and joypy packages that are not included in the environment used when following the installation instructions above, however they are needed to run the code in this repository.

### Potential Limitations
The h5 file used in this repository is very large, and users may experience long wait times for code to run or be unable to download the file.