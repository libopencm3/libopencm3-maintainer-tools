#!/usr/bin/env sh

function runa() {
	cd $REPO$ARCH$BOARD$1
	
	make
	BMP_PORT=COM3 make flash
	cat README
	read -p "Press [Enter] to move to next example ..."
	cd $CWD
}

BMP_PORT=COM3
CWD=$(pwd)
REPO="../../libopencm3-examples/"
ARCH="examples/stm32/f4/"
BOARD="stm32f4-discovery/"

examples=$(find $REPO$ARCH$BOARD -type d -printf '%P\n')

for line in $examples;
do
	runa ${line}
done
