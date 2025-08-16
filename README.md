# Adeept RaspTank-V4 Smart Car Kit for Raspberry Pi
Adeept RaspTank is an open source intelligent robotics product for artificial intelligence, robotics enthusiasts and students. This product is based on the Raspberry Pi motherboard using the python language and is compatible with the following Raspberry Pi models: 3B,3B+,4,5, etc.

## Resources Links

[RobotName]: Adeept RaspTank-V4 \
[Item Code]: ADR013-V4 \
[Official Raspberry Pi website]: https://www.raspberrypi.org/downloads/    \
[Official website]:  https://www.adeept.com/     \
[GitHub]: https://github.com/adeept/adeept_rasptank2/     


## Getting Support or Providing Advice

Adeept provides free and responsive product and technical support, including but not limited to:   
* Product quality issues 
* Product use and build issues
* Questions regarding the technology employed in our products for learning and education
* Your input and opinions are always welcome

We also encourage your ideas and suggestions for new products and product improvements
For any of the above, you may send us an email to:     \
Technical support: support@adeept.com      \
Customer Service: service@adeept.com


## About Adeept

Adeept was founded in 2015 and is a company dedicated to open source hardware and STEM education services. The Adeept technical team continuously develops new technologies, uses excellent products as technology and service carriers, and provides comprehensive tutorials and after-sales technical support to help users combine learning with entertainment. The main products include various learning kits and robots for Arduino, Raspberry Pi, ESP32 and BBC micro:bit.    \
Adeept is committed to assist customers in their education of robotics, programming and electronic circuits so that they may transform their creative ideas into prototypes and new and innovative products. To this end, our services include but are not limited to:   
* Educational and Entertaining Project Kits for Robots, Smart Cars and Drones
* Educational Kits to Learn Robotic Software Systems for Arduino, Raspberry Pi and micro: bit
* Electronic Component Assortments, Electronic Modules and Specialized Tools
* Product Development and Customization Services


## Copyright

Adeept brand and logo are copyright of Shenzhen Adeept Technology Co., Ltd. and cannot be used without written permission.

---

## 🤖 Technical Documentation

### Automatic Movement Systems

The RaspTank robot implements sophisticated **automatic movement modes** managed through a multi-threaded architecture:

#### 🏗️ Architecture Overview
```
- webServer_HAT_V3.1.py    # Command dispatcher
- functions.py             # Automatic movement logic  
- move.py                  # Low-level motor control
- camera_opencv.py         # Computer vision tracking
```

#### 🔄 Threading System
The automatic movement runs in a **separate thread** using Python's `threading.Thread`:

```python
class Functions(threading.Thread):
    def __init__(self):
        self.functionMode = 'none'  # Current mode
        self.__flag = threading.Event()  # Thread control
        
    def run(self):
        while 1:
            self.__flag.wait()  # Wait for activation
            self.functionGoing()  # Execute current mode
```

#### 🎯 Automatic Movement Modes

**A) Obstacle Avoidance (`automatic`)**
- Uses ultrasonic sensor for distance measurement
- Forward movement when path is clear (>40cm)
- Scan left/right when obstacle detected (20-40cm)
- Backup when too close (<20cm)

**B) Line Following (`trackLine`)**  
- Uses 3 infrared line sensors (left, middle, right)
- Follows black lines on white surfaces
- Dynamic speed adjustment based on line position

**C) Computer Vision Tracking**
- Real-time object tracking using OpenCV
- Color-based object following
- Servo-controlled camera movement

#### 🎮 Control Mechanisms
- **Start**: `self.__flag.set()` - Resumes the thread
- **Stop**: `self.__flag.clear()` - Pauses the thread  
- **Mode Switch**: Changes `functionMode` variable
- **Emergency Stop**: `move.motorStop()` - Immediate halt

### 🎥 Computer Vision System

The RaspTank uses **OpenCV-based computer vision** for intelligent tracking:

#### 🎯 Vision Tracking Modes

**Color Tracking (`findColor`)**
```python
# Process flow:
1. Convert frame to HSV color space
2. Create color mask with configurable range
3. Find contours of colored objects
4. Calculate center point and tracking errors
5. Move servos and robot to follow object
```

**Line Following (`findlineCV`)**
```python
# Process flow:
1. Convert to grayscale
2. Apply binary threshold
3. Sample two horizontal scan lines
4. Calculate line center position
5. Control robot movement based on line position
```

#### 🔧 Smart Motor Control
The `video_Tracking_Move()` function provides **differential steering**:
- **Left turn**: Left motor slower, right motor normal speed
- **Right turn**: Right motor slower, left motor normal speed  
- **Forward**: Both motors at equal speed

#### 📡 Servo Tracking System
- **Kalman filtering** for smooth servo movements
- **PID control** for precise tracking
- **Dual-axis tracking** (pan/tilt camera movement)

#### 🎨 Advanced Features
1. **Real-time Processing**: 30+ FPS video analysis
2. **Adaptive Thresholding**: Adjustable for different lighting
3. **Color Range Calibration**: Dynamic HSV range setting
4. **Multi-threading**: Non-blocking CV processing
5. **Differential Steering**: Smooth turning during tracking

#### 🎯 Control Flow
```
Camera Frame → OpenCV Processing → Object Detection → Error Calculation → 
Kalman Filter → Servo Movement + Robot Movement → Repeat
```

### 🛠️ Hardware Integration

The system integrates multiple hardware components:
- **Motors**: DC motors with PCA9685 PWM control
- **Sensors**: Ultrasonic distance, infrared line sensors  
- **Camera**: Raspberry Pi camera with servo-controlled pan/tilt
- **Servos**: Multiple servo motors for mechanical control
- **LEDs**: WS2812 RGB LED strips for visual feedback

### ⚡ Key Features

1. **Non-blocking Operations**: All automatic functions run in background threads
2. **Interruptible Control**: Can be stopped/started instantly via web interface
3. **Multi-modal Behavior**: Supports obstacle avoidance, line following, vision tracking
4. **Sensor Fusion**: Combines ultrasonic, optical, and vision sensors
5. **Web-based Interface**: Real-time control through web browser
6. **Modular Design**: Easy to extend with new autonomous behaviors

The RaspTank combines **computer vision**, **control theory**, and **robotics** to create an intelligent autonomous robot platform suitable for education and research! 🚀
