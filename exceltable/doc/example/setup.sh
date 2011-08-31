#!/bin/sh
##=============================================      
## This is a application installation
## script. The comments are formated using RST
##=============================================
# Installation consists from three phases:
#
# 1. Downloading files
# 2. Installation
# 3. Configuration
#
# Create temp directory
CDATE=$(date +%Y-%m-%d)
mkdir -P /tmp/$CDATE

# .. _clear_temp:
#
# In case of existing files, delete the temporary files first
rm -rf /tmp/$CDATA

# Download the package and locate it to ``temp`` directory.
# Finally, extract the package.
cd /tmp/$CDATE
wget http://server.com/downloads/package.tar.gz
tar -xzf package.tar.gz

# .. IMPORTANT::
#
#    In case of upgrade, :ref:`delete the temporary files <clear_temp>`.
#

# Open the config file in editor
vim /etc/application.conf

# Change the parameter ``listen_port`` if needed. The default value is: 8080:: 
#
#   listen_address = "0:0:0:0"
#   listen_port = 8080
#
# Start the service to verify the configuration is valid
service application start

## 

