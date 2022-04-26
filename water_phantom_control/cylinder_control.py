"""Class to control the electric cylinder,
connected to an Arduino via a motor shield,
connected via USB to the PC. Commands are
sent and received via USB-serial"""
import time
import serial
from serial.tools import list_ports

# Constants
VID = '2341:0043'   # Vendor id

class CylinderControl():
    """Establish connection, initialize position,
    move to position
    """
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

    def move_to_position(self, position_percent, in_cm=True, wait=True):
        """Set position in percent. If wait is true,
        function waits until desired position is reached
        """
        if in_cm:
            position = self.cm_to_percent(position_percent)
        else:
            position = position_percent

        if position > 100:
            raise ValueError("Position must not exceed 100%!")
        if position < 0:
            raise ValueError("Position must be greater or equal 0%!")

        self.ser.write(("Z=%.1f\n" % position).encode())
        # Wait until position is reached
        if wait:
            while self.ser.in_waiting <= 0:
                pass

            # Get response
            res = self.ser.readline()[:-2]
            if res == "DONE":
                return True
        return False

    def get_position(self, in_cm=True):
        """Get current position of the cylinder in percent"""
        self.ser.write("GET\n".encode())

        while self.ser.in_waiting <= 0:
            pass

        percent_value = self.ser.readline()[:-2]
        print(percent_value)
        if in_cm:
            return float( self.percent_to_cm( percent_value ).decode() )
        return float( percent_value.decode() )

    def position_reached(self):
        """Check if the cylinder reached its final position,
        i.e., if it is not moving
        """
        self.ser.write("REACHED\n".encode())
        if self.ser.in_waiting <= 0:
            return False

        # Get response
        res = self.ser.readline()[:-2].decode()
        if res == "True":
            return True
        else:
            return False

    @classmethod
    def percent_to_cm(cls, position_percent):
        """Transform percent to cm"""
        return position_percent / 100 * 29.8 + 2.3

    @classmethod
    def cm_to_percent(cls, position_cm):
        """Transform cm to percent"""
        return (position_cm - 2.3) / 29.8 * 100

    # = Connect & Disconnect =
    def connect(self):
        """Establish connection"""
        if self.ser is None:
            self.ser = serial.Serial(
                self.port,
                baudrate=self.baud_rate
            )
            assert self.ser.isOpen(), \
                'Connection could not be established'

    def disconnect(self):
        """Disconnect Arduino"""
        if self.ser is None:
            return

        self.ser.close()
        self.ser = None

    def __del__(self):
        """Destructor"""
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
