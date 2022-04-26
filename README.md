# Water Phantom Control

Module name: `water_phantom_control`  

Control software for the custom made water phantom of @SchneiderMar. It consists of two stepper motor axes, allowing for horizontal movement, and a electric cylinder that enables vertical movement. The stepper motors are connected to a TMCM-6110 PCB that is controlled via USB. The electric cylinder is connected to an Arduino with a motor shield and is also connected via USB. The following module allows to connect to theses devices, set the axes to their initial positions and afterwards move them to arbitrary positions within the phantom. 

## Installation

There are multiple ways to install the module. The easiest one is to use a virtual environment. More experiened users might want to install the module directly. Please refer to the instructions below and ensure that `python3` is used.

### Virtual Environment Installation

The virtual environment is installed in its own directory. To provide an example, it is called `wpc-venv` in the following. The environment is created via

```python
python3 -m venv wpc-venv
```

and activated via

```
source dpx_virtenv/bin/activate
```

After succesful execution, the name of your virtual environment should appear in parentheses in front of your command prompt. Finally, proceed like described in the "Direct Installation"-section below.

### Direct Installation
`sudo` might be required to provide installation privileges. This won't be necessary when installing in an virtual environment.

#### via pip
If no administrator access is possible, add the parameter `--user` right behind `install`.

```bash
python3 -m pip install /path/to/package
```

If you want to modify the code later on, use

```bash
python3 -m pip install -e /path/to/package
```

instead.

#### via setup.py

Execute in the module's main directory:

```bash
python3 setup.py install
```

If you want to modify the code later on, use

```bash
python3 setup.py develop
```

instead.

## Usage

Only a few commands are necessary to control the axes of the water phantom. A minimum working example is shown below

```python
import water_phantom_control

wpc = water_phantom_control.WaterPhantomControl(None, use_cylinder=True)
wpc.move_to_coords_cm(1, 1, 3)
```

First, the previously installed `water_phantom_control` module is imported and an object `wpc` of class `WaterPhantomControl` is created and the connection to the stepper motors and the electric cylinder is initialized. Here, only two parameters are required for its initialization:

| Parameter | Function |
| :-------- | :------- |
| `cylinder_port` | Port the arduino controlling the electric cylinder is connected. If `use_cylinder` is `False`, the parameter is not considered. If `cylinder_port` is `None`, the program tries to find the port by itself. Please note that this might not work when using Windows |
| `use_cylinder` | If `True`, the electric cylinder, i.e. the z-axis, is used. This can be turned off, so only movement with the x-y-axes can be made. This is useful if the cylinder is not used at all and maybe replaced with a rigid mounting |

After the command was called, all axes move to their initial positions. `move_to_coords_cm` moves the detector to the desired position. The arguments are the `x`-, `y`-, and `z`-positions in cm. The `x`-axis represents the short, uppermost stepper motor axis. `y` resembles the long, stepper motor directly below. Finally, `z` is the axis of the electric cylinder. Note that `z` can be provided in absolute values that describe the distance from the lower part of the cylinder to its housing.  
A parameter `block` can be provided to the `move_to_coords_cm`-command. It is usually set to `True`, i.e. the command waits until all axes reached the provided position. If set to `False`, other commands can be used while the axes are moving. But please take care as sending other move commands during this time might lead to undesired results. By using `wpc.position_reached()`, it can be checked, if all axes are at the provided position.
