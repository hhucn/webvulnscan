#!/bin/sh

mkdir -p /home/webvulnscan/Desktop/
cd /home/webvulnscan/Desktop/
git clone https://github.com/hhucn/webvulnscan.git
cd webvulnscan
git checkout installscripts
cd targets
./install.sh