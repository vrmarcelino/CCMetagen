### Blast
FROM ncbi/blast:latest as blast

### Centrifuge build
FROM debian:stretch-slim as centrifuge_build
RUN apt-get update && apt-get install -y --no-install-recommends  \
    build-essential   \
    ca-certificates   \
    git               \
    openssl           \
  && rm -rf /var/lib/apt/lists/*  && \
     apt-get autoremove -y        && \
     apt-get clean

ENV CTRFG_DST=/tmp/centrifuge
ENV CTRFG_TAG="v1.0.3"
ENV CTRFG_SRC=https://github.com/infphilo/centrifuge.git
RUN git clone --branch $CTRFG_TAG $CTRFG_SRC $CTRFG_DST &&  \
    cd $CTRFG_DST                                       &&  \
    make -j10                                           &&  \
    make install prefix=/usr/local

### Centrifuge
FROM debian:stretch-slim as centrifuge
RUN apt-get update && apt-get install -y --no-install-recommends  \
    curl            \
    ca-certificates \
    libgomp1        \
    liblmdb-dev     \
    openssl         \
    python-minimal  \
    wget            \
  && rm -rf /var/lib/apt/lists/*  && \
     apt-get autoremove -y        && \
     apt-get clean

WORKDIR /
COPY --from=blast /blast blast/
COPY --from=centrifuge_build /usr/local /usr/local
ENV PATH="/blast/bin:${PATH}"
CMD ["/bin/bash"]
