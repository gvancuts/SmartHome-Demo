# The IoT to Cloud SmartHome demo

This repository provides source code that allows to set-up and demonstrate an IoT to Cloud SmartHome demo leveraging [OCF](http://openconnectivity.org/) and [IoTivity](https://www.iotivity.org/) to communicate between smart appliances (OCF servers), a Home GW (OCF client) and a cloud-based portal (using the [IoT REST API Server]). The user can interact with the various devices via both an Android companion app (when on the local network) and via the cloud portal. For a more comprehensive overview of the architecture and a detailed step-by-step guide on how to put it all together, please take a look at our online [tutorial](https://01.org/smarthome).

## The repository is organised as follows:
* `gateway`: code running on the Home Gateway
* `ocf-servers`: OCF server implementations in JavaScript (located in `js-servers`).
   * Generic documentation on how to set them up is available [here](ocf-servers/js-servers/README.md)
   * The specifications for the OCF servers is availabe in the `ocf-servers/doc/` folder
* `ostro-config`: a collection of `systemd` service files that can help automatically start the Home GW software (on the Home Gateway) and OCF servers (on the OCF server hardware). (*note:* these require manual adaptation and not all OCF servers have an associated service file available)
* `sensors`: source code for the various Smart Devices that are based on the [Zephyr Project](https://www.zephyrproject.org/)
* `smarthome-web-portal`: code for the cloud portal
* `snap`: meta file for packaging the Home Gateway into a [snap](https://www.ubuntu.com/desktop/snappy)
* `package.json`: metadata file for the SmartHome GW and IoT Smart Devices that are implemented in JavaScript. It specifically eases the installation of all modules and dependencies using `npm`.
* `Dockerfile`: this allows to build a [Docker](https://www.docker.com/) container that simulates a Connected Smart Home. Such container will include all OCF servers from `ocf-servers/js-servers/` (running in simulation mode) as well as the Home GW function and the [IoT REST API Server](https://github.com/01org/iot-rest-api-server) to connect to the Cloud Portal (aka `smarthome-web-portal`).

You will find dedicated README.md files in most of these subfolders that will explain in more details how to use their respective contents.

## Instructions for the Docker SmartHome container

Please note that there is another Docker container we make available specifically for the Cloud Portal, please look at this [README.md](./smarthome-web-portal/tools/docker/README.md) file for more details on that.

### Prerequisites

* Install Docker on your host OS following the official documentation at [Docker Platform Installation](https://www.docker.com/products/overview#/install_the_platform).

*Note:* you need to be `root` (`sudo`) by default on most host OSs. The commands listed below assumed you have configured your system so you can run `docker` as a normal user.

* Clone the `SmartHome-Demo` repository
```
$ git clone https://github.com/SmartHome-Demo
$ cd SmartHome-Demo
```

### Getting the SmartHome container
There will be two options available, build it locally or grab it from [Docker Hub](https://hub.docker.com).

#### Building the SmartHome Docker container
**Option 1:** build the Docker container
```
$ docker build -t smarthome:v1 .
```
It will take a little while depending on your host machine as it compiles [IoTivity](https://www.iotivity.org) as part of the build process. If you are behind a proxy, please refer to this [README.md](./smarthome-web-portal/tools/docker/README.md) on how to pass the right variables to `docker`.

**Option 2:** get it from Docker Hub (not yet available)

#### Running the SmartHome Docker container
There are a few ways you can run the container, we will explain a couple of them here.

We recommend using a browser below and if you are using Google Chrome, we would recommend that you install the [JSON Viewer](https://chrome.google.com/webstore/detail/json-viewer/gbmdgpbipfallnflgajpaliibnhdgobh) extension (or similar tool) to make the output look more human-friendly.

**Option 1:** Run the container exposing port 8000 to a different port on your host (e.g. 8001)
```
$ docker run -p 8001:8000 --name my-smarthome smarthome:v1
```
To verify that the virtual SmartHome is available, open you browser and go to http://localhost:8001/api/oic/res.

*Note:* it is not strictly required to use Docker's port publishing (`-p 8001:8000` argument) to access the [IoT REST API Server], you can use the container's IP address directly instead of `localhost`. The container will print out its IP address when it starts, or you can also retrieve it using `docker inspect <container ID>`.

You can also use `curl` if you are familiar with it, e.g. `curl http://localhost:8001/api/oic/res`.

**Option 2:** Run the container directly on the host network
```
$ docker run --network host --name my-smarthome smarthome:v1
```
In this case, you can check that the virtual SmartHome is running by checking http://localhost:8000/api/oic/res

The (alleged, not verified yet) advantage of running with the `--network host` parameter is that the virtual gateway should see other OCF servers available on your local network (not just the ones from your container environment).

*Note:* this uses plain HTTP. It is possible to use HTTPS by modifying the [startup script](gateway/start-smarthome-in-docker.sh) and passing the `-s` parameter to the `iot-rest-api-server` startup script.

[IoT REST API Server]: https://github.com/01org/iot-rest-api-server/
