#!/bin/bash

projHome=$(cd ../; pwd)

if ! grep PYTHONPATH ~/.bash_profile; then
    echo "export PYTHONPATH=$projHome" >> ~/.bash_profile
fi
