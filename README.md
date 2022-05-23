# macrosystems_spectral_variance

### Project Description
The purpose of this repository is to document the progress of my Earth Analytics capstone project as well as to safely store related data and items. The project goal is to calculate the variance of hyperspectral imagery between National Ecological Observatory Network (NEON) sites located throughout the western part of the United States. This will be used to support a larger project in which vegetation on the ground will be identified via remote sensing data depending on the wavelengths absorbed/reflected by the vegetation. Others may wish to use the workflow presented in this repository to perform a similar analysis for other NEON sites located outside of the western United States.

### Project Background
Using remote sensing to identify plants for the purposes above is actively being explored.

1. [Multispectral Approach for Identifying Invasive Plant Species Based on Flowering Phenology Characteristics](https://www.mdpi.com/2072-4292/11/8/953/htm)
2. [No place to hide: Rare plant detection through remote sensing](https://onlinelibrary.wiley.com/doi/full/10.1111/ddi.13244) 

While identifying plants using remote sensing is being researched, there are great [advantages to conducting this type of work at long-term ecological monitoring sites](https://doi.org/10.1016/j.scitotenv.2017.08.111) such as NEON. For example, due to available historical data, the impacts of extreme or rare events on plant communities could be determined, and both long-term and short-term trends can be monitored and explored over time. 

### Workflow
Follow the instructions [here](https://www.earthdatascience.org/workshops/setup-earth-analytics-python/) to set up your git and bash environment on your computer. For installing your python environment that will be used for this workflow:
1. Fork and clone [the repository to which this README.md file belongs](https://github.com/rami8797/macrosystems_spectral_variance), if you haven't already. This repository contains an environment.yml file that will be used to set up your python environment.
2. If it’s not already open, open the Terminal on your computer (Git Bash for Windows or Terminal on a Mac/Linux).
3. In the Terminal, set your directory to the cloned macrosystems_spectral_variance directory using cd to change directories (e.g. ```python cd macrosystems_spectral_variance```).
4. Once you are in the macrosystems_spectral_variance directory, you can create your environment. To do this run: ```python conda env create -f environment.yml```.
5. Once the environment is installed you can activate it using: ```python conda activate macrosystems_spectral_variance```.

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

#### Running the Workflow
Begin by running the macrosystems_blog.ipynb file located in the notebooks_and_notebook_resources directory of this repository. This will get you up to speed on the current status of the project as well as prompt you to download an h5 file that will be used in the other notebooks contained within the repository.

After running the macrosystems_blog.ipynb file, run the no_code_html_macrosystems_blog.ipynb to convert the macrosystems_blog.ipynb file to an html file with code blocks removed. This may be useful for reporting purposes.

### Example Usage
Data formats needed to apply this workflow are csv and h5 files. Both files csv file will be automatically downloaded when running the macrosystems_blog_ipynb file located in the notebooks_and_notebook_resources directory. The files will be downloaded to the earth-analytics/data/earthpy-downloads directory located on your computer. To find similar data that could be used in this workflow, refer to the api_exploration_data_url_retrieval.ipynb file located in the notebooks_and_notebook_resources directory. That notebook will take you through how to find other h5 files that are managed by NEON. 

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
3. The notebooks_and_notebook_resources directory contains files that help support the notebooks within it, hence the resources portion of the directory name. I created a filtering function to identify NEON sites that meet a certain criteria in filtering_metadata_function_and_figures.ipynb that uses the file in the data directory. In open_h5_file_function.ipynb, I adapt [the aop_h5refl2array function shown in a NEON tutorial](https://www.neonscience.org/resources/learning-hub/tutorials/calc-ndvi-tiles-py) to create a function that will allow me to open an h5 file, pull out the reflectance arrays within it, put the full arrays into a dataframe where they are matched with their corresponding wavelengths, and then expand the arrays so that each value within an array gets placed into its own row within a "reflectance" column. These two functions are in the macrosystems_module.py file and are callable by importing the macrosystems_module as macromo in notebooks. In create_niwo_h5_waveform.ipynb, I plot the waveform of one h5 file and begin to extract and analyze the bands outlined in the RedEdge-MX-Dual-Camera-Whitepaper.pdf file located in the documents directory. This notebook is currently incomplete. The no_code_html_macrosystems_blog.ipynb notebook detailed under the "Running the Workflow" heading is supported by the no_code_html.tpl file. The macrosystems_blog.html file is the output from running the no_code_html_macrosystems_blog.ipynb notebook.

### Potential Limitations
The h5 file used in this repository is very large, and users may experience long wait times for code to run or be unable to download the file.

### Zenodo Citation
[![DOI](https://zenodo.org/badge/482348508.svg)](https://zenodo.org/badge/latestdoi/482348508)