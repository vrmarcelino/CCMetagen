## Kraken 2 build
FROM debian:stretch-slim as kraken2_build
RUN apt-get update && apt-get install -y --no-install-recommends  \
    build-essential   \
    ca-certificates   \
    git               \
    openssl           \
  && rm -rf /var/lib/apt/lists/*  && \
     apt-get autoremove -y        && \
     apt-get clean

ARG VERSION
ENV VERSION ${VERSION:-v2.0.7-beta}
ARG MAKE_JOBS
ENV MAKE_JOBS ${MAKE_JOBS:-2}
ENV KRK_DST /tmp/kraken
ENV KRK_DIR /kraken2
ENV KRK_SRC https://github.com/DerrickWood/kraken2.git
RUN git clone --branch $VERSION $KRK_SRC $KRK_DST
WORKDIR $KRK_DST
RUN sh -c 'bash install_kraken2.sh $KRK_DIR'

FROM ncbi/blast:latest as blast
FROM debian:stretch-slim as kraken2
ENV KRK_DIR /kraken2
RUN apt-get update && apt-get install -y --no-install-recommends  \
    rsync           \
    ca-certificates \
    liblmdb-dev     \
    openssl         \
    wget            \
  && rm -rf /var/lib/apt/lists/*  && \
     apt-get autoremove -y        && \
     apt-get clean

COPY --from=kraken2_build $KRK_DIR/ $KRK_DIR/
COPY --from=blast /blast/ blast/
ENV PATH "${KRK_DIR}:/blast/bin:${PATH}"
CMD ["/bin/bash"]
