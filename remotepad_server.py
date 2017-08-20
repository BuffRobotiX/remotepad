import argparse
import json
import os
import pyvjoy
import socket
import sys

name_to_axis = {
    'x': pyvjoy.HID_USAGE_X,
    'y': pyvjoy.HID_USAGE_Y,
    'z': pyvjoy.HID_USAGE_Z,
    'rx': pyvjoy.HID_USAGE_RX
}


def set_axis(pad, axis, value):
    """Set a pad's axis from -1 to 1"""
    # Range is 1 (full left) to 32768 (full right) for some reason...
    value = round((value + 1) / 2.0 * (32768 - 1) + 1)
    pad.set_axis(name_to_axis[axis], value)


def reset(pad):
    """Unset a pad's buttons and set its axes to neutral"""
    pad.reset()
    pad.reset_buttons()
    set_axis(pad, 'x', 0)
    set_axis(pad, 'y', 0)
    set_axis(pad, 'z', 0)
    set_axis(pad, 'rx', 0)


def main():
    parser = argparse.ArgumentParser(description='Emulate gamepads from afar.')
    parser.add_argument('setup', nargs='?', default='setup_server.json', help='The setup JSON')
    args = parser.parse_args()
    if not os.path.exists(args.setup):
        print('Setup file does not exits.')
        sys.exit(1)

    with open(args.setup) as f:
        setup = json.load(f)

    pads = []
    for setting in setup['pads']:
        pad = pyvjoy.VJoyDevice(setting['id'])
        reset(pad)
        sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        sock.bind(('', setting['port']))
        sock.setblocking(False)
        pads.append((pad, sock))

    try:
        while True:
            try:
                for pad, sock in pads:
                    try:
                        message, addr = sock.recvfrom(1024)
                    except BlockingIOError:
                        continue
                    data = json.loads(str(message, encoding='utf8'))
                    # print(data)
                    """
                    {
                      "axes": {
                        "x": 0.25,
                        "y": 0.0,
                        "z": 0.85,
                        "rx": 0.0
                      },
                      "buttons": {
                        "0": 0,
                        "1": 0,
                        "2": 1,
                        "3": 0,
                        "4": 1,
                        "5": 0,
                        "6": 0,
                        "7": 0,
                        "8": 1,
                        "9": 0,
                        "10": 0,
                        "11": 0
                      }
                    }
                    """
                    for axis, value in data["axes"].items():
                        set_axis(pad, axis, value)
                    for button, value in data["buttons"].items():
                        pad.set_button(int(button) + 1, value)
            except KeyboardInterrupt:
                break
    finally:
        print('Closing.')
        for _, sock in pads:
            sock.close()

if __name__ == '__main__':
    main()
