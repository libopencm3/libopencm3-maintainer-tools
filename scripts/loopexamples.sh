#!/usr/bin/env sh

function boldtext() {
	echo -e "\e[1m$1\e[0m"
}

function runa() {
	# go to the directory with example
	cd $REPO$ARCH"/"$BOARD$1
	
	#clear screen
	echo -e "\e[2J"
	
	#Make the example
	boldtext "\nBuilding example $ARCH"/"$BOARD$1 ...\n"
	make
	
	#Flash the example into board
	boldtext "\nFlashing example $ARCH"/"$BOARD$1 ...\n"
	BMP_PORT=COM3 make flash
	
	# display the README of the example
	boldtext "\nExample's README:\n"
	echo -e "\e[1;32m"
	cat README
	echo -e "\e[0m"
	
	#restore working firectory
	cd $CWD
	
	boldtext "Is the example behaving correctly? [y(es)/n(o)/s(kip)]"
	
	while true; do
		read yn
		case $yn in
		[Yy]*)
			./wikiedit.py -f $WIKIFILE -t $REPO -s $ARCH pass $BOARD$1
			break
			;;
		[Nn]*)
			boldtext "Write a short description of the bug:"
			read descr
			./wikiedit.py -f $WIKIFILE -t $REPO -s $ARCH -m "$descr" fail $BOARD$1
			break
			;;
		[Ss]*)
			break
			;;
		*)
			echo "Please answer Yes, No or Skip!"
			;;
		esac
	done
}

BMP_PORT=COM3
CWD=$(pwd)
REPO="../../libopencm3-examples/"
ARCH="examples/stm32/f4"
BOARD="stm32f4-discovery/"
WIKIFILE="f4"

examples=$(find $REPO$ARCH"/"$BOARD -type d -printf '%P\n')

./wikiedit.py -f $WIKIFILE -t $REPO -s $ARCH init-tree
read

for line in $examples;
do
	runa ${line}
	
	boldtext "Press [Enter] to move to the next example ..."
	read
done

./wikiedit.py -f $WIKIFILE -t $REPO -s $ARCH update-tree
