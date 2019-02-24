#!/bin/bash

set -eu

IMAGE="kaczmarj/neurodocker:master@sha256:936401fe8f677e0d294f688f352cbb643c9693f8de371475de1d593650e42a66"

docker run --rm ${IMAGE} generate docker -b neurodebian:stretch -p apt \
    --dcm2niix version=v1.0.20180622 method=source \
    --install git mercurial gcc pigz liblzma-dev libc-dev netbase nifti2dicom \
    --copy . /src/dcm2dcm \
    --miniconda use_env=base conda_install="python=3.6 numpy nomkl" \
        pip_install="nibabel" \
    --entrypoint "/src/dcm2dcm" \
    --run "chmod +x /src/dcm2dcm" \
> ./Dockerfile
