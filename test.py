# Load FastPitch
from nemo.collections.tts.models import FastPitchModel
import soundfile as sf
from nemo.collections.tts.models import HifiGanModel

spec_generator = FastPitchModel.from_pretrained("nvidia/tts_en_fastpitch")

# Load vocoder
model = HifiGanModel.from_pretrained(model_name="nvidia/tts_hifigan")

parsed = spec_generator.parse("You can type your sentence here to get nemo to produce speech.")
spectrogram = spec_generator.generate_spectrogram(tokens=parsed)
audio = model.convert_spectrogram_to_audio(spec=spectrogram)

# Save the audio to disk in a file called speech.wav
sf.write("speech.wav", audio.to('cpu').detach().numpy()[0], 22050)
