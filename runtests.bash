#!/bin/bash


if [ $# -ne 1 ]; 
    then
    echo "usage: $ ./runtests.bash ./<ExecutableSolution> ";
    exit
fi

EXE=$1

if [ ! -d results/ ];
then 
    mkdir results
fi

if [ ! -d tmp/ ];
then
    mkdir tmp
fi

for f in Tests/*.in 
do
    rm -rf tmp/*

    strippedFolder="${f##*/}"
    strippedExtension="${strippedFolder%%.in}"
    fout="results/${strippedExtension}.out"
    T="$(date +%s%N)"
    $EXE < "$f" > "$fout"
    T="$(($(date +%s%N)-T))"
    M="$((T/1000000))"
    diff "${fout}" "Tests/${strippedExtension}.out" > "tmp/currdiff.tmp"
    if [ -s "tmp/currdiff.tmp" ]
    then
        echo "Test $strippedExtension failed"
    else
        printf "Test $strippedExtension passed  - %04d ms\n" "$((M))"
    fi
done

rm -rf tmp/*
rm -rf results/*
rmdir results
rmdir tmp
