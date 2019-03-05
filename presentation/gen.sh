#!/bin/bash

# ---- Latex generator using pdflatex -----
# - Written by Magnus Sörensen -

# Base file is the starting point for the documens with out tex ending i.e main.tex is just main.
# pdfshow is the pdf viewer.
baseFile=main
pdfshow=zathura
output_directory=/tmp/pdflatex/


check_process() {
  echo "$ts: checking $1"
  [ "$1" = "" ]  && return 0
  [ `pgrep -n $1` ] && return 1 || return 0
}

#if [ $(uname) == "Linux" ]; then echo yes;fi

if [ ! -d $output_directory ];
then
    mkdir $output_directory
fi
#ps aux | grep $pdfshow > /dev/null
check_process "$pdfshow"
if [ ! $? -eq 0 ];
then
    echo "$pdfshow is running. Kill ing it."
    pkill $pdfshow
fi
cp $baseFile.tex $baseFile.bac
if [ -f $baseFile.tex ];
then
    pdflatex -interaction=nonstopmode -output-directory $output_directory $baseFile.tex > /dev/null
    cp "$output_directory$baseFile.pdf" .
fi
if [ -f $baseFile.pdf ];
then
    $pdfshow $baseFile.pdf &
fi
cat $output_directory$baseFile.log
#rm *.out *.bac *.bac *.aux > /dev/null
