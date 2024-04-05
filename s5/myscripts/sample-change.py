from pydub import AudioSegment as am
sound = am.from_file(filepath, format='wav', frame_rate=22050)
sound = sound.set_frame_rate(16000)
sound.export(filepath, format='wav')
