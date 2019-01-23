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

ARG VERSION
ENV VERSION ${VERSION:-v1.0.3}
ARG MAKE_JOBS
ENV MAKE_JOBS ${MAKE_JOBS:-2}
ENV CTRFG_DST /tmp/centrifuge
ENV CTRFG_SRC https://github.com/infphilo/centrifuge.git
RUN git clone --branch $VERSION $CTRFG_SRC $CTRFG_DST &&  \
    cd $CTRFG_DST                                     &&  \
    make -j $MAKE_JOBS                                &&  \
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
ENV PATH "/blast/bin:${PATH}"
CMD ["/bin/bash"]
