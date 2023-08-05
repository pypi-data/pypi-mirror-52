#!/usr/bin/env python3
# coding=utf-8

"""A utility to write build files to AWS S3.

Build files consist of txt.gz and csv.gz files, those that are
the result of de-duplicated graph processing and txt->csv pre-processing.

To use this utility you will need to ensure that your AWS credentials
are available via expected environment variables. Please refer to
the AWS boto3 documentation, which describes this: -

    https://boto3.amazonaws.com/v1/documentation/api/latest/guide/quickstart.html

Alan Christie
February 2019
"""

import argparse
import logging
import os
import sys

import boto3

# Configure basic logging
formatter = logging.Formatter('%(asctime)s %(levelname)s # %(message)s',
                              '%Y-%m-%dT%H:%M:%S')

out_hdlr = logging.StreamHandler()
out_hdlr.setFormatter(formatter)
out_hdlr.setLevel(logging.INFO)

logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)
logger.addHandler(out_hdlr)

# Expected environment variables (that define the bucket)
s3_bucket_env = 'AWS_S3_BUCKET'
s3_build_root = 'build'
s3_archive_bucket = os.environ.get(s3_bucket_env)
if not s3_archive_bucket:
    logger.error('You must define %s', s3_bucket_env)
    sys.exit(1)

parser = argparse.ArgumentParser('Graph Build File Putter')
parser.add_argument('source', metavar='DIR', type=str,
                    help='The local directory (where the raw data exists)')
parser.add_argument('path', metavar='PATH', type=str,
                    help='The path, relative to the "raw" directory'
                         ' in your S3 bucket. e.g. "activity/senp7/build-1"')

args = parser.parse_args()

# Check source directory
if not os.path.isdir(args.source):
    logger.error('The source directory does not exist (%s)', args.source)
    sys.exit(1)

# The S3 build path...
dst = s3_build_root + '/' + args.path + '/'
s3_client = boto3.client('s3')

# We must not write to an existing path (key).
# It is up to the user to make sure the destination does not exist,
# it's too easy to over-write files in S3.
target = s3_client.list_objects_v2(Bucket=s3_archive_bucket,
                                   Prefix=dst)
if 'KeyCount' in target and target['KeyCount']:
    logger.error('The build path already exists in S3.'
                 ' You cannot "put" to existing locations.')
    sys.exit(1)

# The list of files to load...
required_build_files = ['nodes.csv.gz',
                        'edges.csv.gz']
# Optional files.
# Molecules rejected at the filter stage,
# molecules excluded during fragmentation
# and other files from nextflow (report, timeline, trace)
optional_build_files = ['rejected-compounds.tab.gz',
                        'excluded.csv.gz',
                        'report.html',
                        'timeline.html',
                        'trace.txt']

# Check that all the files exist...
for build_file in required_build_files:
    src = os.path.join(args.source, build_file)
    if not os.path.isfile(src):
        logger.error('Missing "%s" build file.', src)
        sys.exit(1)

build_files = required_build_files + optional_build_files
for build_file in build_files:
    src = os.path.join(args.source, build_file)
    if os.path.isfile(src):
        dst = s3_build_root + '/' + args.path + '/' + build_file
        logger.info('Putting %s -> %s...', build_file, args.path)
        s3_client.upload_file(src, s3_archive_bucket, dst)
