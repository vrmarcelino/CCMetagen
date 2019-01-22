#!/bin/bash
#-------------------------------------------------------------------------------
#  \author Jan P Buchmann <jan.buchmann@sydney.edu.au>
#  \copyright 2019 The University of Sydney
#  \description
#-------------------------------------------------------------------------------
CENTRIFUGE_DOCKER="kmeta_ctrf:latest"
CENTRIFUGE_VOL="ctrf"
CENTRIFUGE_CONTAINERDIR="/cntrf"
CENTRIFUGE_CONTAINER="centrifuge"

DOCKER_BIN=$(which docker)
DOCKER_RUN="${DOCKER_BIN} run"
DOCKER_EXEC="${DOCKER_BIN} exec"
DOCKER_STOP="${DOCKER_BIN} stop"

THREADS=10

function start_centrifuge()
{
  $DOCKER_RUN --detach                                                        \
              --rm                                                            \
              --tty                                                           \
              --name $CENTRIFUGE_CONTAINER                                    \
              --mount source=$CENTRIFUGE_VOL,target=$CENTRIFUGE_CONTAINERDIR  \
              $CENTRIFUGE_DOCKER
}

function stop_centrifuge()
{
  $DOCKER_STOP $CENTRIFUGE_CONTAINER
}

function setupdbs()
{
  local CTRF_LIBDIR=$CENTRIFUGE_CONTAINERDIR/library
  local CTRF_TAXDIR=$CENTRIFUGE_CONTAINERDIR/taxonomy
  local SEQIDMAP="seqid2taxid.map"
  local CENTRIFUGE_DOWNLOAD="centrifuge-download"
  local CMD_DOWNLOAD_LIBS="$CENTRIFUGE_DOWNLOAD -o $CTRF_LIBDIR"

  $DOCKER_EXEC -t $CENTRIFUGE_CONTAINER sh -c "$CMD_DOWNLOAD_LIBS -a \"Contig\"     -m -d \"fungi\" refseq >  $CENTRIFUGE_CONTAINERDIR/$SEQIDMAP"
  $DOCKER_EXEC -t $CENTRIFUGE_CONTAINER sh -c "$CMD_DOWNLOAD_LIBS -a \"Scaffold\"   -m -d \"fungi\" refseq >> $CENTRIFUGE_CONTAINERDIR/$SEQIDMAP"
  $DOCKER_EXEC -t $CENTRIFUGE_CONTAINER sh -c "$CMD_DOWNLOAD_LIBS -a \"Chromosome\" -m -d \"fungi\" refseq >> $CENTRIFUGE_CONTAINERDIR/$SEQIDMAP"
  $DOCKER_EXEC -t $CENTRIFUGE_CONTAINER sh -c "$CMD_DOWNLOAD_LIBS                   -m -d \"fungi\" refseq >> $CENTRIFUGE_CONTAINERDIR/$SEQIDMAP"
  $DOCKER_EXEC -t $CENTRIFUGE_CONTAINER sh -c "$CENTRIFUGE_DOWNLOAD -o $CTRF_TAXDIR taxonomy"
  $DOCKER_EXEC -t $CENTRIFUGE_CONTAINER sh -c "cat $CTRF_LIBDIR/*/*.fna > input-sequences.fna"
  $DOCKER_EXEC -t $CENTRIFUGE_CONTAINER sh -c "centrifuge-build -p $THREADS --conversion-table $CENTRIFUGE_CONTAINERDIR/$SEQIDMAP --taxonomy-tree $CTRF_TAXDIR/nodes.dmp --name-table $CTRF_TAXDIR/names.dmp input-sequences.fna bacfun_refseq"
}

start_centrifuge
setupdbs
stop_centrifuge
