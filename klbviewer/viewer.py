import pyklb
import numpy as np
import napari
import sys
import os.path


def load_data(filename):
    return pyklb.readfull(filename)

def shift_time(filename, dt):
    splits = filename.split("TM")

    if len(splits) > 0:
        time = int(splits[1][:6]) + dt
        # reassemble new file name
        for i in range(1, len(splits)):
            splits[i] = f"{time:06}" + splits[i][6:] 

        new_filename = "TM".join(splits)

    if os.path.isfile(new_filename):
        return new_filename
    else: 
        print("next file does not exist!")
        return None

def find_all_channels(filename):
    if "CHN" not in filename:
        return [filename]

    channel_filenames = []
    splits = filename.split("CHN")
    for channel_number in range(100):
        splits[1] = f"{channel_number:02}" + splits[1][2:] 
        new_filename = "CHN".join(splits)
        if os.path.isfile(new_filename):
            channel_filenames.append(new_filename)

    return channel_filenames


def klb_viewer(filename):
    with napari.gui_qt(): 
        viewer = napari.Viewer()
        filenames = find_all_channels(filename)

        for fn in filenames:
            data = load_data(fn)
            viewer.add_image(data, scale=(4, 1, 1), name=fn)

        @viewer.bind_key('p')
        def load_next_frame(viewer):
            for i in range(len(viewer.layers)):
                new_filename = shift_time(viewer.layers[i].name, 1)
                if new_filename is not None:
                    viewer.layers[i].data = load_data(new_filename)

        @viewer.bind_key('o')
        def load_next_frame(viewer):
            for i in range(len(viewer.layers)):
                new_filename = shift_time(viewer.layers[i].name, -1)
                if new_filename is not None:
                    viewer.layers[i].data = load_data(new_filename)

if __name__ == '__main__':
    
    if len(sys.argv) > 1:
        filename = sys.argv[1]
        klb_viewer(filename)

