from ubuntu:bionic

RUN apt-get update && apt-get install -y \
    vim \
    git \
    wget \
    bc \
    build-essential \
    python \
    openjdk-8-jdk \
    parallel \
    software-properties-common

RUN add-apt-repository -y ppa:ubuntugis/ppa && apt-get update && apt-get install -y gdal-bin

WORKDIR /app
RUN git clone https://github.com/auxiliary/npmap-species

WORKDIR /app
RUN git clone https://github.com/seelabutk/eden 

RUN cd /app/npmap-species/environmentallayers && ./download_environment_layers.sh
RUN cd /app/npmap-species/atbirecords && python separate.py JUST_COORDS

# Change config_all to other configurations if you need to in do_run.sh
RUN cd /app/npmap-species/backend/maxent/ && ./clean.sh && ./run.sh
RUN cd /app/npmap-species/backend/maxent/libfdr/src/ && make
RUN cd /app/npmap-species/backend/maxent/eden_folds/ && . commands
RUN cd /app/npmap-species/environmentallayers && ./convert_asc_to_mxe.sh

# For some reason, only the 2015 environmental layers work. Even if that wasn't the case, you'd want to use one set of environmental layer extracts
# so let's remove the rest
RUN cd /app/npmap-species/environmentallayers && find . -type f -newermt 20150801 ! -newermt 20170101 | sed 's/\.asc/\.mxe/g' | sed 's/\.\//mxe\//g' | xargs -I{} rm {}

# Make sure you have hundreds of GB space if you're doing the whole thing
RUN cd /app/npmap-species/backend/maxent/eden_maxent/ && parallel < commands





ENV PATH="/app/eden/:${PATH}"



    


