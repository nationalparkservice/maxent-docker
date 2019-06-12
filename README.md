# maxent-docker

This repository serves as the hub for Docker related files to setup the backend for Species mapper.

## Prerequisites 
* [Docker](https://github.com/wsargent/docker-cheat-sheet/blob/master/README.md)

## Quick Start
#### Build
`./npsdocker.sh build`
####'Windows Powershell: docker build ['folder where Dockerfile is]'

#### Run
`./npsdocker.sh run`

#### Run and Upload to MapBox
`./npsdocker.sh -u MB_USER MB_ACCESS_TOKEN run`

#### Run, Upload to MapBox and Dump
`./npsdocker.sh -u MB_USER MB_ACCESS_TOKEN -d run`

#### Run only for selected species, upload to Mapbox and Dump
`./npsdocker.sh -u MB_USER MB_ACCESS_TOKEN -d -c run`

## build - Building the Docker Image
Provided is a shell script that will generate the image for you. Clone this repository to the computer with docker, use the shell script provided, npsdocker.sh, to build an image.

### Standard Build
`./npsdocker.sh build`
* Builds a Docker Image named npsbe
* This step may take anywhere from 10-15 minutes.
* On Step 13/15 errors may occur if CartoDB is busy (throws an error 403 from python's urllib)
  * Wait 10-20 minutes then re-run build script

### Fresh Build
`./npsdocker.sh freshBuild`
* Removes a the previous Docker Image and builds one from scratch, this is equivalent to running build for the first time.
* This is not intended to be used often, just here incase the npmap-species code is updated and the image is outdated.

## run - Running the Docker Image
Provided is a shell script that will run an instance of a built image for you. Clone this repository to the computer with docker, use the shell script provided, npsdocker.sh, to build an image. After uploading environmental data, one may then use the run command to launch an instance of the image and perform the necessary computations for maxent.

### Preliminary
* Before Running, look at the project folder heirarchy:
```
    . <- Current Folder
    ├── Dockerfile                  # Dockerfile that sets up max-ent and backend
    ├── npsdocker.sh                # Helper script to build and run a Docker Instance
    └── mountdata                   # Default mounted volume, folder where data is uploaded and output is dumped
      ├── ENVIRONMENTS.zip          # Uploaded ENVIRONMENTS.zip, a zip containing *no folders*, only .asc files
      └── config.txt (optional)     # An optional config.txt, to run maxent on select species
```

#### mountdata
This is the default mounted volume (change this folder from default `mountdata` if so desired with the `-v` or `--volume` flag). The Docker instance expects to find `ENVIRONMENTS.zip` here, optionally there may be a config.txt here as well. Output from maxent and eden will be placed here if requested with the `d` or `--dump` flag.

##### ENVIRONMENTS.zip
This is the data that is fed to maxent. It is a zip of `.asc` files, it should contain no folders or subfolders. When unzipped, it should be `.asc` files only.

##### config.txt
This is an optional configuration file. It is a text file, first naming the number of folds then listing names of species that will be ran through maxent. If no config file is specified, all species will be simulated.
Here is the format of `config.txt`:
```
10                              <- Number of folds, advised to keep it at 10
Catocala_ilia                   <- Scientific name of species with spaces replaced with underscore
Luzula_acuminata_variety
Ephemerella_invaria_group
Eutyphlus_similis
Xestia_normaniana
Lochmaeus_manteo
Acentrella_ampla
Calycanthus_floridus_v_glaucus
```

### run flags
#### -u MB_USER MB_ACCESS_TOKEN
To avoid putting public access tokens in plain text, username and access token is passed to the run script. `-u` stands for upload. Without this flag, it will not upload output to mapbox.
Example:

* `./npsdocker.sh -u pprovins sk.ThisIsAPrivateAccessToken run`
  * Uploads to mapbox account `pprovins` using the access token `sk.ThisIsAPrivateAccessToken`

#### -d
To dump the outputs of the computations onto disk, use the `-d` flag. The mounted volume, `mountdata`, will contain the dump inside `mountdata/output`.
Example:

* `./npsdocker.sh -d run`
  * This creates a dump to `mountdata/output`
* `./npsdocker.sh -u pprovins sk.ThisIsAPrivateAccessToken -d run`
  * This uploads the output to mapbox as well as dumps the data to `mountdata/output`

#### -c
If a full simulation is not necessary (only a few species are wanted to be updated), the `-c` flag allows those species to be specified. If `-c` is specified, there is expected to be a `config.txt` to be found in `mountdata` (see preliminary for such an example). Example:

* `./npsdocker.sh -c run`
  * This runs a simulation over species specified by `config.txt` in `mountdata`
* `./npsdocker.sh -d -c run`
  * This creates a dump to `mountdata/output` of species specified by `config.txt` in `mountdata`
* `./npsdocker.sh -u pprovins sk.ThisIsAPrivateAccessToken -c run`
  * This uploads the output to mapbox for the simulation over species specified by `config.txt` in `mountdata`
* `./npsdocker.sh -u pprovins sk.ThisIsAPrivateAccessToken -c -d run`
  * This uploads the output to mapbox for the simulation over species specified by `config.txt` in `mountdata` and creates a dump as well.
