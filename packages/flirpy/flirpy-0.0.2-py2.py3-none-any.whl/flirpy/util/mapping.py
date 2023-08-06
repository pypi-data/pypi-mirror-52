import smopy
import numpy as np
from flirpy.io.fff import Fff

def plot_track(files):

    coords = []

    for f in files:
        frame = Fff(f)
        _, _, lon, lat, alt, _, _, velocity, track =  frame.get_gps()
        coords.append((lat, lon, alt, velocity, track))

    return np.array(coords)