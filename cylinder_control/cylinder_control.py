import time
import serial
from serial.tools import list_ports

# Constants
VID = '2341:0043'   # Vendor id

class CylinderControl():
    def __init__(
        self,
        port,
        baud_rate=9600
    ):
        self.port = port
        self.baud_rate = baud_rate
        self.ser = None

        self.connect()
        # Wait for connection
        time.sleep(2)

    def move_to_position(self, position, wait=True):
        """Set position in percent. If wait is true,
        function waits until desired position is reached
        """
        if position > 100:
            raise ValueError("Position must not exceed 100%!")
        if position < 0:
            raise ValueError("Position must be greater than 0%!")

        self.ser.write("Z=%.1f\n" % position)
        # Wait until position is reached
        if wait:
            while self.ser.in_waiting <= 0:
                pass

            # Get response
            res = self.ser.readline()[:-2]
            if res == "DONE":
                return True
        return False

    def get_position(self):
        """Get current position of the cylinder in percent"""
        print( self.ser.isOpen() )
        self.ser.write("GET\n")

        while self.ser.in_waiting <= 0:
            pass

        return self.ser.readline()[:-2]

    # = Connect & Disconnect =
    def connect(self):
        if self.ser is None:
            self.ser = serial.Serial(
                self.port,
                baudrate=self.baud_rate
            )
            assert self.ser.isOpen(), \
                'Connection could not be established'

    def disconnect(self):
        if self.ser is None:
            return

        self.ser.close()
        self.ser = None

    def __del__(self):
        self.disconnect()

def find_port():
    """Find port with correct hwid to establish connection"""
    for port in list_ports.comports():
        chars = port.hwid.split(' ')

        # USB device check
        if chars[0] != 'USB':
            continue

        # Vendor check
        vendor = chars[1][8:]
        if vendor != VID:
            continue
        return port.device
    return None
