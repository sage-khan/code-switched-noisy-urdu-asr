#!/usr/bin/env python3

from vosk import Model, KaldiRecognizer, SetLogLevel
import os
import wave
import json

#fname =  input ( "Enter audio file name: " ) 
fname = sys.argv[1]
wav = ".wav"
txt = ".txt"
transcript = fname + txt
audiofilename = fname + wav

#wav = input( "enter audio filename with extension: " )
wf = wave.open(audiofilename, "rb")
model = Model("..")
rec = KaldiRecognizer(model, wf.getframerate())

results = []
# recognize speech using vosk model

while True:
    data = wf.readframes(4000)

    if len(data) == 0:
        break

    if rec.AcceptWaveform(data):
        part_result = json.loads(rec.Result())
        results.append(part_result)
        print(rec.Result())

    else:
        print(rec.PartialResult())
part_result = json.loads(rec.FinalResult())
results.append(part_result)

# forming a final string from the words
text = ''
for r in results:
    text += r['text'] + ' '

print(f"Vosk thinks you said:\n {text}")         
#print(rec.FinalResult())

# convert list of JSON dictionaries to list of 'Word' objects
list_of_Words = []
for sentence in results:
    if len(sentence) == 1:
        # sometimes there are bugs in recognition 
        # and it returns an empty dictionary
        # {'text': ''}
        continue
    for obj in sentence['result']:
        w = custom_Word.Word(obj)  # create custom Word object
        list_of_Words.append(w)  # and add it to list

wf.close()  # close audiofile

# output to the screen
for word in list_of_words:
    print(word.to_string())
