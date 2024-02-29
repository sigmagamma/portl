import os
import sys
import wave
import contextlib


def get_duration(wave_folder,file_name):
    try:
        with contextlib.closing(wave.open(os.path.join(wave_folder, file_name), 'r')) as f:
            frames = f.getnframes()
            rate = f.getframerate()
            return round(frames / float(rate), 6)
    except Exception:
        print("problem with file {}".format(file_name))

def rewrite_scene(speech_folder, src_scene_filename, target_scene_filename, scene_map):
    with open(src_scene_filename,errors="ignore") as source_scene, open(target_scene_filename, "w") as target_scene:
        current_time = 0
        stopped=False
        for line in source_scene:
            if stopped:
                target_scene.write(line)
            elif line.strip().startswith('event speak'):
                event = line.split()[2].strip('"')
                event_details = scene_map[event.lower()]
                event_gap = event_details['start_time']
                if event_gap is None or event_gap is '':
                    stopped=True
                    target_scene.write(line)
                    continue
                target_scene.write(line)
                target_scene.write(source_scene.readline())
                actual_start_time = current_time + float(event_gap)
                actual_end_time = actual_start_time + get_duration(speech_folder, event_details.get('audiofile')+".wav")
                out_line = "      time "+"{:.6f}".format(actual_start_time)+" "+"{:.6f}".format(actual_end_time)+"\n"
                current_time = actual_end_time
                target_scene.write(out_line)
            elif not line.strip().startswith('time'):
                target_scene.write(line)


if __name__ == '__main__':
    rewrite_scene(sys.argv[1],sys.argv[2],sys.argv[3],{'narration.new1_welcome_00':{'start_time':0.02,
                                                                                    'audiofile':'new1_welcome_00.wav'},
                                                        'narration.new1_welcome_01':{'start_time':0.009728,'audiofile':
                                                                                    'new1_welcome_01.wav'},
                                                       'narration.new1_welcome_02': {'start_time': -0.006279,
                                                                                     'audiofile': 'new1_welcome_02.wav'},
                                                       'narration.new1_welcome_03': {'start_time': 0.013764,
                                                                                     'audiofile': 'new1_welcome_03.wav'
                                                                                     }})