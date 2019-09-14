#!/bin/bash

for i in {1..3}
do
	python3 tsc_main.py $i
done
wall "Run complete"
