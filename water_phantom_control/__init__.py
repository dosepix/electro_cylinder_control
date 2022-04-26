"""Module to control the axes of the water phantom"""
from . import cylinder_control
from . import motor_control

class WaterPhantomControl():
    """Class to control the axes"""
    def __init__(self,
        cylinder_port,
        use_cylinder=True
    ):
        self.use_cylinder = use_cylinder
        
        # Connect to arduino of cylinder
        if self.use_cylinder:
            if cylinder_port is None:
                port = cylinder_control.find_port()
            else:
                port = cylinder_port

            self.cc = cylinder_control.CylinderControl(
                port,
                baud_rate=9600
            )
            self.cc.move_to_position(0, in_cm=False, wait=False)

        self.mc = motor_control.MotorControl()
        self.mc.move_to_initial()
        self.position_reached()

    def move_to_coords_cm(self, x_pos, y_pos, z_pos, block=True):
        """Move axes to coordinates in cm. If block is True,
        execution halts until positions are reached
        """
        self.mc.move_to_cm(x_pos, top=True)
        self.mc.move_to_cm(y_pos, top=False)
        if self.use_cylinder:
            self.cc.move_to_position(abs(z_pos), in_cm=True, wait=False)

        if block:
            while not self.position_reached():
                pass

    def position_reached(self):
        """Check if axes reached their positions"""
        pos_reached_mc =  self.mc.position_reached()
        if self.use_cylinder:
            pos_reached_cyl = self.cc.position_reached()
            return pos_reached_mc and pos_reached_cyl
        return pos_reached_mc
