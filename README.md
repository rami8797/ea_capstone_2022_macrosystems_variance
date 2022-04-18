# ea_capstone_2022_macrosystems_variance

### Project Purpose
The purpose of this project is to calculate the variance of hyperspectral imagery between National Ecological Observatory Network (NEON) sites located throughout the western part of the United States. This will be used to support a larger project in which vegetation on the ground will be identified via remote sensing data depending on the wavelengths absorbed/reflected by the vegetation. Knowing the the variance of hyperspectral imagery between sites is a critical part of this larger goal. For example, sites located at higher elevations may have vegetation that refelct more of the blue wavelength compared to plants located at lower-elevation sites. If you used the assumption that all plants reflect the same amount of the blue wavelength at other sites, you would not be able to correctly identify plants located in other areas, hence the need to know the hyperspectral variance of NEON sites. 

The second purpose of this project is to determine whether the variance at each individual NEON site is driven by space or time to inform sampling decisions. Specifically, we hope to answer the question: how many times will sampling need to take place at each NEON location to capture all of the variation at that site? Will it be at the same 10 hectare plot within the site over the course of a month (variation driven by time) or will sampling need to be done just once but at several distinct 10 hectare plots at the same site (variation driven by space)? 

### Installation Instructions
Follow the instructions [here](https://www.earthdatascience.org/workshops/setup-earth-analytics-python/) to set up your python, git, and bash environment on your computer.

### Project Data
1. **Sentinel-2**

[Credit](https://sentinel.esa.int/web/sentinel/missions/sentinel-2)

![Sentinel-2 Image of Niwot Ridge](/images/sentinel_2_niwot_ridge.png)


2. **Airplane platform**

[Credit](https://data.neonscience.org/data-products/DP3.30006.001)

![NIWOT Level 3 Orthorectified Mosaic Dataset Red Band Reflectance (August 2020)](/images/niwot_red_refl_08_22.png)


3. **Unmanned Aerial Vehicle (UAV)**

[Credit](https://uavprime.com/wp-content/uploads/2021/04/RedEdge-MX-Dual-Camera-Whitepaper.pdf)

![UAV Captured Wavelengths](/images/micasense_wavelength_image.png)


### Project Workflow

![Project Workflow Diagram](/images/ea_capstone_22_workflow.png)