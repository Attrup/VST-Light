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
Note that if an invalid value is passed to any of the class methods, a `ValueError` will be raised. 

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