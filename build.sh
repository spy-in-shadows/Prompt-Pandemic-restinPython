#!/usr/bin/env bash
# exit on error
set -o errexit

apt-get update && apt-get install -y libxml2-dev libxslt1-dev

pip install -r requirements.txt
