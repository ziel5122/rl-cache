#!/bin/bash

cache_max=$1
data_mult=$2
type=$3

file_name=$type"-"$cache_max"-"$data_mult".csv"
echo $file_name

1>./grids/$file_name

for ((cache_size=1;cache_size<=$1;cache_size++))
{
	data_size=$((cache_size * data_mult))
	data_max=$((cache_max * data_mult))
	for ((;data_size<=data_max;data_size+=$data_mult))
	{
		python cache_sim.py -c $cache_size -d $data_size -n 1000 $type 1>>./grids/$file_name
	}
}
