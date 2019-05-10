#!/bin/bash
#scripts/validate-everything.sh
mkdir -p output
for f in syllabi/*
do
	course=`basename "$f"`
	course="${course%.*}"
	echo "processing $course"
	xsltproc transformations/syllabus-to-html.xsl $f > output/$course.html
	if [ $? -eq 0 ]; then
 	   	echo "$f was processed"
	else
	    	echo "*** $f failed to process"
		exit
	fi
done  
