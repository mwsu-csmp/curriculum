#!/bin/bash
for f in schema/*
do
	xmllint --noout $f
	if [ $? -eq 0 ]; then
 	   	echo "$f is valid"
	else
	    	echo "*** $f failed to validate"
		exit
	fi
done  

for f in transformations/*
do
	xmllint --noout $f
	if [ $? -eq 0 ]; then
 	   	echo "$f is valid"
	else
	    	echo "*** $f failed to validate"
		exit
	fi
done  

for f in syllabi/*
do
	xmllint --schema schema/* --noout $f
	if [ $? -eq 0 ]; then
 	   	echo "$f is valid"
	else
	    	echo "*** $f failed to validate"
		exit
	fi
done  

#xmllint --schema schema/* syllabi/CSC184.xml --noout
