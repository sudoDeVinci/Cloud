# Background

Quick yet accurate Weather predication is imperative for certain industries to now only survive, but simply exist. An important factor of these is the ability to track, categorize and predict movements of clouds within a given area. Ceilometers use a laser/light source to determine a cloud's base or ceiling height. A  Ceilometer usually can also measure aerosol concentration in air [[1]](#1). The downside is that ceilometers have a relatively small area of measurement directly above the unit which would not be an issue, however, as of 2020 they can cost around USD $30 000 per unit [[3]](#3).

There exists however, high quality satellite data mada available by NASA. The new MISR Level 2 Cloud product contains height-resolved, cloud motion vectors at 17.6 km resolution; cloud top heights at 1.1 km resolution; and cross-track cloud motion components at 1.1 km resolution [[2]](#2). Now this data is made available to be used by software engineers to visualize as needed. The issue? This data is not meant for real-time application on a  local area level. These products are made for global application, collecting data only on the sunlit side of earth over the course of 9 days [[4]](#4). 

A  better solution for the local-area level must be thought of then, to better predict cloud movement and category.



## Proposal

In the case of local cloud monitoring, what I propose as needed is real-time, modular, and open-source as to avoid contractual right to repair issues.

My plan is a mesh network comprised of simple esp32-based devices, equipped with a medium-resolution camera, hygrometer, altimeter, and gyroscope.

I propose that with these devices, environmental readings and pictures of the sky can be transmitted to a central server in set time intervals for processing in essentially real-time. These measurements and images, in theory, can be used to determine cloud characteristics and movement in a way not done anywhere else. 
This system can then by used in conjunction with existing systems to provide more accurate weather data for a local area.


### Cloud Height

An important factor for cloud monitoring is obtaining the cloud base height.
The cloud base is  the lowest point of the visible portion of a cloud, usually expressed in meters above sea level/planet surface.
This can be calculated in close estimation by finding the lifted condensate level.
The lifted condensation level or lifting condensation level (LCL) is formally defined as the height or pressure at which the relative humidity (RH) of an air parcel will reach 100% with respect to liquid water when it is cooled by dry adiabatic lifting. [[5]](#5) The LCL can be approximated using the dew point,humidity and temperature a few diffrent ways. The most popular being Espy's equation, which has been shown to be satifactory for accurate readings within 200m. [[6]](#6)


### Cloud Identification

I have discovered it possible through a previous proof of concept, that it is theoretically possible to identify clouds from images of the sky, using only the visual colour space. In short, clouds are can be shown to be quite diffrent in their colour content from the surrounding sky or landmarks (obviously). This can be seen in the below graph, showing the differences in the BGR colour space of clouds vs the sky.

<br>
<br>

![BGR Frequency Chart for High Res Images](/Graphs/BGRBarGraph.png "BGR Frequency Chart for High Res Images")
##### Figure showing frequency distribution in BGR colour channels of Sky versus Cloud Image set
<br>
<br>

<br>
<br>

This separation can also be seen in the HSV color space, as shown below.
![HSV Frequency Chart for High Res Images](/Graphs/HSVBarGraph.png "BGR Frequency Chart for High Res Images")
##### Figure showing frequency distribution in HSV colour channels of Sky versus Cloud Image set
<br>
<br>

<br>
<br>

Using singular value decomposition, we can view each colour channel separaetly as a principle component. Here we can see that two of each of our channels can be used to separate the cloud vs sky pixel values. Scree plots showing these can be seen below.
![BGR ScreePlot for High Res Images](/Graphs/BGRScree.png "BGR ScreePlot for High Res Images")![HSV ScreePlot for High Res Images](/Graphs/HSVScree.png "HSV ScreePlot for High Res Images")
##### Figure showing ScreePlot of HSV colour channels in Sky versus Cloud Image set
<br>
<br>

#### Cloud Type Identification

This information then, can be used to train models identify the cloud type. If we are able to estimate the coud height, as well as having the environmental readings and a medium-resoltuion image, this should in theory be simple. 
* (While this is usualy done while also using IR information to determine the cloud temperature, due to the fact camera will be pointing upwards, this is not an option.)

I propose training a simple classification model using both this data. Once the model is able to classify the cloud type and state its position in the image, we can move onto assigning it a motion vector. 


### Cloud Movement Information

Assigning motion vectors to identified clouds allows us to determine the direction, speed and size of the cloud formation.
This is done after undistorting the image using the camera's intrinsic distortion matrix, then mapping the cloud image onto 3D space given the angle of the camera to the sky.
A cloud's size can be assigned from the image. This is important not only to keep a record of for tracking weather changes, but also determining the future cloud shade on the ground.
A motion vector can be assigned to a cloud by comparing two images taken within the set time interval.
In a situation where a cloud is larger than the viewing area of the camera, this idea of assigning motion vectors breaks down, however, this is where the idea of the mesh network comes into play.


### Device arrangement

A mesh network is needed, not only to properly analyze very large clouds, but also to track them across large distances.
I propose a grid arrangement, where, while the controllers may be placed at diffrent heights, the edge of the view of one controller at a pre-determined height, must be the beginnning of the viewing area of another.
For example: If a minimum viewing height of 1.98km is chosen (the average minimum height of cumulo-nimbus clouds) [[7]](#7), and a camera with a 90 deg angle of view (relatively small) at that height is used, then an area of ~3.96km can be covered by a single camera. This means that for continuous veiwing, cameras must be placed every ~4km in all directions. In reality, cameras with wider FOVs exist, making this a somewhat worst case scenario.


### Bill of materials

1. 4 esp-32 CAM boards to arrange in a grid pattern. I chose [these](https://www.amazon.se/-/en/Freenove-ESP32-WROVER-Compatible-Wireless-Detailed/dp/B09BC5CNHM/ref=d_pd_sbs_sccl_2_4/258-4653752-6686012?pd_rd_w=cLYYr&content-id=amzn1.sym.c4184aba-d168-41de-ae27-7ea9a5ac5302&pf_rd_p=c4184aba-d168-41de-ae27-7ea9a5ac5302&pf_rd_r=J39YTFT9T0YD3286FJ86&pd_rd_wg=UZr9j&pd_rd_r=70d6ad77-67e9-41e1-817d-5663a0cb7a10&pd_rd_i=B09BC5CNHM&psc=1) at ~200kr each

2. 4 medium-quality cameras. I chose the [OV5670](https://www.aliexpress.com/item/1005003006706291.html?spm=a2g0o.productlist.main.11.1fe76789LXf1t9&algo_pvid=186dfeb3-c167-4fac-af7a-992f5e8d79c4&algo_exp_id=186dfeb3-c167-4fac-af7a-992f5e8d79c4-5&pdp_npi=3%40dis%21SEK%21194.13%21126.18%21%21%21%21%21%402100ba4716847273871928704d074c%2112000023187267001%21sea%21SE%210&curPageLogUid=V8FZx2ua980H) at ~300kr each.

3. 4 high accuracy humidity sensors. I chose the [SHT31-D](https://www.electrokit.com/en/product/adafruit-sensirion-sht31-d-temperatur-luftfuktighetssensor/) at  ~230kr each.

4. 4 high accuracy altimeters. I chose the [BMP390](https://www.electrokit.com/en/product/adafruit-bmp390-barometer-and-altimeter/) at ~180kr each.

5. 4 gyroscopes. I chose the [MPU-6050](https://www.electrokit.com/en/product/mpu-6050-accelerometer-3-axel-monterad-pa-kort-2/) at ~52kr each.

All other materials are already possessed.

A total of : 3848 sek


### Expected time

If shipping times remain in my favour, I should be able to contruct the  4 weather stations by the end of July, 2023.
For the requested parts list, supply is short and resources for usage are sparce. 


# Bibliography

<a id = "1" href = "https://books.google.se/books?id=_iqUDwAAQBAJ&pg=PA60&redir_esc=y#v=onepage&q&f=false">[1]</a> The National Oceanic and Atmospheric Administration. 16 November 2012. p. 60.

<a id = "2" href = "https://www-cdn.eumetsat.int/files/2020-04/pdf_conf_p60_s6_03_mueller_v.pdf">[2]</a> K. Mueller, M. Garay, C. Moroney, V. Jovanovic (2012). MISR 17.6 KM GRIDDED CLOUD MOTION VECTORS: OVERVIEW AND ASSESSMENT, Jet Propulsion Laboratory, 4800 Oak Grove, Pasadena, California.

<a id = "3" href = "https://ieeexplore.ieee.org/stamp/stamp.jsp?arnumber=9088230">[3]</a> F .Rocadenbosch, R. Barragán , S.J. Frasier ,J. Waldinger, D.D. Turner , R.L. Tanamachi, D.T. Dawson (2020) Ceilometer-Based Rain-Rate Estimation: A Case-Study Comparison With S-Band Radar and Disdrometer Retrievals in the Context of VORTEX-SE

<a id = "4" href = "https://misr.jpl.nasa.gov/mission/misr-instrument/spatial-resolution/">[4]</a> “Misr: Spatial resolution,” NASA, https://misr.jpl.nasa.gov/mission/misr-instrument/spatial-resolution/ (accessed May 19, 2023). 

<a id = "5" href = "https://www.ncl.ucar.edu/Document/Functions/Contributed/tlcl_rh_bolton.shtml">[5]</a> “tlcl_rh_bolton,” Tlcl_rh_bolton, https://www.ncl.ucar.edu/Document/Functions/Contributed/tlcl_rh_bolton.shtml (accessed May 21, 2023). 


<a id = "6" href = https://www.researchgate.net/publication/290441042_A_Simplified_Analytical_Method_to_Calculate_the_Lifting_Condensation_Level_from_a_Skew-T_Log-P_Chart#pf3>[6]</a> Muñoz, Erith & Mundaray, Rafael & Falcon, Nelson. (2015). A Simplified Analytical Method to Calculate the Lifting Condensation Level from a Skew-T Log-P Chart. Avances en Ciencias e Ingenieria. 7. C124-C129. 

<a id = "6" href = https://cloudatlas.wmo.int/en/observation-of-clouds-from-aircraft-descriptions-cumulonimbus.html>[7]</a> [1] Wmo, “Cumulonimbus,” International Cloud Atlas, https://cloudatlas.wmo.int/en/observation-of-clouds-from-aircraft-descriptions-cumulonimbus.html (accessed May 21, 2023). 


















