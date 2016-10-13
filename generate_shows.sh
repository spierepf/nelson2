#!/bin/bash

rm shows/*
python generate_shows.py
for i in `grep -r "\- show" config modes | cut -f7 -d' ' | sort -u` ; do cat shows/$i.yaml > /dev/null ; done
