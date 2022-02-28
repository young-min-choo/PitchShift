import librosa
import soundfile as sf

song = 'Vaundy odoriko INSTRUMENTAL.mp3'
rate = 44100
y, sr = librosa.load(song)
y_shifted = librosa.effects.pitch_shift(y, sr=rate, n_steps=+1)
sf.write('Vaundy odoriko INSTRUMENTAL + 1.flac', y_shifted, samplerate=sr,format='FLAC', subtype='PCM_24')
