## Cloud Size Estimation

The main crux of this project is the estimation of a cloud's size after it's pixel area has been selected. This is difficult with most camera's, as every camera has some intrinsic distortion, making accurate estimation of size and distance difficult. However, it is possible to calibrate our camera and undistort images captured with it. Since the angle of the camera is known to us (preferably 90), along with the approximate cloud base height, and the field of view of the camera, it is then possible to give an estimation of the total area of the cloud. This would also allow us, knowing the distance the cloud would travel across two frames at that particular height, to then assign a velocity vector to a cloud.

### Cloud Base Height Calculation

An important factor for cloud monitoring is obtaining the cloud base height. The cloud base is
the lowest point of the visible portion of a cloud, usually expressed in meters above sea
level/planet surface. This can be calculated in close estimation by finding the lifted condensate
level. The lifted condensation level or lifting condensation level (LCL) is formally defined as the
height or pressure at which the relative humidity (RH) of an air parcel will reach 100% with
respect to liquid water when it is cooled by dry adiabatic lifting. [5] The LCL can be
approximated using the dew point,humidity and temperature a few different ways. The most
popular being Espy's equation, which has been shown to be satisfactory for accurate readings
within 200m [6].

A more simple cloud height for most cumulus and cumulo-nimbus clouds can be found via:

1. Calculating the difference between the current temperature and the dew point.
2. Divide the result by 2.5 for measurements in Celsius (4.4 for Farenheit) then multiply by 1000 to get the cloud base in feet above the current measurement point.
3. Multiply this result by 0.3048 to get the cloud base height in feet from the current height.

### Camera Calibration

In simple terms, all cameras have intrinsic and extrinsic characteristics which induce image distortion which can be expressed as matrices. Once found, we can induce a distortion matrix, and thusly, an image matrix to be applied to images to undo distortion. This is done via the openCV library and involves finding the position of known, measured object points in our distorted image and finding the transformations done to obtain our known measurements. In my case these are found in [calibration images](/calibration_images/), the code from which is mostly [from Nicolai Høirup Nielsen](https://github.com/niconielsen32) in his [ComputerVision](https://github.com/niconielsen32/ComputerVision) repository. An example below shows an example image and its undistorted form.

![Distorted image 4](calibration_images/img4.jpeg "Calibration image example")![Undistorted image 4](calibration_images/undistorted.png "Undistorted Image Example")

This undistorted image can now be used for the mapping of 3D objects of known dimensions.

If another lens was added such as a dome to the camera module, an extrinsic matrix for the lensing of that dome would be needed but trivial to adjust for.