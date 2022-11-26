import os
import sys
import wave
import contextlib

if __name__ == '__main__':
        for fname in os.listdir(sys.argv[1]):
            try:
                with contextlib.closing(wave.open(os.path.join(sys.argv[1],fname), 'r')) as f:
                    frames = f.getnframes()
                    rate = f.getframerate()
                    duration = round(frames / float(rate),3)
                    print("{},{}".format(fname,duration))
            except Exception as e:
                print("problem with file {}".format(fname))