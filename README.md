# dcm2dcm

Convert DICOM images to DICOM images by way of NIFTI

## Overview

This script and accompanying Docker image convert a DICOM source (one or more
images) to a DICOM target using NIFTI as an intermediate.  This process can
have a variety of effects, among them removing information that was embedded in
the original DICOM headers.

## Approach

Two open-source image-processing tools are used: `dcm2niix` and `nifti2dicom`.
A python script wraps the two tools and generates a temporary directory where
the temporary NIFTI files are written.

## Usage

Script
```
usage: dcm2dcm.py [-h] [--src SRC] [--dst DST]

optional arguments:
  -h, --help  show this help message and exit
  --src SRC   Source of existing DICOM data
  --dst DST   Dest. for new DICOM data
```

Via Docker
```
docker run \
    --rm -it \
    -v /path/to/src:/work davidewarrenphd/dcm2dcm
        --src /work/src \
        --dst /work/dst
```
