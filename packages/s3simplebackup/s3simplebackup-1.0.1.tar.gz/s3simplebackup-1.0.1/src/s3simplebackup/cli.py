import boto3
import os
import json
from argparse import ArgumentParser
from glob import glob

try:
    with open('config.json') as f:
        config = json.loads(f.read())
        default_bucket = config['default_bucket']
except:
        default_bucket = None

def create_parser():
    parser = ArgumentParser()
    parser.add_argument('target', help="File or Directory to upload")
    if default_bucket:
        parser.add_argument('bucket', help="Bucket to upload files to", default=f"{default_bucket}", nargs="?")
    elif not default_bucket:
        parser.add_argument('bucket', help="Bucket to upload files to")
    return parser

def main():
    s3 = boto3.resource('s3')
    args = create_parser().parse_args()
    if "~" in args.target:
        args.target = (args.target).replace("~", f"{os.getenv('HOME')}"+'/')
        print(args.target)
    if "*" in args.target:
        for file in glob(f'{args.target}', recursive=True):
            if os.path.isfile(file):
                s3.meta.client.upload_file(file, args.bucket, file)
    elif not os.path.exists(args.target):
        raise ValueError(f"{args.target} does not exist")
    elif os.path.isfile(args.target):
        s3.meta.client.upload_file(args.target, args.bucket, args.target)
    elif os.path.isdir(args.target):
        replace = os.path.abspath(args.target) + "/"
        for folder, subfolders, files in os.walk(args.target):
            for file in files:
                filePath = os.path.join(os.path.abspath(folder), file)
                filePath = filePath.replace(f"{replace}",'')
                s3.meta.client.upload_file(filePath, args.bucket, filePath)
    else:
        raise ValueError(f"{args.target} unknown type")
    print(f"{args.target} uploaded to {args.bucket}")
