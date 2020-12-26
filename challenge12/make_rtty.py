# Try generating RTTY WAV files in Python

import fileinput
import wave
import numpy

string = 'MANOLO'

baud = 50.0
tone_duration = 1.0/50.0
samplerate = 8000.0
samples = tone_duration * samplerate
frequency_mark = 500.0
frequency_space = 1000.0
period_mark = samplerate / frequency_mark
period_space = samplerate / frequency_space
omega_mark = numpy.pi * 2.0 / period_mark
omega_space = numpy.pi * 2.0 / period_space

x_mark = numpy.arange(int(period_mark), dtype=numpy.float) * omega_mark
x_space = numpy.arange(int(period_space), dtype=numpy.float) * omega_space

y_mark = 2**14 * numpy.sin(x_mark)
y_space = 2**14 * numpy.sin(x_space)

mark = numpy.resize(y_mark, (samples,))
space = numpy.resize(y_space, (samples,))

binary_mark = ''
for i in range(len(mark)):
    binary_mark += wave.struct.pack('h', mark[i])
binary_space = ''
for i in range(len(space)):
    binary_space += wave.struct.pack('h', space[i])

wav = wave.open('rtty.wav', 'wb')
wav.setnchannels(1)
wav.setsampwidth(2)
wav.setframerate(samplerate)

print 'binary_mark:', binary_mark, type(binary_mark)
print 'binary_space:', binary_space, type(binary_space)

data = []
for i in xrange(30):
    wav.writeframes(binary_mark)

for char in string:
    binary = ord(char)
    wav.writeframes(binary_space)
    for shift in range(7):
        if binary & (1<<shift):
            wav.writeframes(binary_mark)
        else:
            wav.writeframes(binary_space)
    wav.writeframes(binary_mark)
    wav.writeframes(binary_mark)
    wav.writeframes(binary_mark)
    wav.writeframes(binary_mark)

wav.close()
