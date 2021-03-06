#!/usr/bin/env python
import argparse
import glob
import logging
import os
import subprocess
import sys
import tempfile

from collections import namedtuple
from os.path import join as opj


def convert_src_to_nifti(src_dir, dst_dir):
    '''Converts the DICOM data in src_dir to NIFTI under dst_dir.'''
    cmd_str = f'dcm2niix -z y -o {dst_dir} {src_dir}'
    subprocess.run(cmd_str.split())


def convert_nifti_to_dicom(src_dir, dst_dir):
    '''Converts the DICOM data in src_dir to NIFTI under dst_dir.'''
    nifti_paths = (glob.glob(opj(src_dir, '*.nii.gz')) +
                   glob.glob(opj(src_dir, '*.nii')))
    for nifti_path in nifti_paths:
        try:
            nifti_bits = decompose_neuro_path(nifti_path)
        except ValueError as e:
            print(e)
            continue
        cmd_str = (f'nifti2dicom '
                   f'-i {nifti_path} '
                   f'-o {opj(dst_dir, nifti_bits.prefix)} '
                   f'-p {nifti_bits.prefix}- '
                   f'--accessionnumber 1 '
                   f'--patientname "NA" '
                   f'--seriesdescription {nifti_bits.prefix} '
                   f'--patientdob "19700101" '
                   f'--patientid 1')
        subprocess.run(cmd_str.split())


def decompose_neuro_path(path):
    '''Return a decomposed neuroimaging data path.'''
    import re
    NeuroPath = namedtuple('NeuroPath', 'dir fn prefix ext afspace compressed')
    directory, fn = os.path.split(path)
    NEURO_EXTS = '|'.join('nii head brik gii mgh mgz img hdr mnc'.split())
    neuro_restr = (r'^'
                   r'(?P<prefix>.+?)'
                   r'(?P<afspace>\+(orig|tlrc))?'
                   r'(?P<ext>.({})+(.gz)?)'
                   r'$').format(NEURO_EXTS)
    neuro_regex = re.compile(neuro_restr, re.I)
    match = neuro_regex.match(fn)
    if match is None:
        raise ValueError('Not a neuro path.')
    prefix, afspace, ext = [match.groupdict().get(i) for i in
                            'prefix afspace ext'.split()]
    compressed = any([ext.lower().endswith(i) for i in ('.gz', '.mgz')])
    return NeuroPath(directory, fn, prefix, ext, afspace, compressed)


def main(src, dst):
    '''Main function for dcm2dcm.'''
    assert os.path.isdir(src)
    assert os.path.isdir(dst)
    with tempfile.TemporaryDirectory() as tmpd:
        convert_src_to_nifti(src, tmpd)
        convert_nifti_to_dicom(tmpd, dst)


def parse_args():
    parser = argparse.ArgumentParser()
    parser.add_argument('--src', help='Source of existing DICOM data')
    parser.add_argument('--dst', help='Dest. for new DICOM data')
    # parser.add_argument('--nifti', help='Dir for intermediate NIFTI files')
    # parser.add_argument('--keep', help='Keep intermediate files',
    #                     default=False, action='store_true')
    if len(sys.argv) == 1:
        parser.print_help(sys.stderr)
        sys.exit(1)
    return parser.parse_args()


if __name__ == '__main__':
    args = parse_args()
    main(args.src, args.dst)
