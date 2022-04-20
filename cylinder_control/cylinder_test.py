#!/usr/bin/env python
import cylinder_control

PORT = 'COMX'

def main():
    port = cylinder_control.find_port()
    print(port)
    if port is None:
        port = PORT

    cc = cylinder_control.CylinderControl(
        port,
        baud_rate=9600
    )

    positions = [10, 50, 90, 50, 10]
    for position in positions:
        cc.move_to_position(position)
        print( cc.get_position() )

if __name__ == '__main__':
    main()
