#Run in the root of the parent directory with args as the name of the parent directory.,,example: python3 audioscanner.py myfolder,,where myfolder contains the subfolders like AhmadAli


    # get all audio files 
    # get folder with transcripts
#pip install audio-metadata    
# open root folder
# go to child folder
# go to child folder


from curses import meta
import os
import csv
from os import listdir
from os.path import isfile, join
import audio_metadata
import re
import sys

def atoi(text):
    return int(text) if text.isdigit() else text

def natural_keys(text):
    return [ atoi(c) for c in re.split(r'(\d+)', text) ]


x = "./" + sys.argv[1] + "/"
mypath = os.path.abspath(x)
onlydirs = [f for f in sorted(listdir(mypath),key=natural_keys)]

if '.DS_Store' in onlydirs:
    onlydirs.remove('.DS_Store')

header = ["filepath","filesize","audio_format","bit_depth","bitrate","channels","duration","sample_rate","transcript"]

with open('test_data.csv', 'w', encoding='UTF8') as f:
      writer = csv.writer(f)
      writer.writerow(header)

for dir in onlydirs:
    transcripts = []
    current_dir = x + dir + "/"
    curr_path = os.path.abspath(current_dir)
    audio_files = [f for f in sorted(listdir(curr_path),key=natural_keys) if isfile(join(curr_path, f))]
    transcript_dir = current_dir + "Transcript/"
    transcript_path = os.path.abspath(transcript_dir)
    transcript_files = [f for f in sorted(listdir(transcript_path),key=natural_keys) if isfile(join(transcript_path, f))]

    if '.DS_Store' in transcript_files:
        transcript_files.remove('.DS_Store')
    
    if '.DS_Store' in audio_files:
        audio_files.remove('.DS_Store')

    for file in transcript_files:
        with open( os.path.abspath(transcript_path + "/" + file ), 'r', encoding='UTF8') as f:
            contents = f.read()
            transcripts.append(contents)
    
    for index, item in enumerate(audio_files):
        metadata = audio_metadata.load(os.path.abspath(curr_path + "/" + item ))
        row = [metadata.filepath, metadata.filesize, metadata.streaminfo.audio_format, metadata.streaminfo.bit_depth, 
                metadata.streaminfo.bitrate, metadata.streaminfo.channels, metadata.streaminfo.duration, metadata.streaminfo.sample_rate, transcripts[index]]
        with open('test_data.csv','a') as f:
            writer = csv.writer(f)
            writer.writerow(row)
        print("1 Record Added")

    

print("All Done!")



