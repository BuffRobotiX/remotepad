# remotepad

remote pad is a python3 program that allows you to emulate gamepads on one computer controlled by gamepads from other
computers. remotepad only supports Windows and python3.

remotepad leverages the joystick emulation softwate, [vJoy][1], and its unofficial python
bidings, [pyvjoy](https://github.com/tidzo/pyvjoy) by [tidzo](https://github.com/tidzo), which is included in this
repository.

This repo includes a server side program, for receiving and emulating gamepads, and a client side program, for
transmitting gamepad commands.

## Server setup.
1. Download and install [vJoy][1]. You may want to replace the vJoyInterface DLL with the new installed one from
`Program Files\vJoy\x86` if it is out of date.
2. Launch the "Configure vJoy" application.
3. Add the number of devices you wish to emulate on your machine.
4. Make sure each gamepad has 4 axes: X, Y, Z, and Rx, and 12 buttons. This is the configuration that remotepad
supports.
5. Edit the `setup_server.json` file to configure it for your needs:

The setup json contains a list of 'pads' which map UDP ports to vJoy device IDs. Choose which ports map to which IDs.

Notice: Ensure that the number of pads in the setup file are equivalent to the number of configured vJoy devices.
6. Ensure that firewall rules and port forwarding allow access to the specified ports.
7. Run `remotepad_server.py` with python3.

## Client setup
1. Install the `pygame` package:
```
pip3 install pygame
```
or
```
pip3 install -r requirements.txt
```
2. Edit `setup_client.json` to your liking:
The ID should be set to the gamepad ID of the gamepad you would like to use. Running `remotepad_client.py` will print
the list of attached devices.

The address is the IP address of the server.

The port is the agreed upon network port of the server.

You can also remap axes and buttons to emulate differently on the server.

3. Run `remotepad_client.py` with python3.

Now actions performed on the remote gamepad should be applied to the virtual one.

[1]:http://vjoystick.sourceforge.net
