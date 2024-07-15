# VST-Light
A Python package for seamless control of network-compatible VLP light controllers from VS Technology.


## Installation
VST-Light is available on PyPi and is therefore easily installed using pip:
```zsh
pip install VST-Light
```

## How to Use
### Initialization
To use the module in your project, simply import the `VSTLight` module into your code, and create an instance of the `NetworkController` class, specifying the number of channels available on the connected light controller, and possibly the IP of the light controller, if it has been changed from the default `192.168.11.20`:
```python
import VSTLight

lights_a = VSTLight.NetworkController(4)                    # Default IP
lights_b = VSTLight.NetworkController(4, "192.168.11.128")  # Updated IP
```

At the time of creation, the NetworkController object will open a connection to the physical light controller, if this fails a `ConnectionError` will be raised. Therefore it is required to connect the light controller and turn it on, before running any of the code relying on the `NetworkController` object. When connecting a light controller it is required to update the IP of the ethernet adapter used to make the connection, to be on the same subnet as the controlelr. The VLP controllers are hardcoded to reply to the IP `192.168.11.1`, and it is therefore revommended to update the ethernet adapter to this specific IP, but any IP on the `192.168.11.XXX` subnet will work, as long it is not occupied by another device.  
The network connection has a timeout of 5 seconds, the call to create the `NetworkController` object is therefore blocking untill a connection has been established or the time has passed.

Please refer to the documentation of the connected VLP light controller for more information on how it operates and what the different modes mean.

### Updating the Channels
Having crated an instance of the `NetworkController` class, the intensity and state of a single channel can be updated:
```python
lights_a.set_intensity(2, 158)
lights_a.set_on(2)
```
Alternatively all channels can be updated at once:
```python
lights_b.set_all_intensities(200)
lights_b.set_all_on()
```
Note that if an invalid value is passed to any of the class methods, a `ValueError` will be raised. Additionally the channel number passed to the controller object is derived from the channel number on the physical light controller. It is therefore NOT zero indexed, but rather starts at 1 for the lowest channel.

### Speed Limitations
The VLP controllers are physically limited in how quickly they can recieve new commands. Each command must be spaced out by at least 5 ms, in order to be interpreted correctly. To overcome this, the `VSTLight` module keeps track of the time since the last command. If the time is less than 5 ms, the program will sleep untill 5 ms has passed since the last command was sent. Therefore any method call on a `NetworkController` object, has the potential to be blocking, if performed within 5 ms of another call.

If this is undesireable for your usecase, consider running the `NetworkController` in a separate thread, so as to not block your main thread at any point.

### Example
Below is an example program that turns a light connected to channel 1, on and off 1000 times:
```python
from VSTLight import NetworkController
import time

# Create controller object
lights = NetworkController(4)

# Set the intensity of channel 1 to 255
lights.set_intensity(1, 255)

# Toggle the light on and off 1000 times
for _ in range(1000):
    lights.set_on(1)
    time.sleep(0.5)

    lights.set_off(1)
    time.sleep(0.5)

# Close the connection and shut down gracefully
lights.destroy()
```

Refer to the section below for a list of all available methods. Complete example programs showcasing the module functionality can be found in the [examples](https://github.com/Attrup/VST-Light/tree/main/examples) folder.
## Available Methods
Below is an exhaustive list of all methods currently available using the `NetworkController` class:
- `set_intenisty`: Updates the intensity of a single channel
- `get_intensity`: Returns the intensity of a single channel
- `set_on`: Turn a single channel on
- `set_off`: Turn off a single channel
- `toggle`: Toggle the on-off state of a channel
- `set_strobe_mode`: Updates the strobe mode of a single channel
- `get_strobe_mode`: Returns the strobe mode of a single channel
- `set_all_intensities`: Updates the intensity of all channels
- `set_all_on`: Turn all channels on
- `set_all_off`: Turn all channels off
- `toggle_all`: Toggle the on-off state of a channel
- `set_all_strobe_modes`: Set the strobe mode of all channels