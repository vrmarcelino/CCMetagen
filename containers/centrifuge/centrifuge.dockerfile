## Setup deps

### Blast
FROM ncbi/blast:latest as blast

###### Centrifuge
FROM debian:stretch-slim as centrifuge
RUN apt-get update && apt-get install -y --no-install-recommends  \
    build-essential   \
    ca-certificates   \
    curl              \
    git               \
    liblmdb-dev        # required for blast \
    openssl           \
    python-minimal    \
    wget              \
    zlib1g-dev        \
  && rm -rf /var/lib/apt/lists/* && apt-get autoremove -y && apt-get clean

COPY --from=blast /blast /
ENV PATH="/blast/bin:${PATH}"
ENV CTRFG_DST=/tmp/centrifuge
ENV CTRFG_TAG="v1.0.3"
ENV CTRFG_SRC=https://github.com/infphilo/centrifuge.git
RUN git clone --branch $CTRFG_TAG $CTRFG_SRC $CTRFG_DST &&  \
    cd $CTRFG_DST && make -j10                          &&  \
    make install prefix=/usr/local

ENV CTRF_BASE /cntrf
ENV CTRF_LIBDIR $CTRF_BASE/library
ENV CTRF_TAXDIR $CTRF_BASE/taxonomy
RUN mkdir -p $CTRF_BASE && mkdir $CTRF_LIBDIR && mkdir $CTRF_TAXDIR
WORKDIR /
CMD ["/bin/bash"]

#RUN centrifuge-download -o $CTRF_LIBDIR -a "Contig" -m -d "fungi" refseq > $SEQIDMAP     && \
#    centrifuge-download -o $CTRF_LIBDIR -a "Scaffold" -m -d "fungi" refseq >> SEQIDMAP   && \
#    centrifuge-download -o $CTRF_LIBDIR -a "Chromosome" -m -d "fungi" refseq >> SEQIDMAP && \
#    centrifuge-download -o $CTRF_LIBDIR -m -d "fungi,bacteria" refseq >> SEQIDMAP        && \
#    centrifuge-download -o CTRF_TAXDIR taxonomy
#RUN cat $CTRF_LIBDIR/*/*.fna > input-sequences.fna
#RUN centrifuge-build -p 10 --conversion-table SEQIDMAP --taxonomy-tree $CTRF_TAXDIR/nodes.dmp --name-table $CTRF_TAXDIR/names.dmp input-sequences.fna bacfun_refseq
#FROM alpine:latest
#RUN apk update && apk upgrade
#COPY --from=blast /blast/bin/ /usr/local/bin
