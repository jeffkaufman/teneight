import wave
import struct
import math
import random

R = 44100
V = 32767/2
DURATION = 16

def write(fname, tempo):
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
      start = tempo*beat + tempo*beat_number/interval
      writeSine(start, R/8, V/2, 800)
      writeSine(start, R/8, V/4, 400)
      writeSine(start, R/8, V/4, 300)
      writeSine(start, R/8, V/4, 200)
      writeSine(start, R/12, V/32, 100)
      writeSine(start, R/16, V/32, 50)

  def writeNote(start):
    writeNoise(start, R/64, V/128)
    writeNoise(start, R/32, V/512)
    writeNoise(start, R/16, V/1024)

  def writeNoteBeats():
    for beat in range(DURATION*2):
      start = tempo*beat
      if (beat//2) % 2 == 0:
        writeNote(start + 0*tempo/4)
        writeNote(start + 1*tempo/4)
        writeNote(start + 2*tempo/4)
        writeNote(start + 3*tempo/4)
      else:
        writeNote(start + 0*tempo/5)
        writeNote(start + 1*tempo/5)
        writeNote(start + 2*tempo/5)
        writeNote(start + 3*tempo/5)
        writeNote(start + 4*tempo/5)

  writeDownbeats()
  writeNoteBeats()
  writeUpbeats(4, 2)

  for value in values:
    outf.writeframesraw(struct.pack('<h', value))

  outf.close()

if __name__ == "__main__":
  for tempo, tempo_name in [
    (R / 2, "120bpm"),
    (2 * R / 3, "90bpm"),
    ]:
    write('t8-reel-teneight-alternate-%s.wav' % tempo_name, tempo)
