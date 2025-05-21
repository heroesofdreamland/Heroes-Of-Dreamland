import os
import re

#abs path
directory = '../resources/used_resources/units/chaos_incarnatech/tier1/bomb/bomb/idle'

for filename in os.listdir(directory):
    match = re.search(r'(\d{3}\.png)$', filename)
    if match:
        new_filename = match.group(1)
        old_file_path = os.path.join(directory, filename)
        new_file_path = os.path.join(directory, new_filename)
        os.rename(old_file_path, new_file_path)
