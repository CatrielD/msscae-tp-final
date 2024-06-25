#!/usr/bin/env bash

for f in *.pkl
do
    tar -zcf ${f%.pkl}.tar.gz $f
done
