#!/bin/bash
for f in schema/*
do
	xmllint --noout $f
	if [ $? -eq 0 ]; then
 	   	echo "$f validates"
	else
	    	echo "*** $f failed to validate"
		exit
	fi
done  

for f in transformations/*
do
	xmllint --noout $f
	if [ $? -eq 0 ]; then
 	   	echo "$f validates"
	else
	    	echo "*** $f failed to validate"
		exit
	fi
done  

for f in syllabi/*
do
	xmllint --schema schema/course.xsd --noout $f
	if [ $? -ne 0 ]; then
	    	echo "*** $f failed to validate"
		exit
	fi
done  

for f in standards/*.xml
do
	xmllint --schema schema/standard.xsd --noout $f
	if [ $? -ne 0 ]; then
	    	echo "*** $f failed to validate"
		exit
	fi
done  

#xmllint --schema schema/* syllabi/CSC184.xml --noout
