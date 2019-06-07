from ubuntu:bionic

RUN apt-get update && apt-get install -y \
    vim \
    git \
    wget \
    bc \
    build-essential \
    python \
    python-pip \
    openjdk-8-jdk \
    parallel \
    unzip \
    software-properties-common

RUN add-apt-repository -y ppa:ubuntugis/ppa && apt-get update && apt-get install -y gdal-bin

RUN pip install mapbox mapboxcli

WORKDIR /app
RUN git clone https://github.com/3PIV/npmap-species

WORKDIR /app
RUN git clone https://github.com/seelabutk/eden 

ENV PATH="/app/eden/:${PATH}"

RUN mkdir /app/data

# Handle fetching the environmental layers
RUN cd /app/npmap-species/backend/maxent/libfdr/src/ && make
RUN cd /app/npmap-species/backend/maxent && make
RUN cd /app/npmap-species/atbirecords && python separate.py JUST_COORDS

# Change config_all to other configurations if you need to in do_run.sh
RUN cd /app/npmap-species/backend/maxent/ && ./clean.sh 

ENTRYPOINT ["/app/npmap-species/dockerrun.sh"]
