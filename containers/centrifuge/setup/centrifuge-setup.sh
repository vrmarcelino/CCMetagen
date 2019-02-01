#!/bin/bash
#-------------------------------------------------------------------------------
#  \author Jan P Buchmann <jan.buchmann@sydney.edu.au>
#  \copyright 2019 The University of Sydney
#-------------------------------------------------------------------------------

DOCKER_BIN=$(which docker)
DOCKER_BUILD="$DOCKER_BIN build"
DOCKER_RUN="${DOCKER_BIN} run"
DOCKER_EXEC="${DOCKER_BIN} exec"
DOCKER_STOP="${DOCKER_BIN} stop"

DOCKERFILES="${0%/*}/../../containers"
DOCKERFILE="$DOCKERFILES/centrifuge/centrifuge.dockerfile"
IMAGE="centrifuge"
IMAGE_TAG="latest"
CENTRIFUGE_VOL="centrifugeVol"
CENTRIFUGE_CONTAINERMNT="/centrifuge"
VERSION=v1.0.3
MAKE_JOBS=10
CONTAINERID="$IMAGE-setup"

function make_container()
{
  $DOCKER_BUILD --force-rm                        \
                --build-arg VERSION=$VERSION      \
                --build-arg MAKE_JOBS=$MAKE_JOBS  \
                 -t $IMAGE                        \
                 -f $DOCKERFILE .
}

function start_centrifuge()
{
  $DOCKER_RUN --detach                                                        \
              --rm                                                            \
              --tty                                                           \
              --name $CONTAINERID                                             \
              --mount source=$CENTRIFUGE_VOL,target=$CENTRIFUGE_CONTAINERMNT  \
              $IMAGE:$IMAGE_TAG
}

function stop_centrifuge()
{
  $DOCKER_STOP $CONTAINERID
}

function setup_centrifuge()
{
  local CTRF_LIBDIR=$CENTRIFUGE_CONTAINERMNT/library
  local CTRF_TAXDIR=$CENTRIFUGE_CONTAINERMNT/taxonomy
  local SEQIDMAP="seqid2taxid.map"
  local CENTRIFUGE_DOWNLOAD="centrifuge-download"
  local CMD_DOWNLOAD_LIBS="$CENTRIFUGE_DOWNLOAD -o $CTRF_LIBDIR"
  local INPUTSEQ="input-sequences.fna"
  $DOCKER_EXEC -t $CONTAINERID sh -c "$CMD_DOWNLOAD_LIBS -a \"Contig\"     -m -d \"fungi\" refseq >  $CENTRIFUGE_CONTAINERMNT/$SEQIDMAP"
  $DOCKER_EXEC -t $CONTAINERID sh -c "$CMD_DOWNLOAD_LIBS -a \"Scaffold\"   -m -d \"fungi\" refseq >> $CENTRIFUGE_CONTAINERMNT/$SEQIDMAP"
  $DOCKER_EXEC -t $CONTAINERID sh -c "$CMD_DOWNLOAD_LIBS -a \"Chromosome\" -m -d \"fungi\" refseq >> $CENTRIFUGE_CONTAINERMNT/$SEQIDMAP"
  $DOCKER_EXEC -t $CONTAINERID sh -c "$CMD_DOWNLOAD_LIBS                   -m -d \"fungi\" refseq >> $CENTRIFUGE_CONTAINERMNT/$SEQIDMAP"
  $DOCKER_EXEC -t $CONTAINERID sh -c "$CENTRIFUGE_DOWNLOAD -o $CTRF_TAXDIR taxonomy"
  $DOCKER_EXEC -t $CONTAINERID sh -c "cat $CTRF_LIBDIR/*/*.fna > $INPUTSEQ"
  $DOCKER_EXEC -t $CONTAINERID sh -c "centrifuge-build -p $MAKE_JOBS --conversion-table $CENTRIFUGE_CONTAINERMNT/$SEQIDMAP --taxonomy-tree $CTRF_TAXDIR/nodes.dmp --name-table $CTRF_TAXDIR/names.dmp $INPUTSEQ bacfun_refseq"
}

make_container
start_centrifuge
setup_centrifuge
stop_centrifuge
