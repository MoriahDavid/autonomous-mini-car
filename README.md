# Self Driving Mini Car :construction: :stop_sign: :car:
## The Project:
In this final assigment we focus on creat self driving car system using camera and few sensors.
The main goal is that the car can drive in a path and avoid hitting obstacles on the way.
<br />
### We Use:
1. Modified RC-car with bluetooth control
2. Simple android phone for camera and sensors
<br />

## The Car
The car build with 3 components: toy car, android smartphone and computer.</br>
- The computer running the main control unit over python.
- The toy car is modified to be controlled by Wi-Fi instead of the original controller.
We build it using XIAO-ESP32C2 and L298N motor controller.
- The android smartphone used as camera and sensors for the car.</br>
We used 2 apps:
  - **IP Webcam** - Streaming video over Wi-Fi.</br>
  Can be downloaded form the Play Store [link](https://play.google.com/store/apps/details?id=com.pas.webcam)
  - **SensorServer** - Streaming sensors data over websockets.</br>
  Can be downloaded the apk from this repo [link](https://github.com/umer0586/SensorServer)
![image](https://github.com/MoriahDavid/autonomous-mini-car/assets/93945532/b9d8b12f-a8aa-41bb-8d8e-a847bd16adf4)

<br />
<br />

## Project Structure
The code is separated into parts in order to be more generic and easy to modify.
- **Camera class** - Handle the connection to the camera and  provide a function to retrieve the current frame.
- **Lane Detection class** - Gets a video frame and detects a lane (blue lines) and retrieve the steering angle for get the center of the lane. 
- **Object detection class** - Gets a video frame and return the objects exist in the image using YoloV8 model.
- **Sensors class** - Handle the connection to the sensorServer and provides functions to retrieve the sensors data.
- **Car class** - Handle the connection to the car controller and provides function to control the car - move forward and backward with wanted angle, stop and set car speed.
- **Car Controller class** - get the data from the other classes and responsible to the state machine that control the car actions.

![image](https://github.com/MoriahDavid/autonomous-mini-car/assets/93945532/2121a664-b1f8-4074-89b0-3e31aabc599f)

<br />
<br />

## How To Run:
In order to run you must have all 3 components connected to the same Wi-Fi network, for the most simplicity we used the android phone as hotspot.</br>
The smartphone should be mounted landscape on the car in about 60 degrees to the floor.</br>
1. Open the smartphone hotspot
2. Turn on the car
3. Open the IP Webcam app and the SensorServer app
4. Run the main control program in the computer

The user can control with the keyboard. For stopping the car press the key 's' and for resume running press the key 'r'.
By default, the car start on 'stop' mode.
<br />
<br />

![image](https://github.com/MoriahDavid/autonomous-mini-car/assets/93945532/63452bca-3c43-47a9-b167-e6b2f835a518)

### Related Works:
In several related works we found, the researchers used the OpenCV library to identify a travel lane, road signs and obstacles.<br />
In addition, some of them used additional sensors to detect distance and collision.<br />
According to the output of the sensors and the detection of the movement, a state machine was run which controlled the commands to move the vehicle.

References: 
1. [Self-Driving Car: Using OpenCV Library and Python (IJIRT)](https://ijirt.org/master/publishedpaper/IJIRT159204_PAPER.pdf) <br />
2. [AUTONOMOUS SMART VEHICLE SYSTEM USING OPENCV (IJEAST)](https://www.ijeast.com/papers/307-311,%20Tesma0702,IJEAST,%2017362.pdf) <br />
3. [Lane detection for a self-driving car using OpenCV (medium)](https://medium.com/analytics-vidhya/lane-detection-for-a-self-driving-car-using-opencv-e2aa95105b89)




