# CSMP Curriculum

## Python Library

Several python functions and classes are made available for manipulation of MWSU CSMP curriculum in other scripts and applications.

## Syllabus Content

Syllabi are codified to include all necessary catalog information, all necessary official syllabus content, and also alignment to curriculum standards. The schema folder contains official schema for validation of syllabus documents, the transformation folder contains XSLT scripts for conversion in to official syllabi, and the scripts folder contains shell scripts to automate these processes. 

## Alignment of Curriculum to External Standards

The standards folder contains initial efforts towards development of XML codification of external (or internal) standards, but is still a work in progress. 

## Dependencies (ubuntu packages listed)
* python3
* pytest-benchmark  (python3-pytest-benchmark in Ubuntu 20.04)
* libxml2-utils
* xmllint (this is part of libxml2-utils in the Ubuntu 20.04 repositories, and does not need to be installed separately)

Once all these are installed, run:

```pip3 install . ```

to install the package
