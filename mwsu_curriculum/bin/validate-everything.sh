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

for dir in syllabi/*
do
  for f in $dir/*
  do
	xmllint --schema schema/course.xsd --noout $f
	if [ $? -ne 0 ]; then
	    	echo "*** $f failed to validate"
		exit
	fi
  done  
done  

for f in standards/*.xml
do
	xmllint --schema schema/standard.xsd --noout $f
	if [ $? -ne 0 ]; then
	    	echo "*** $f failed to validate"
		exit
	fi
done  

for f in rosters/*.xml
do
	xmllint --schema schema/roster.xsd --noout $f
	if [ $? -ne 0 ]; then
	    	echo "*** $f failed to validate"
		exit
	fi
done  

for f in schedules/*.xml
do
	xmllint --schema schema/schedule.xsd --noout $f
	if [ $? -ne 0 ]; then
	    	echo "*** $f failed to validate"
		exit
	fi
done  

for dir in programs/*
do
  for f in $dir/*
  do
	xmllint --schema schema/program.xsd --noout $f
	if [ $? -ne 0 ]; then
	    	echo "*** $f failed to validate"
		exit
	fi
  done  
done  

pytest-3 -v
