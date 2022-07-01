# Hyperspectral Variation at NEON Sites in the Western United States

### Project Description
The purpose of this repository is to document the progress of my Earth Analytics capstone project as well as to safely store related data and items. The project goal is to create a pandas dataframe that will allow users to further determine the spatial and temporal variation of hyperspectral imagery between National Ecological Observatory Network (NEON) located throughout the western part of the United States. This will be used to support a larger project in which vegetation on the ground will be identified via remote sensing data depending on the wavelengths absorbed/reflected by the vegetation. Others may wish to use the workflow presented in this repository to perform a similar analysis for other NEON sites located outside of the western United States.

### Project Background
Using remote sensing to identify plants for the purposes above is actively being explored.

1. [Multispectral Approach for Identifying Invasive Plant Species Based on Flowering Phenology Characteristics](https://www.mdpi.com/2072-4292/11/8/953/htm)
2. [No place to hide: Rare plant detection through remote sensing](https://onlinelibrary.wiley.com/doi/full/10.1111/ddi.13244) 

While identifying plants using remote sensing is being researched, there are great [advantages to conducting this type of work at long-term ecological monitoring sites](https://doi.org/10.1016/j.scitotenv.2017.08.111) such as NEON. For example, due to available historical data, the impacts of extreme or rare events on plant communities could be determined, and both long-term and short-term trends can be monitored and explored over time. 

### Workflow
Follow the instructions [here](https://www.earthdatascience.org/workshops/setup-earth-analytics-python/) to set up your git and bash environment on your computer. For installing your python environment that will be used for this workflow:
1. Fork and clone [the repository to which this README.md file belongs](https://github.com/rami8797/macrosystems_spectral_variance), if you haven't already. This repository contains an environment.yml file that will be used to set up your python environment.
2. If it’s not already open, open the Terminal on your computer (Git Bash for Windows or Terminal on a Mac/Linux).
3. In the Terminal, set your directory to the cloned macrosystems_spectral_variance directory using cd to change directories to where the environment file is stored (e.g. ```cd macrosystems_spectral_variance/macrosystems-env```).
4. Once you are in the macrosystems_spectral_variance/macrosystems-env directory, you can create your environment. To do this run: ```conda env create -f environment.yml```.
5. Once the environment is installed you can activate it using: ```conda activate macrosystems-variance```.

These instructions were adapted from the instructions made available by EarthLab on [how to setup conda environments](https://www.earthdatascience.org/workshops/setup-earth-analytics-python/setup-python-conda-earth-analytics-environment/).

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
12. macrosystems_module

#### Running the Workflow
Begin by opening the python command prompt or terminal on your computer. Activate your environment by typing ```conda activate macrosystems-variance``` and then ```jupyter notebook```. This will open jupyter notebook in a browser tab. From there, navigate to the the example_workflow.ipynb file located in the notebooks_and_notebook_resources directory of this repository. Run the notebook by selecting Kernel from the menu bar and then Restart & Run All. Finally, select Restart and Run all Cells when prompted. Running this notebook in tandem with reading the final_blog.html file will get you up to speed on the current status of the project as well as prompt you to download an h5 file that can be used for further plotting or analyses.

To get an html file from a jupyter notebook, open a new terminal and navigate to the notebooks_and notebook_resources of this repository. With the macrosystems-variance environment activated, run ```jupyter nbconvert --to html_embed --no-input final_blog.ipynb``` in the terminal to convert the final_blog.ipynb file to an html file with code blocks removed. This may be useful for reporting purposes.

### Example Usage
Data formats needed to apply this workflow are csv and h5 files. Both files will be automatically downloaded when running the example_workflow.ipynb file located in the notebooks_and_notebook_resources directory. The files will be downloaded to the earth-analytics/data/earthpy-downloads directory located on your computer. To find similar data that could be used in this workflow, refer to the api_exploration_data_url_retrieval.ipynb file located in the notebooks_and_notebook_resources directory. That notebook will take you through how to find other h5 files that are managed by NEON. 

#### Using the .csv File in this Repository
An example of how to use the csv file located in this repository is below. NOTE: Make sure to run the example_workflow.ipynb file and set a path to the csv file (NEON_Field_Site_Metadata_20220224.csv) prior to running this code.

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
3. The notebooks_and_notebook_resources directory contains files that help support the notebooks within it, hence the resources portion of the directory name. Functions used in this workflow are contained in the macrosystems_module.py file. Functions are callable by importing the macrosystems_module as macmo in notebooks.

### Potential Limitations
The h5 file used in this repository is very large, and users may experience long wait times for code to run or be unable to download the file.

### Zenodo Citation
[![DOI](https://zenodo.org/badge/482348508.svg)](https://zenodo.org/badge/latestdoi/482348508)