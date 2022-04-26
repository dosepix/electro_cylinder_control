import water_phantom_control

def main():
    # Establish connections, move to initial positions
    wpc = water_phantom_control.WaterPhantomControl(None, use_cylinder=True)

    # Move axes
    wpc.move_to_coords_cm(1, 1, 3)

if __name__ == '__main__':
    main()
