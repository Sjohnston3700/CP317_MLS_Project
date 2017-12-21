############################################################
# Dockerfile to build ezMarker Container
# Based on Ubuntu
############################################################

# Set the base image to Ubuntu
FROM ubuntu

# File Author / Maintainer
MAINTAINER Maintaner Name

# Update the sources list
RUN apt-get update

# Install basic applications
RUN apt-get install -y tar git curl nano wget dialog net-tools build-essential

# Install Python and Basic Python Tools
RUN apt-get install -y python3 python-dev python-distribute python3-pip

# Get copy of repo with correct API credentials
ADD /python /python

# Get pip to download and install requirements:
RUN pip3 install -r /python/requirements.txt

# Expose ports
EXPOSE 80

# Set the default directory where CMD will execute
WORKDIR /python

# Set the default command to execute    
# when creating a new container
# i.e. using CherryPy to serve the application
CMD python3 ezMarker.py
