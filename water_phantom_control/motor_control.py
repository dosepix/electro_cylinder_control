"""Class to control the stepper motors, resembling the
horizontal axes of the water phantom. The motors are
connected to the TMCM-6110 PCB that is connected via USB
to the PC
"""
import time
import pytrinamic
from pytrinamic.connections import ConnectionManager
from pytrinamic.modules import TMCM6110

class MotorControl():
    """Establish connection, initialize position,
    move to position
    """
    def __init__(self):
        connectionManager = ConnectionManager()
        self.interface = connectionManager.connect()
        self.module = TMCM6110(self.interface)
        self.module.set_global_parameter(
            self.module.GP0.EndSwitchPolarity, 0, 1)

        # Get motors
        self.motor_top = self.module.motors[0]
        self.motor_bottom = self.module.motors[1]

        # Stop motors when already driving
        self.motor_top.stop()
        self.motor_bottom.stop()

        # Apply settings to motors
        self.apply_settings()

    class SETTINGS:
        """Settings"""
        MAX_DIST_TOP = 20 # cm
        MAX_DIST_BOTTOM = 30 # cm
        MAX_VELOCITY = 500
        MAX_VELOCITY_SEARCH = MAX_VELOCITY // 5
        NUM_MICROSTEPS = 64

    def apply_settings(self):
        """Apply the settings to the connected motors"""
        for motor in [self.motor_top, self.motor_bottom]:
            motor.drive_settings.max_current = 250
            motor.drive_settings.max_velocity = self.SETTINGS.MAX_VELOCITY
            motor.drive_settings.standby_current = 0
            motor.drive_settings.boost_current = 0
            motor.drive_settings.microstep_resolution =\
                motor.ENUM.microstep_resolution_64_microsteps
                # microstep_resolution_fullstep

            motor.max_acceleration = 1000
            # motor.actual_position = 0

            motor.set_axis_parameter(motor.AP.LeftLimitSwitchDisable, 0)
            motor.set_axis_parameter(motor.AP.RightLimitSwitchDisable, 1)

            # Reference search
            motor.set_axis_parameter(motor.AP.ReferenceSearchMode, 1)
            motor.set_axis_parameter(
                motor.AP.ReferenceSearchSpeed, self.SETTINGS.MAX_VELOCITY)
            motor.set_axis_parameter(
                motor.AP.ReferenceSwitchSpeed, self.SETTINGS.MAX_VELOCITY_SEARCH)

    def microsteps_to_cm(self, dist):
        """Transform microsteps to cm"""
        return (dist / self.SETTINGS.NUM_MICROSTEPS) * 0.01

    def cm_to_microsteps(self, dist):
        """Transform cm to microsteps"""
        return dist * 10 * 100 * self.SETTINGS.NUM_MICROSTEPS

    def move_to_cm(self, dist, top=True):
        """Move motor to dist. Select motor by
        setting top to either True or False"""
        if top:
            assert dist <= self.SETTINGS.MAX_DIST_TOP,\
                "Chosen distance is out of range!"
            motor = self.motor_top
        else:
            assert dist <= self.SETTINGS.MAX_DIST_BOTTOM,\
                "Chosen distance is out of range!"
            motor = self.motor_bottom

        dist_micro_steps = self.cm_to_microsteps(dist)
        motor.move_to(dist_micro_steps, self.SETTINGS.MAX_VELOCITY)

    def move_to_initial(self):
        """Move motors to their initial positions"""
        # Drive to reference position
        for motor_id in [0, 1]:
            self.interface.send(13, 0, motor_id, 0)

        # Wait until end position is reached
        while self.motor_top.get_axis_parameter(self.motor_top.AP.LeftEndstop) < 1 and\
            self.motor_bottom.get_axis_parameter(self.motor_bottom.AP.LeftEndstop) < 1:
            continue
        time.sleep(1)

        self.motor_top.actual_position = 0
        self.motor_bottom.actual_position = 0

    def position_reached(self):
        """Check if motors reached the desired positions"""
        return self.motor_top.get_position_reached()\
            and self.motor_bottom.get_position_reached()
