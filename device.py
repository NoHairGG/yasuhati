import pyaudio
import numpy
import audioop

print("line2")
pa = pyaudio.PyAudio()
print("line3")
print(pa.get_device_count())
print("line4")
print(pa.get_default_input_device_info())
print("line5")
print(pa.get_default_output_device_info())
for i in range(pa.get_device_count()):
    dev = pa.get_device_info_by_index(i)
    print((i,dev['name'],dev['maxInputChannels'],dev['defaultSampleRate']))
    #print(dev)
stream = pa.open(format = pyaudio.paInt16,channels=1,rate=44100,input_device_index=3,input=True)
numpy.set_printoptions(threshold=numpy.inf)
f = open("demofile2.txt", "a")
count = 0
while True and count < 1000:
        raws=stream.read(1024, exception_on_overflow = False)
        samples=numpy.frombuffer(raws, dtype=numpy.int16)
        #result = str(samples)
        #f.write(result)
        rms = audioop.rms(samples, 2)
        print(rms)
        count = count + 1
