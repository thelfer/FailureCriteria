#!/bin/bash
cd tests/mesh/
rm -f *trace
cd ../../

cd tests/castem/
rm -f *trace
rm -rf castem/ src/ include/
cd ../../

cd src/
rm -rf src/ include/ __pycache__/
cd ..
