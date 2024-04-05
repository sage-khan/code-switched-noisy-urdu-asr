import os
from pydub import AudioSegment


path = input ("please enter path:")

#Change working directory
os.chdir(path)

audio_files = os.listdir()

# You dont need the number of files in the folder, just iterate over them directly using:
for file in audio_files:
    #spliting the file into the name and the extension
    name, ext = os.path.splitext(file)
    if ext == ".mp3":
       mp3_sound = AudioSegment.from_mp3(file)
       #rename them using the old name + ".wav"
       mp3_sound.export("{0}.wav".format(name), format="wav")

#from os import path
#from pydub import AudioSegment

## files
#src = input("input source name of mp3 file:")
#dst = input("enter destination wav name:")

## convert wav to mp3
#sound = AudioSegment.from_mp3(src)
#sound.export(dst, format="wav")
