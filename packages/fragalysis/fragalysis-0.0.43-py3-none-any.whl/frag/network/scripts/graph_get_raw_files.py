#!/usr/bin/env python3
# coding=utf-8

"""A utility to get raw (vendor) data files from AWS S3.
This utility collects data, normally prior to standardising.

This module assumes that the source of the data
resides in an S3 bucket with a directory structure that complies with the
**Fragalysis S3 Data Archive** definition.

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
s3_data_root = 'raw'
s3_archive_bucket = os.environ.get(s3_bucket_env)
if not s3_archive_bucket:
    logger.error('You must define %s', s3_bucket_env)
    sys.exit(1)

parser = argparse.ArgumentParser('Graph Raw File Getter')
parser.add_argument('path', metavar='PATH', type=str,
                    help='The path, relative to the "raw" directory'
                         ' in your S3 bucket. e.g. "activity/senp7/v1"')
parser.add_argument('destination', metavar='DIR', type=str,
                    help='The local destination directory for the data,'
                         ' which must not exist and will be created')
parser.add_argument("--force", dest="force", action="store_true")

args = parser.parse_args()

# Destination?
if not args.force and os.path.isdir(args.destination):
    logger.error('Destination exists')
    sys.exit(1)

src = s3_data_root + '/' + args.path + '/'
logger.info('Getting files from "%s"...', args.path)

# Get the contents of the selected directory...
s3_client = boto3.client('s3')
resp = s3_client.list_objects_v2(Bucket=s3_archive_bucket,
                                 Prefix=src)

# And download everything that looks like a file...
if resp and 'KeyCount' in resp:

    if resp['KeyCount']:

        if not os.path.isdir(args.destination):
            os.mkdir(args.destination)

        num_files = 0
        for content in resp['Contents']:
            if not content['Key'].endswith('/'):
                filename = content['Key'].split('/')[-1]
                logger.info('%s > %s', filename, args.destination)
                s3_client.download_file(s3_archive_bucket,
                                        content['Key'],
                                        os.path.join(args.destination, filename))
                num_files += 1
        logger.info('Done (%d)', num_files)

    else:

        # KeyCount was zero
        logger.warning('No files found')
        sys.exit(1)

else:

    logger.error('Unexpected response (expected KeyCount)')
    sys.exit(1)
