#!/bin/bash
# NÃO RODAS AINDA PELO AMOR DE QUALQUER COISA
p=('01' '02' '03' '04' '05' '06' '07' '08' '09' '10' '11' '12' '13' '14' '15' '16' '17' '18' )
# sist=(007 008 008 008 008 007 008 008 007 007 008 011 008 008 008 008 011 010)


for ((a=0; a < 18; a++))
do
	# rm -rf slices_Pat${p[a]}/sistole/
	# rm -rf slices_Pat${p[a]}/diastole/
	slices=$( head -n 6 ./HeartDatabase/Pat${p[a]}/expert1/systole_endocarde_scaled.pgm | cut -d ' ' -f 3 |  tail -n 2 | head -n 1);
	echo ${a}	
	if [ ${a} -eq 4 ];
  	then
  		slices=29
	fi
	if [ ${a} -eq 8 ];
  	then
  		slices=34
	fi
	echo ${slices}
	
	for((b = 0; b < slices; b++))
	do
		./extractplane ./HeartDatabase/Pat${p[a]}/expert1/systole_endocarde_scaled.pgm ${b} xy slices/slices_Pat${p[a]}/experts/Pat${p[a]}_sistole_expert1${b}_endo.pgm
		./extractplane ./HeartDatabase/Pat${p[a]}/expert1/systole_epicarde_scaled.pgm ${b} xy slices/slices_Pat${p[a]}/experts/Pat${p[a]}_sistole_expert1${b}_epi.pgm
		./extractplane ./HeartDatabase/Pat${p[a]}/expert2/systole_endocarde_scaled.pgm ${b} xy slices/slices_Pat${p[a]}/experts/Pat${p[a]}_sistole_expert2${b}_endo.pgm
		./extractplane ./HeartDatabase/Pat${p[a]}/expert2/systole_epicarde_scaled.pgm ${b} xy slices/slices_Pat${p[a]}/experts/Pat${p[a]}_sistole_expert2${b}_epi.pgm

		./extractplane ./HeartDatabase/Pat${p[a]}/expert1/diastole_endocarde_scaled.pgm ${b} xy slices/slices_Pat${p[a]}/experts/Pat${p[a]}_diastole_expert1${b}_endo.pgm
		./extractplane ./HeartDatabase/Pat${p[a]}/expert1/diastole_epicarde_scaled.pgm ${b} xy slices/slices_Pat${p[a]}/experts/Pat${p[a]}_diastole_expert1${b}_epi.pgm
		./extractplane ./HeartDatabase/Pat${p[a]}/expert2/diastole_endocarde_scaled.pgm ${b} xy slices/slices_Pat${p[a]}/experts/Pat${p[a]}_diastole_expert2${b}_endo.pgm
		./extractplane ./HeartDatabase/Pat${p[a]}/expert2/diastole_epicarde_scaled.pgm ${b} xy slices/slices_Pat${p[a]}/experts/Pat${p[a]}_diastole_expert2${b}_epi.pgm



	done
done	
