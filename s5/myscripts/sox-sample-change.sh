cd ~/Documents/moreDrums/

ls

mkdir converted

for file in *.wav; do sox $file -c 1 -r 48000 -b 16 converted/$(basename $file) -V; done
