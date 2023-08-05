

S3Backup
========

CLI for backing up to S3

Usage
-----

- Install AWS CLI and add your credentials
- Run "pip install -e ." in the programs parent directory
- Run script from a directory to backup OR point to directory.
- First variable is the target object and second variable is the destination bucket.
- If the json config default bucket is set then you can skip the second variable to use the default.
- To use a wildcard you must place it in quotations '*'.
- To use recursive wildcards you must use '**' see glob module.


Examples
--------

Example to upload current working directory::

  s3simplebackup . testbucket

Example to upload a home Directory::

  s3simplebackup ~ testbucket

Example to upload a folder::

  s3simplebackup folder testbucket

Example to upload all python scripts in Directory with default bucket::

  s3simplebackup '*.py'

Example to upload all python scripts recursively in directory with default bucket::

  s3simplebackup '**.py'
