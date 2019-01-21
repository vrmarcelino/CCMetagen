## Setup deps

###### Centrifuge
FROM debian:stretch-slim as centrifuge
RUN apt-get update && apt-get install -y --no-install-recommends  \
    build-essential wget git openssl ca-certificates zlib1g-dev   \
  && rm -rf /var/lib/apt/lists/* && apt-get autoremove -y && apt-get clean

ENV DST=/tmp/centrifuge
ENV TAG="v1.0.3"
ENV SRC=https://github.com/infphilo/centrifuge.git
RUN git clone --branch $TAG $SRC $DST && cd $DST && make -j3 && make install prefix=/usr/local

### Blast
FROM ncbi/blast:latest as blast
COPY --from=centrifuge /usr/local/bin /usr/local/bin

ENV VAR CTRF_LIBDIR=/library
ENV VAR CTRF_TAXDIR=/taxonomy
ENV VAR SEQIDMAP=seqid2taxid.map

RUN mkdir /library
RUN centrifuge-download -o $CTRF_LIBDIR -a "Contig" -m -d "fungi" refseq > $SEQIDMAP     &&
    centrifuge-download -o $CTRF_LIBDIR -a "Scaffold" -m -d "fungi" refseq >> SEQIDMAP   &&
    centrifuge-download -o $CTRF_LIBDIR -a "Chromosome" -m -d "fungi" refseq >> SEQIDMAP &&
    centrifuge-download -o $CTRF_LIBDIR -m -d "fungi,bacteria" refseq >> SEQIDMAP        &&
    centrifuge-download -o CTRF_TAXDIR taxonomy
RUN cat $CTRF_LIBDIR/*/*.fna > input-sequences.fna
RUN centrifuge-build -p 3 --conversion-table SEQIDMAP --taxonomy-tree $CTRF_TAXDIR/nodes.dmp --name-table $CTRF_TAXDIR/names.dmp input-sequences.fna bacfun_refseq

#FROM alpine:latest
#RUN apk update && apk upgrade
#COPY --from=blast /blast/bin/ /usr/local/bin
