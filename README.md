# KMetagen

## Containers

### Repository layout
```
.(gitroot)
|-- containers
|   `-- centrifuge
|       `-- centrifuge.dockerfile
`-- tools
    `-- setup
        `-- centrifuge-setup.sh
```
### Centrifuge

#### Setup

0. Run `tool/setup/centrifuge-setup.sh`

Name                | Type              | Description
--------------------|-------------------|---------------
`centrifuge`        | Docker image      | Basic image
`centrifuge-setup`  | Docker container  | Container for setup
`centrifugeVol`     | Docker volume     | Volume storing databases and indices

`centrifuge.dockerfile` is the Dockerfile to build the basic `centrifuge` image.
This image is run detached as `centrifuge-setup` with the volume `centrifugeVol`
mounted to `/centrifuge` in the container to store the databases and indices.
The setup is calling `docker exec`  to invoke the individual steps required for
the centrifuge setup.

#### Use

Basic example to use centrifuge and mount the corresponding volume to `/centrifuge`:


`docker run --rm -it --mount source=centrifugeVol,target=/centrifuge centrifuge:latest`
