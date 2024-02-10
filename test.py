from screeninfo import get_monitors

monitors = get_monitors()
for m in range(len(monitors)):
    if monitors[m].is_primary==True:
        monitor = monitors[m]
dpi_x = monitor.width/monitor.width_mm
dpi_y = monitor.height/monitor.height_mm