# Run in Krita client. Must be in .kra. There are 2 things indicated below that need to be changed before use.

from krita import *
import os
from pathlib import Path


document = Krita.instance().activeDocument()
path = "C:/Users/username/Documents"  # Yes I use Windows

if document:
    webpOptions=InfoObject()
    webpOptions.setProperty('quality', 80)
    webpOptions.setProperty('preset', "default")
    webpOptions.setProperty('lossless', 0)
    webpOptions.setProperty('tradeoff', 6)
    webpOptions.setProperty('dithering', True)
    webpOptions.setProperty('haveAnimation', False)

    original_width = document.width()
    original_height = document.height()
    project_name = document.fileName().split(".")[0].split('\\')[-1]

    # I personally have a folder with the artwork's filename,
    # and all the resized versions inside it with starting
    # with the same filename, like "NiceDrawing/NiceDrawing.webp".

    # CHANGE the file path to the directory you expect the resized images to be inside.
    target_base_path = f"{path}/{project_name}"
    target_path = f"{target_base_path}/{project_name}"

    # CHANGE this to what you need. Hardcoded because I cannot be bothered to make a plugin that takes inputs.
    widths_to_save = [148, 254, 199, 240, 307, 340]

    # Check if the folder exists and create it if it doesn't
    if not os.path.exists(target_base_path):
        try:
            os.makedirs(target_base_path)
            print(f"Created folder: {target_base_path}")
        except OSError as e:
            print(f"Error creating folder '{target_base_path}': {e}", "Error")
            exit() # Stop the script if folder creation fails

    # export original size
    document.setBatchmode(True)
    document.exportImage(target_path + '.webp', webpOptions)
    print(f"Exported: {target_path}.webp")

    # export resized
    for width in widths_to_save:
        if width > 0 and original_width > 0:
            height = int(original_height * width / original_width)
            scaled_document = document.clone()
            scaled_document.scaleImage(width, height, 0 ,0, 'auto')
            new_filepath = f"{target_path}-{width}.webp"
            print(f"Exported: {new_filepath}")
            scaled_document.exportImage(new_filepath, webpOptions)
        else:
            print(f"Skipping invalid width: {width}")
else:
    print("No active document found.", "Warning")
   

# Reset batch mode setting or your other exports outside the script will be weird
document.setBatchmode(False)