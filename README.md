# UGLab - Urban Growth Lab

UGLab is a python open source project capable to execute Urban Growth predictions for any geographic area available on [CORINE](https://land.copernicus.eu/pan-european/corine-land-cover) dataset. 

Running the dea
## Prerequistics
- Set up a python 3.7 environment.

The project has been tested under the following environment.
```
Python: 3.7.6
platform: Windows-10-10.0.19041-SP0
pip: n/a
setuptools: 58.2.0
setuptools_rust: 0.12.1
```


- Install GDAL. Further info can be fond [here](https://pypi.org/project/GDAL/). (if you face any problems installing GDAL then try to install [OsGeo](https://www.osgeo.org/projects/osgeo4w/))
- Pip install the following libraries
 >##### keras
 >##### numpy
 >##### gdal
 >##### rtree
 >##### sklearn
 >##### matplotlib
- Download the project and extract it locally
- Run the uglab_demo.py script within the root of the project

For demonstration purposes we include a subset of the Pan -European datasets needed to run the project.
This is a demo project for city of Munich, Germany. 
Related data sources are placed within `_uglab_source_demo_data` folder.
All generated files will be placed within `_uglab_demo_project` folder.
Also notice the existence of `MUNICH_MBR.shp` within `_uglab_demo_project` folder, this is the study area for our demo (munich).
The whole procedure to complete will take from 15 minutes to 1 hour depending on the machine running it. 

After script completion your  `_uglab_demo_project` folder should be fulfilled with the intermediate produced data.
There should also be a new folder `ml_data` containing the final data, including:
- 1 plot for the feature impact using the Linear Regression method
- 1 plot for the feature impact using the Random Forest method
- 1 plot for Accuracy learning curves
- 1 plot for Loss learning curves
- 1 csv file containing x_coord, y_coord, urban/nonurban 2006, urban/nonurban 2018, urban/nonurban 2018 - predicted
eg.
```
2786941.88	4211759.85	0.00	0.00	0.00	0.00
2800021.84	4211316.97	0.00	1.00	1.00	1.00
2799278.66	4211021.72	0.00	1.00	0.00	1.00
................................................
```
- 1 geotiff for the year 2018 with real changes
- 1 geotiff for the year 2018 with predicted changes
- 1 geotiff for the year 2030 with predicted changes






## License

This project is part of my PHD research. The source code is released under the MIT license.  Please let me ([tsagkis@mail.ntua.gr](mailto:tsagkis@ntua.gr)) and my tutor Professor Eythimios Bakogiannis ([xxx@mail.ntua.gr](mailto:xxx@ntua.gr)) know for any progreess or customization you have made and would like to share. 

See [LICENSE](LICENSE) file for details.



........ more information soon.
