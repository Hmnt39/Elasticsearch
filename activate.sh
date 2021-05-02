#!/bin/bash

ABS_ENV_DIR=$(cd ${1:-~/env/es/} && pwd -P)
source $ABS_ENV_DIR/bin/activate
echo "Using virtualenv from $ABS_ENV_DIR"