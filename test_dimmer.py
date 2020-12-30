import osascript
import time

with open("scripts/brighten.applescript") as brighten_file:
    brighten_script = brighten_file.read()

with open("scripts/dim.applescript") as dim_file:
    dim_script = dim_file.read()


def dim():

    osascript.osascript(dim_script)


def brighten():

    osascript.osascript(brighten_script)

dim()
time.sleep(5)
brighten()