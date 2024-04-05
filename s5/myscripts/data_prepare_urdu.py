import os
FFMPEG_BIN = "ffmpeg"
whole_dataset_csv = "whole_data_urdu_16k.csv"
BASE_DIR = "SEHARDATA"

# Urdu data pre-process
data_list = ["86sentences", "100sentences", "Common Voice Urdu",
            "Third Dataset"]


def convert_audio(src_file, dst_file, samplerate=16000):
    try:
        convert_command = "ffmpeg -i {} -acodec pcm_s16le -ac 1 -ar {} {} -y -loglevel panic".format(
            src_file, samplerate, dst_file
        )
        os.system(convert_command)
        return True
    except Exception as error:
        print(repr(error))
        return False


def read_text_from_file(text_file):
    if not os.path.isfile(text_file):
        return ""
    
    try:
        with open(text_file, 'r', encoding="utf-8") as fp:
            text_data = ' '.join([x.strip() for x in fp.readlines()])
            return text_data
    except Exception as error:
        print(error)
        return ""


def get_file_size_in_bytes(file_path):
    """ Get size of file at given path in bytes"""
    try:
        size = os.path.getsize(file_path)
        return size
    except:
        return 0


# write header(columns) to csv file
if not os.path.isfile(whole_dataset_csv):
    with open(whole_dataset_csv, "w", encoding="utf-8") as csvfp:
        csvfp.write("wav_filename,wav_filesize,transcript\n")

# 1. 86sentences/
# """
cur_data_dir = "86sentences"
cur_text_dir = "TRANSCRIPT 86 sentences"
cur_audio_dir = [x for x in os.listdir(cur_data_dir) if x != cur_text_dir and not x.endswith("_16k")]

print("sub audio-data in {}: {}".format(cur_data_dir, cur_audio_dir))
with open(whole_dataset_csv, "a", encoding="utf-8") as csvfp:
    for sub_audio_dir in cur_audio_dir:
        cur_dir_path = os.path.join(cur_data_dir, sub_audio_dir)
        if os.path.isdir("{}_16k".format(cur_dir_path)):
            continue
        audio_files = os.listdir(cur_dir_path)

        new_audio_dir = "{}_16k".format(cur_dir_path)
        os.makedirs(new_audio_dir, exist_ok=True)

        # check audio extension and write to csv file with transcript
        for audio_file in audio_files:
            if not audio_file.lower().endswith(".wav"):
                continue
            text_file = os.path.join(cur_data_dir, cur_text_dir, audio_file[:-4]+".txt")
            if not os.path.isfile(text_file):
                print("Not found text file: {}".format(text_file))
                continue

            text_data = read_text_from_file(text_file)
            if text_data == "":
                continue

            # convert audio to 16kHz samplerate
            convert_audio_path = os.path.join(new_audio_dir, audio_file)
            if not convert_audio(os.path.join(cur_dir_path, audio_file), convert_audio_path, 16000):
                print("Error in converting audio {}".format(audio_file))
                continue
            
            file_size = get_file_size_in_bytes(convert_audio_path)
            if file_size == 0:
                continue
            csvfp.write("{},{},{}\n".format(convert_audio_path, file_size, text_data))
            print("{},{},{}".format(convert_audio_path, file_size, text_data))
# """

# 2. 100sentences
cur_data_dir = "100sentences"
cur_text_dir = "TRANSCRIPT 100 SENTENCES"
cur_audio_dir = [x for x in os.listdir(cur_data_dir) if x != cur_text_dir and not x.endswith("_16k")]

print("sub audio-data in {}: {}".format(cur_data_dir, cur_audio_dir))
with open(whole_dataset_csv, "a", encoding="utf-8") as csvfp:
    for sub_audio_dir in cur_audio_dir:
        cur_dir_path = os.path.join(cur_data_dir, sub_audio_dir)
        if os.path.isdir("{}_16k".format(cur_dir_path)):
            continue
        audio_files = os.listdir(cur_dir_path)

        new_audio_dir = "{}_16k".format(cur_dir_path)
        os.makedirs(new_audio_dir, exist_ok=True)

        # check audio extension and write to csv file with transcript
        for audio_file in audio_files:
            ext = audio_file.lower()[-3:]
            if not ext in ["wav", "wma", "mp3"]:
                continue
            text_file = os.path.join(cur_data_dir, cur_text_dir, audio_file[:-4]+".txt")
            if not os.path.isfile(text_file):
                print("Not found text file: {}".format(text_file))
                continue

            text_data = read_text_from_file(text_file)
            if text_data == "":
                continue

            # convert audio to 16kHz samplerate
            convert_audio_path = os.path.join(new_audio_dir, audio_file[:-4]+".wav")
            if not convert_audio(os.path.join(cur_dir_path, audio_file), convert_audio_path, 16000):
                print("Error in converting audio {}".format(audio_file))
                continue
            
            file_size = get_file_size_in_bytes(convert_audio_path)
            if file_size == 0:
                continue
            csvfp.write("{},{},{}\n".format(convert_audio_path, file_size, text_data))
            print("{},{},{}".format(convert_audio_path, file_size, text_data))

# 3. Third Dataset
cur_data_dir = "ThirdDataset"
cur_text_dir = "Transcript"
cur_audio_dir = [x for x in os.listdir(cur_data_dir) if x != cur_text_dir and not x.endswith("_16k")]

print("sub audio-data in {}: {}".format(cur_data_dir, cur_audio_dir))
with open(whole_dataset_csv, "a", encoding="utf-8") as csvfp:
    for sub_audio_dir in cur_audio_dir:
        cur_dir_path = os.path.join(cur_data_dir, sub_audio_dir)
        if os.path.isdir("{}_16k".format(cur_dir_path)):
            continue
        audio_files = os.listdir(cur_dir_path)

        new_audio_dir = "{}_16k".format(cur_dir_path)
        os.makedirs(new_audio_dir, exist_ok=True)

        # check audio extension and write to csv file with transcript
        for audio_file in audio_files:
            ext = audio_file.lower()[-3:]
            if not ext in ["wav", "wma", "mp3"]:
                continue
            text_file = os.path.join(cur_data_dir, cur_text_dir, audio_file[:-4]+".txt")
            if not os.path.isfile(text_file):
                print("Not found text file: {}".format(text_file))
                continue

            text_data = read_text_from_file(text_file)
            if text_data == "":
                continue

            # convert audio to 16kHz samplerate
            convert_audio_path = os.path.join(new_audio_dir, audio_file[:-4]+".wav")
            if not convert_audio(os.path.join(cur_dir_path, audio_file), convert_audio_path, 16000):
                print("Error in converting audio {}".format(audio_file))
                continue
            
            file_size = get_file_size_in_bytes(convert_audio_path)
            if file_size == 0:
                continue
            csvfp.write("{},{},{}\n".format(convert_audio_path, file_size, text_data))
            print("{},{},{}".format(convert_audio_path, file_size, text_data))