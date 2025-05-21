import plistlib
from PIL import Image
import os

#abs path
animated_objects = ['../resources/used_resources/units/chaos_incarnatech/tier1/bomb/bomb']

for sp in animated_objects:
    print(sp)
    plist_file = sp + '.plist'
    with open(plist_file, "rb") as file:
        plist_data = plistlib.load(file)

    # Get sprites data
    sprites_data = plist_data["frames"]

    # Process sprite data
    for sprite_name, sprite_info in sprites_data.items():
        frame_string = sprite_info["frame"]
        sprite_x, sprite_y, sprite_width, sprite_height = map(int, frame_string.strip("{}").replace("},{", ",").split(","))

        # Load sprite sheet
        sprite_sheet_path = sp + '.png'
        sprite_sheet = Image.open(sprite_sheet_path)

        # Crop sprite
        sprite = sprite_sheet.crop((sprite_x, sprite_y, sprite_x + sprite_width, sprite_y + sprite_height))

        # Get the type of the sprite from the filename
        sprite_type = sprite_name.split("_")[-2]

        # Create the output folder if it doesn't exist
        output_folder =  sp + '/' + sprite_type
        os.makedirs(output_folder, exist_ok=True)

        # Save sprite to a separate file
        sprite_save_path = f"{output_folder}/{sprite_name}"
        sprite.save(sprite_save_path)