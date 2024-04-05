#!/bin/bash

for i in wav/*.wav; do
    if sox -r 8000 -e unsigned -b 16 -c 1 "$i" "$i.resampled"; then
        # This way we will only replace the original file with the 
        # resampled version if sox returns a zero (no error) error code.
        mv "$i.resampled" "$i"
    else
        soxerrno = $?
        echo "Sox reported error number $soxerrno while processing file $i"
    fi
done

