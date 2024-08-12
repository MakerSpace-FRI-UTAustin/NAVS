from pvrecorder import PvRecorder
import wave, struct
from pydub import AudioSegment

#Beginning Code to figure out  what mics 
for index, device in enumerate(PvRecorder.get_available_devices()):
    print(f"[{index}] {device}")

def audio():
    recorder = PvRecorder(device_index=0, frame_length=512) #(32 milliseconds of 16 kHz audio)
    audio = []
    path = 'audio_recording.wav'

    try:
        recorder.start()

        while True:
            frame = recorder.read()
            audio.extend(frame)
    except KeyboardInterrupt:
        recorder.stop()
        with wave.open(path, 'w') as f:
            f.setparams((1, 2, 16000, 512, "NONE", "NONE"))
            f.writeframes(struct.pack("h" * len(audio), *audio))
    finally:
        recorder.delete()
        return "audio_recording.wav"