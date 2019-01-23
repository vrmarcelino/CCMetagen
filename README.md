# KMetagen

## Containers

### Repository layout
```
.(gitroot)
|-- containers
|   |-- centrifuge
|   |   `-- centrifuge.dockerfile
|   `-- kraken2
|       `-- kraken2.dockerfile
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

#### Usage

Basic example to use centrifuge and mount the corresponding volume to `/centrifuge`:

`docker run --rm -it --mount source=centrifugeVol,target=/centrifuge centrifuge:latest`

### Kraken2

A basic Docker container for kraken2.

#### Usage

`docker run --rm -t kraken2:latest kraken2`
