import argparse
import json
import os
import pygame
import socket
import sys


def main():
    parser = argparse.ArgumentParser(description='Emulate gamepads from afar.')
    parser.add_argument('setup', nargs='?', default='setup_client.json', help='The setup JSON')
    args = parser.parse_args()
    if not os.path.exists(args.setup):
        print('Setup file does not exits.')
        sys.exit(1)

    with open(args.setup) as f:
        setup = json.load(f)

    pygame.init()
    pygame.joystick.init()

    for i in range(pygame.joystick.get_count()):
        joystick = pygame.joystick.Joystick(i)
        joystick.init()
        print('{}: {}'.format(i, joystick.get_name()))

    pad = pygame.joystick.Joystick(setup['id'])
    pad.init()

    axes = [int(axis) for axis in setup['axes'].keys()]
    buttons = [int(button) for button in setup['buttons'].keys()]

    sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

    try:
        while True:
            pygame.event.get()
            state = {'axes': {}, 'buttons': {}}

            for axis in axes:
                value = pad.get_axis(axis)
                mapped = setup['axes'][str(axis)]
                state['axes'][mapped] = value

            for button in buttons:
                value = pad.get_button(button)
                mapped = setup['buttons'][str(button)]
                state['buttons'][mapped] = value
            # print(state)

            sock.sendto(bytes(json.dumps(state), encoding='utf8'), (setup['address'], setup['port']))
    except KeyboardInterrupt:
        print('Exiting.')
        pygame.quit()
    finally:
        print('Closing.')
        pygame.quit()
        sock.close()

if __name__ == '__main__':
    main()
