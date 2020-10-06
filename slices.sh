#!/bin/bash

p=('01' '02' '03' '04' '05' '06' '07' '08' '09' '10' '11' '12' '13' '14' '15' '16' '17' '18' )
sist=(007 008 008 008 008 007 008 008 007 007 008 011 008 008 008 008 011 010)


for ((a=0; a < 18; a++))
do
	rm -rf slices_Pat${p[a]}/sistole/
	rm -rf slices_Pat${p[a]}/diastole/
	slices=$( head -n 2 ./slices/Pat${p[a]}/img/out001.pgm | cut -d ' ' -f 3 | tail -n 1);	
	mkdir slices_Pat${p[a]}
	mkdir slices_Pat${p[a]}/sistole
	mkdir slices_Pat${p[a]}/diastole
	
	for((b = 0; b < slices; b++))
	do
		./extractplane ./Pat${p[a]}/img/out${sist[a]}.pgm ${b} xy slices_Pat${p[a]}/sistole/Pat${p[a]}_sistole_slice${b}.pgm
		./extractplane ./Pat${p[a]}/img/out001.pgm ${b} xy slices_Pat${p[a]}/diastole/Pat${p[a]}_diastole_slice${b}.pgm

	done
done	
