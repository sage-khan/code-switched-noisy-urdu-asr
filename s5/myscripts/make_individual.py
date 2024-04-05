import os
import pandas as pd
import librosa


train_dir = "train"
os.makedirs(train_dir, exist_ok=True)

test_dir = "test"
os.makedirs(test_dir, exist_ok=True)
data_dir = "/home/metanet/ProgramFiles/kaldi/kaldi/egs/ASR-for-urdu/s5/wav/"


def get_audio_length(full_path_string):
    y, sr = librosa.load(full_path_string)  # librosa.ex(audio_filepath[:-4]))
    end_time = librosa.get_duration(y=y, sr=sr)
    return end_time


def get_utt_id(full_path_string, number):
    _, folder_name, _ = full_path_string.split("/")
    utt_id = folder_name + f"_{number}"
    return utt_id


def get_rec_id(full_path_string):
    _, folder_name, filename = full_path_string.split("/")
    rec_id = folder_name.split("_")[0] + "_" + filename[:-4] + "_wav"

    return rec_id


def get_segments(full_path_string):
    _, folder_name, filename = full_path_string.split("/")
    rec_id = folder_name.split("_")[0] + "_" + filename
    return rec_id


def make_utt2spk(dataframe):
    utt2spk = [f"{utt} {utt}" for utt in dataframe.utt_id]
    sample_num = len(utt2spk)
    train_num = int(sample_num * 0.9)
    train_data, test_data = split_data(utt2spk)
    
    test_utt2spk = os.path.join(test_dir, "utt2spk")
    with open(test_utt2spk, "w") as u2s:
        u2s.write("\n".join(test_data))
    train_utt2spk = os.path.join(train_dir, "utt2spk")
    with open(train_utt2spk, "w") as u2s:
        u2s.write("\n".join(train_data))


def make_wavscp(dataframe):
    utt_scp = [f"{rec} {data_dir}{file_path}" for rec, file_path in zip(dataframe.rec_id, dataframe.wav_filename)]
    sample_num = len(utt_scp)
    train_num = int(sample_num * 0.9)
    train_data, test_data = split_data(utt_scp)

    test_utt_scp = os.path.join(test_dir, "wav.scp")
    with open(test_utt_scp, "w") as scp:
        scp.write("\n".join(test_data))
    
    train_utt_scp = os.path.join(train_dir, "wav.scp")
    with open(train_utt_scp, "w") as scp:
        scp.write("\n".join(train_data))


def make_segments(df):
    segments = [f"{utt} {rec_id} 0 {end}" for utt, rec_id, end in zip(df.utt_id, df.rec_id, df.end)]
    sample_num = len(segments)
    train_num = int(sample_num * 0.9)
    train_data, test_data = split_data(segments)
    
    test_segments = os.path.join(test_dir, "segments")
    with open(test_segments, "w") as seg:
        seg.write("\n".join(test_data))

    train_segments = os.path.join(train_dir, "segments")
    with open(train_segments, "w") as seg:
        seg.write("\n".join(train_data))


def make_text(dataframe):
    utt_text = [f"{utt} {text}" for utt, text in zip(dataframe.utt_id, dataframe.transcript)]
    sample_num = len(utt_text)
    train_num = int(sample_num * 0.9)
    train_data, test_data = split_data(utt_text)

    test_text = os.path.join(test_dir, "text")
    with open(test_text, "w") as tf:
        tf.write("\n".join(test_data))
    train_text = os.path.join(train_dir, "text")
    with open(train_text, "w") as tf:
        tf.write("\n".join(train_data))


def split_data(data):
    train = []
    test = []
    for i in range(len(data)):
        if i % 10 == 0:
            test.append(data[i])
        else:
            train.append(data[i])
    return train, test

def main(full_source):

    if not os.path.isfile(full_source):
        print("No such file exist: {}".format(full_source))
        return
    # open tsv file
    print("Reading {} ...".format(full_source))
    dataframe = pd.read_csv(full_source)
    header = dataframe.columns # ["wav_filename", "transcript"]
    print(header)

    dataframe_copied = dataframe.copy()
    dataframe_copied["_id_"] = list(range(len(dataframe_copied)))
    dataframe_copied["utt_id"] = dataframe_copied.apply(lambda x: get_utt_id(x['wav_filename'], x['_id_']), axis=1)
    # dataframe_copied["spk_id"] = dataframe_copied["wav_filename"].apply(get_utt_id)


    dataframe_copied["rec_id"] = dataframe_copied["wav_filename"].apply(get_rec_id)
    # dataframe_copied["start"] = dataframe_copied["wav_filename"].apply(get_utt_id)
    dataframe_copied["end"] = dataframe_copied["wav_filename"].apply(get_audio_length)

    make_text(dataframe_copied)
    make_utt2spk(dataframe_copied)
    make_wavscp(dataframe_copied)
    make_segments(dataframe_copied)
    pass


if __name__ == '__main__':
    source_full_data = 'whole_data_urdu_16k.csv'
    main(source_full_data)
