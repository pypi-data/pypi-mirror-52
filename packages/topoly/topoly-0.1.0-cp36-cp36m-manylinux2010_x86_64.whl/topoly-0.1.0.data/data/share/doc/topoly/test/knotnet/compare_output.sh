#!/usr/bin/env bash

SRC1=`cat $1 | grep "#"`
SRC2=`cat $2 | grep "#"`

if [ "$SRC1" != "$SRC2" ]; then
  echo "Matrix File headers don't match!"
  exit 1
fi

F1_LEN=`cat $1 | wc -l`
F2_LEN=`cat $2 | wc -l`
FLEN_DIF=$(($F1_LEN-$F2_LEN))
#echo ${FLEN_DIF#-}

if (( ${FLEN_DIF#-} > 80)); then
  echo "File length is significantly different!"
  exit 2
fi
