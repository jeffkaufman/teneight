import wave
import struct
import math
import random

R = 44100
V = 32767/2
DURATION = 16

def write(fname, tempo, note_beats, up_beats):
  outf = wave.open(fname, 'w')
  outf.setnchannels(1) # mono
  outf.setsampwidth(2)
  outf.setframerate(R)

  values = [0]*(int(R * DURATION))

  def emit(start, offset, value):
    pos = start + offset
    if pos >= len(values):
      return
    values[pos] += value

  # all inputs are in samples
  def writeSine(start, length, volume, wavelen):
    # always write a multiple of wavelen/2 to end at a zero crossig
    half_wave = int(wavelen / 2)
    half_wavelengths = int(length / half_wave)
    for i in range(half_wavelengths * half_wave):
      emit(start, i, math.sin(2.0 * i / wavelen * math.pi) * volume)

  def writeNoise(start, length, volume):
    for i in range(length):
      emit(start, i, random.randint(-volume, volume))    

  def writeDownbeats():
    for beat in range(DURATION*2):
      start = tempo*beat
      writeSine(start, R/8, V/2, 1600) 
      writeSine(start, R/8, V/4, 800) 
      writeSine(start, R/8, V/4, 600) 
      writeSine(start, R/8, V/4, 400)
      writeSine(start, R/12, V/32, 200) 
      writeSine(start, R/16, V/32, 100)

  def writeUpbeats(interval, beat_number):
    for beat in range(DURATION*2):
      start = tempo*beat  + tempo*beat_number/interval
      writeSine(start, R/8, V/2, 800) 
      writeSine(start, R/8, V/4, 400) 
      writeSine(start, R/8, V/4, 300) 
      writeSine(start, R/8, V/4, 200)
      writeSine(start, R/12, V/32, 100) 
      writeSine(start, R/16, V/32, 50)

  def writeNoteBeats(interval):
    for beat in range(DURATION * 2 * interval):
      start = tempo * beat / interval
      writeNoise(start, R/64, V/128)
      writeNoise(start, R/32, V/512)
      writeNoise(start, R/16, V/1024)

  writeDownbeats()
  writeNoteBeats(note_beats)
  writeUpbeats(up_beats, {
    2:1,
    3:2,
    4:2,
    5:3,
  }[up_beats])

  for value in values:
    outf.writeframesraw(struct.pack('<h', value))

  outf.close()

if __name__ == "__main__":
  for tempo, tempo_name in [
    (R / 2, "120bpm"),
    (2 * R / 3, "90bpm"),
    ]:
    write('t8-march-%s.wav' % tempo_name, tempo, 2, 2)
    write('t8-jig-%s.wav' % tempo_name, tempo, 3, 3)
    write('t8-reel-%s.wav' % tempo_name, tempo, 4, 4)
    write('t8-teneight-%s.wav' % tempo_name, tempo, 5, 5)
    write('t8-teneight-over-jig-%s.wav' % tempo_name, tempo, 3, 5)
