<center>![logo](img/head.png)</center>

# DV-Python

*A library that to connect a python script to outputs from the dynamic vision system DV. This is used in conjunction with the Dynamic Vision Sensor (DVS).*

## Features
[DV (Dynamic Vision System)](https://inivation.gitlab.io/dv-docs/) is a platform to develop high-performance, embedded, deployable C++ applications. However, for rapid prototyping and experimenting, many developers prefer to use python. 

**DV-Python** DV python is a library that helps you:

* Get live (raw or processed) data from DV into your python application
* Open files you recorded with DV
* Open older files, recorded with now obsolete software (such as jaer)

## Installation
Make sure you are using a recent python 3 version.
The easiest way to install the library is via pip

```bash
pip3 install dv
```

## Get live event data from the camera

DV communicates with the outside world by means of your computers network stack. To make DV export your required data to the network, follow these steps:

#### Configure DV

1. Start DV
2. Go to *Structure* tab
3. Add a `Dv net output tcp server` by clicking on *Add module*

   ![add module screenshot](img/1.png)

4. Name the module as you wish, for example "event_server"
5. Connect `events` output of your camera with the input of the added module

   ![connection screenshot](img/2.png)

6. The module assumes port `7777` by default. If you are happy with that, you can start the module by pressing the play button. If not, click on the plus button next to the modules name in the configuration list in the right sidebar. 
7. To change the port, change the setting in the window that popped up
   ![connection screenshot](img/3.png)



#### Connect in your python program

A sample program that loops over the events in the input:

```python
from dv import NetworkEventInput

with NetworkEventInput(address='localhost', port=7777) as i:
    for event in i:
        print(event.timestamp)
```

An event has properties `x`, `y`, `polarity` and timestamp. The timestamp is in microseconds.

## Get live frame data from the camera

Configure DV as in the event case, but connect the camera frame output to the network module input.

#### Connect in your python program

A sample program that loops over the events in the input:

```python
from dv import NetworkFrameInput
import cv2

with NetworkFrameInput(address='localhost', port=7777) as i:
    for frame in i:
        print(frame)
        cv2.imshow('out', frame.image)
        cv2.waitKey(1)
```

`frame.image` is a *numpy* matrix that can directly be used to perform openCV operations on it.

### Get other data from the camera
As with the event and frame case, one can also obtain IMU and Trigger data from the camera the same way.


## Open a recording made with DV

Ever `.aedat` file created with DV, contains all the streams of data that were connected to while recording. To get the names of all the streams in the file, call the `.names`.

```python
from dv import AedatFile

with AedatFile(<Path to aedat file>) as f:
	# list all the names of streams in the file
    print(f.names)
    
    # loop through the "events" stream
    for e in f['events']:
        print(e.timestamp)
        
    # loop through the "frames" stream
     for frame in f['frames']:
        print(frame)
        cv2.imshow('out', frame.image)
        cv2.waitKey(1)

```



## Load an old, legacy .aedat file
dv-python supports loading some (sane) *aedat 2* and *aedat 3* files. However, it only supports reading the event data from these files. Other data, like frames etc. is not supported.

```python
from dv import LegacyAedatFile

with LegacyAedatFile('myFile.aedat') as f:
	for event in f:
		print(event.timestamp)
```

**Note** Reading of the file is done completely in python and is therefore pretty slow. This is not recommended for more than quick tests.

## Contribution

This is very new software which can and will contain bugs. Please report any bugs you find, and we'll quickly address them.