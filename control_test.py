import water_phantom_control

def main():
    wpc = water_phantom_control.WaterPhantomControl(None, use_cylinder=True)
    wpc.move_to_coords_cm(1, 1, 3)

if __name__ == '__main__':
    main()
