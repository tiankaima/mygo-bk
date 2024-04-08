import os

# read from template.html:
with open("template.html", "r") as file:
    template = file.read()

# replace REPLACE_THIS_INDEX with 1 -> 13, and write each to ./video/_id_.html, 2 digits
export_path = "./video"
for i in range(1, 14):
    with open(f"{export_path}/{str(i).zfill(2)}.html", "w") as file:
        file.write(template.replace("REPLACE_THIS_INDEX", str(i).zfill(2)))
