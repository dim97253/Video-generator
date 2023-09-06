from bark import SAMPLE_RATE, generate_audio, preload_models
from IPython.display import Audio
from scipy.io.wavfile import write as write_wav

def get_wav (name, prompt):
    filename = f"{name}.wav"
    preload_models()
    speech_array = generate_audio(prompt,history_prompt="v2/en_speaker_7")
    #speech_array = generate_audio(prompt)
    write_wav(filename, SAMPLE_RATE, speech_array)
    return filename