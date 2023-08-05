# ProcessedPiRecorder
A multiprocessed class of picamera for video recording.

Saves timestamped images to a BigTif. Can handle stereopi videostream.

## Installation

      pip3 install ProcessedPiRecorder

## Requires

* tifffile        - 2019.7.26    
* picamera        - 1.13         
* opencv-contrib-python - 3.4.4.19     
* numpy           - 1.17.0  

## Basic Usage
You have to initialize the recorder and then tell it when to start recording. 
### Initialize:

      myRecorder = ProcessedPiRecorder(x_resolution = , y_resolution = , framerate = , 
                                       rec_length = , tif_path = ,
                                       stereo=False, scale_factor=1, timestamp=True)
                                       
* (x_resolution, y_resolution) - pixel dimensions to acquired by the sensor(s)
* framerate - desired framerate in Hz
* rec_length - number of seconds to record
* tif_path - file to the output big tif file
* stereo - if True, hflip=True, stereo_mode='side-by-side', stereo_decimate=False
* scale_factor - sets the resize parameter at resolultion*scale_factor
* timestamp - if True, all frames are timestapmed at aquisition

### Run

      myRecorder.recordVid()

## Contributors
This code was written and is maintained by [Matt Davenport](https://github.com/mattisabrat) (mdavenport@rockefeller.edu).
