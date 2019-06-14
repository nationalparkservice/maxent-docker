# Windows Docker Helper

### Preliminary
* Before Running, look at the project folder heirarchy:
```
    . <- Current Folder
    ├── Dockerfile                  # Dockerfile that sets up max-ent and backend
    ├── main.exe                    # Helper script to build and run a Docker Instance
    └── mountdata                   # Default mounted volume, folder where data is uploaded and output is dumped
      ├── ENVIRONMENTS.zip          # Uploaded ENVIRONMENTS.zip, a zip containing *no folders*, only .asc files
      └── config.txt (optional)     # An optional config.txt, to run maxent on select species
```

### Obtaining Main.exe

Current release of the executable can be found at the releases tab at the [maxent docker github repo](https://github.com/nationalparkservice/maxent-docker).

### Build Button

If a Docker Image has not been created, this button will do so for you.
* Window will become unresponive when building. This is normal.
* Progress of the build will display on the terminal window that accompanies the GUI.

### Run Button

Once a Docker Image has been created, the image may be ran.
* Window will become unresponive when ran. This is normal.
* Progress of the run will display on the terminal window that accompanies the GUI.

### Option Buttons

Before running, there are checkboxes denoting options for the run:
* Upload - Check this box and fill the username and token spots to upload to desired mapbox user
* Config - Check this box and a simulation will be ran over the specified species in /mountdata/config.txt
* Dump   - Check this box and outputs of the simulation will be dumped to hard drive
