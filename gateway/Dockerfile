#
# Copyright (c) 2017 Intel Corporation
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#      http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
#

FROM debian:jessie

# Allows to set-up HTTP(S) proxy using '--build-arg'
ARG http_proxy
ARG https_proxy

ENV http_proxy ${http_proxy}
ENV https_proxy ${https_proxy}

RUN echo $https_proxy
RUN echo $http_proxy

# Update and install core build tools
RUN apt-get update
RUN apt-get install -y \
    build-essential git scons libtool autoconf \
    valgrind doxygen wget unzip curl

# Install IoTivity build dependencies
RUN apt-get install -y \
    libboost-dev libboost-program-options-dev libboost-thread-dev \
    uuid-dev libexpat1-dev libglib2.0-dev libsqlite3-dev \
    libcurl4-gnutls-dev

# Install npm, nodejs
# the node.js package in Debian Jessie official repositories is too
# old for iotivity-node (> 0.10 required and 0.10.29 provided)
RUN curl -sL https://deb.nodesource.com/setup_6.x | /bin/bash -
RUN apt-get install -y nodejs

# Intall Home Gateway server
RUN mkdir -p /opt/SmartHome-Demo/gateway/
COPY . /opt/SmartHome-Demo/gateway/
WORKDIR /opt/SmartHome-Demo/gateway/

RUN npm install

VOLUME ["/opt/security-files/"]

# Forward port
EXPOSE 8000 8080

# Unset proxy
ENV http_proxy ""
ENV https_proxy ""

# Start Home Gateway
ENTRYPOINT ["/opt/SmartHome-Demo/gateway/start-gateway-in-docker.sh"]

