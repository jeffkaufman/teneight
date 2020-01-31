import wave
import struct
import math
import random

R = 44100
V = 32767/3
DURATION = 4

def write(fname, tempo):
  outf = wave.open(fname, 'w')
  outf.setnchannels(1) # mono
  outf.setsampwidth(2)
  outf.setframerate(R)

  values = [0]*(int(R * DURATION))

  def emit(start, offset, value):
    pos = start + offset
    while pos >= len(values):
      values.append(0)
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

  def writeLowNote(start, root):
    writeSine(start, R/8, V/2, root) 
    writeSine(start, R/8, V/2, root/2) 
    writeSine(start, R/8, V/3, root/3) 
    writeSine(start, R/8, V/4, root/4)
    writeSine(start, R/12, V/32, root/8) 
    writeSine(start, R/16, V/32, root/16)
    writeSine(start, R/20, V/2048, root/64)

  def writeLowLongNote(start, root, length):
    writeSine(start, length, V/64, root) 
    writeSine(start, length, V/64, root/2) 
    writeSine(start, length, V/64, root/3) 
    writeSine(start, length, V/128, root/4)
    writeSine(start, length, V/256, root/8) 

  def writeNote(start, note):
    writeSine(start, R/32, V/16, note)
    writeSine(start, R/64, V/32, note/2)
    writeSine(start, R/128, V/32, note/3)
    writeSine(start, R/128, V/64, note/4)

  def writeTss(start):
    writeNoise(start, R/64, V/64)
    writeNoise(start, R/32, V/256)
    writeNoise(start, R/16, V/512)

  T = 1.0595

  N8 = 1600
  N7 = N8 * T
  N6 = N7 * T * T
  N5 = N6 * T * T
  N4 = N5 * T * T
  N3 = N4 * T
  N2 = N3 * T * T
  N1 = N2 * T * T

  wlen = {'1': N1,
          '2': N2,
          '3': N3,
          '4': N4,
          '5': N5,
          '6': N6,
          '7': N7,
          '8': N8}
  
  drone = """
    1 4 1 4
    1 4 1 4

    6 6 4 4
    6 6 5 5
  """

  i = 0
  for c in drone:
    if not c.strip():
      continue

    if c == '0':
      pass
    else:
      writeLowLongNote(i, wlen[c], tempo*4)

    i += tempo*4
  
  highdrone = """
    5 3 4 0   5 3 4 0
    5 3 4 1   2 3 4 5

    8 8 3 3   4 4 5 5
    8 8 3 3   2 2 5 4
  """

  i = 0
  for c in highdrone:
    if not c.strip():
      continue

    if c == '0':
      pass
    else:
      writeLowLongNote(i, wlen[c]/4, tempo*2)

    i += tempo*2
  


  bass = """
    1 5   1 5
    4 8   4 2
    1 5   1 5
    4 8   5 3

    1 5   1 5
    4 8   4 2
    1 5   1 5
    4 8   5 3

    6 6   6 6
    8 7   6 5
    4 4   4 4
    8 7   6 5
    
    6 6   6 6
    8 7   6 6
    5 5   4 4
    3 3   2 2
  """

  i = 0
  for c in bass:
    if not c.strip():
      continue

    if c == '0':
      pass
    else:
      writeLowNote(i, wlen[c])

    writeTss(i + 7*tempo/16)

    i += tempo

  melody = """
    1 0 5 8 5    1 0 5 8 2
    1 0 5 8 5    1 0 5 8 3

    4 0 4 8 2    4 0 6 8 5
    4 0 4 8 2    4 0 6 8 2

    1 0 5 8 5    1 0 5 8 2
    1 0 5 8 5    1 0 5 8 3

    4 0 4 8 2    4 0 6 8 6
    5 4 5 7 6    5 4 5 6 7

    1 0 5 8 5    1 0 5 8 2
    1 0 5 8 5    1 0 5 8 3

    4 0 4 8 2    4 0 6 8 5
    4 0 4 8 2    4 0 6 8 2

    1 0 5 8 5    1 0 5 8 2
    1 0 5 8 5    1 0 5 8 3

    4 0 4 8 2    4 0 6 8 6
    1 2 3 4 5    6 7 5 6 7



    8 0 8 8 8    0 8 7 8 7
    8 0 8 8 8    0 8 7 8 7

    8 0 8 8 8    0 8 7 8 7
    8 8 7 6 6    5 5 6 5 5

    4 0 4 4 4    0 4 5 4 5
    4 0 4 4 4    0 4 5 4 5

    4 0 4 4 4    0 4 5 4 5
    4 4 5 6 6    5 5 6 7 7

    8 0 8 8 8    0 8 7 8 7
    8 0 8 8 8    0 8 7 8 7

    8 0 8 8 8    0 8 7 8 7
    8 8 7 6 6    5 5 6 5 4

    5 0 5 4 5    0 3 5 4 5
    4 0 4 3 4    0 2 4 3 4
   
    3 0 3 2 3    2 1 2 3 4
    5 5 5 0 5    0 5 5 4 5
  """

  i = 0
  for c in melody:
    if not c.strip():
      continue

    if c == '0':
      pass
    else:
      writeNote(i, wlen[c] / 32)

    i += tempo/5

  for value in values:
    outf.writeframesraw(struct.pack('<h', value))
  for value in values:
    outf.writeframesraw(struct.pack('<h', value))

  outf.close()

if __name__ == "__main__":
  for tempo, tempo_name in [
    (R / 2, "120bpm"),
#    (2 * R / 3, "90bpm"),
    ]:
    write('t8-melodic-%s.wav' % tempo_name, tempo)
