import os
import sys
import csv

# arg[1] - folder with scene files
# arg[2] - path to csv file with names of relevant scenes
if __name__ == '__main__':
    lines = []
    with open(sys.argv[2], encoding="utf-8-sig") as csv_file:
        csv_reader = csv.DictReader(csv_file)
        for scenes_line in csv_reader:
            scene_filename = scenes_line['scene']
            scene_path = os.path.join(sys.argv[1],scene_filename)
            if os.path.exists(scene_path):
                with open(scene_path) as scene_file:
                    current_time = 0
                    for line in scene_file:
                        if line.strip().startswith('event speak'):
                            out_line = scene_filename + ',' + line.split()[2]+','
                            scene_file.readline()
                            times = scene_file.readline().split()
                            gap = float(times[1])-current_time
                            current_time = float(times[2])
                            out_line += str(gap)
                            print(out_line)
