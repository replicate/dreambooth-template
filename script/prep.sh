#!/bin/sh

# Prep cog with NSFW safety weights before using cog to build container.

# see DOWNLOAD variables section for steps to build a new tarball

# NOTE: this script provides a cachable way of building the container with weights.
# As the builder might be run on ubuntu, or alpine, or any other linux distro, this 
# script should be written to minimize dependencies on the host system.

# Current dependencies:
# - curl
# - md5sum
# - tar
# - CACHE_DIR (passed as first argument)

set -o xtrace  # enable command tracing
set -o errexit # exit on error

# This script is meant to live in the script directory of a cog repo
# To test, test that cog.yaml exists in the parent directory of this script

SCRIPT_DIR=$(dirname "$0")
PARENT_DIR=$(dirname "$SCRIPT_DIR")

if ! test -f "$PARENT_DIR/cog.yaml"; then
    echo "cog.yaml not found in parent of script directory: $PARENT_DIR"
    exit 1
fi

# DOWNLOAD variables

# The tarball contains the safety weights, which are downloaded to `diffusers-cache`
# directory via the `script/download-weights` script.

# To create a new tarball, run that script, then create and update a new tarball
# with the following command:

#    script/download-weights
#    tar -cf safety.tar diffusers-cache/
#    md5sum safety.tar
#    mv safety.tar safety-<md5sum>.tar
#    gsutil cp safety-<md5sum>.tar gs://replicant-misc

# then update the DOWNLOAD variables below with the new md5sum and url

DOWNLOAD_URL="https://storage.googleapis.com/replicant-misc/safety-16af6aac4bcc97d6f5e38ec53eec7fac.tar"
DOWNLOAD_MD5="16af6aac4bcc97d6f5e38ec53eec7fac"
CACHE_DIR=$1
CACHE_FN=safety-16af6aac4bcc97d6f5e38ec53eec7fac.tar
CACHED="$CACHE_DIR/$CACHE_FN"

if ! test -d "$CACHE_DIR"; then
    echo "Destination directory does not exist: $CACHE_DIR"
    echo "Usage: $0 CACHE_DIR"
    exit 1
fi

# download with continue / this should be a no-op if the file already exists
curl "$DOWNLOAD_URL" -C - -o "$CACHED"


set +o errexit  # disable exit on error, as we will want to delete 
                # the file if the md5sum doesn't match

# ensure the md5sum matches, store exit code
echo "$DOWNLOAD_MD5  $CACHED" | md5sum -c -
MD5=$?

set -o errexit  # re-enable exit on error

if [ $MD5 -ne 0 ]; then
    echo "MD5 sum mismatch"
    rm "$CACHED"
    exit 1
fi

# extract the tarball into the parent directory of the script
# which is the root of the repo
tar -xf "$CACHED" -C "$PARENT_DIR"