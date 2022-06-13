import os
from utils import TimeHelper
import subprocess

TEMP_OUTPUT_FILE_NAME = 'out'
TEMP_CUTS_VIDEOS_FILE_NAME = 'cuts_files.txt'
TEMP_CUTS_TIMESTAMPS_FILE_NAME = 'cuts.txt'


def generate_cuts_file(cuts):
    with open(TEMP_CUTS_TIMESTAMPS_FILE_NAME, 'w') as f:
        f.write('\n'.join(cuts))

def parse_cuts_file_to_commands(input_video_name):
    lines = []
    input_video_duration = subprocess.check_output(['ffprobe', '-v', 'error', '-show_entries', 'format=duration', '-of', 'default=noprint_wrappers=1:nokey=1', input_video_name]) 
    input_video_duration = int(float(input_video_duration.decode('utf-8').replace('\r\n', '')))

    # create array with each line
    with open(TEMP_CUTS_TIMESTAMPS_FILE_NAME) as file:
        for index, line in enumerate(file):
            if (index == 0 and (line.split(',')[0] != "00:00:00")):
                lines.append('00:00:00,00:00:00')
            lines.append(line.rstrip())

    # loop through the lines and create command that will include the desired part of the video (removing the cuts)
    commands = []
    for index, line in enumerate(lines):
        part_to_include_initial_time = line.split(',')[1]

        if (index==len(lines)-1):
            if (TimeHelper.get_time_total_seconds(line.split(',')[1]) < input_video_duration):
                part_to_include_end_time = 'end'
            else: 
                part_to_include_end_time = None
        else:
            part_to_include_end_time = TimeHelper.subtract_times(part_to_include_initial_time, lines[index+1].split(',')[0])

        # commented parts increase accuracy
        if (part_to_include_end_time=='end'):
            commands.append(f'ffmpeg -loglevel quiet -ss {part_to_include_initial_time}.00 -i {input_video_name} -c copy {TEMP_OUTPUT_FILE_NAME+str(index)}.mp4')
            # commands.append(f'ffmpeg -ss {part_to_include_initial_time}.00 -i {input_video_name} {TEMP_OUTPUT_FILE_NAME+str(index)}.mp4')
        elif (part_to_include_end_time!='end' and part_to_include_end_time):
            commands.append(f'ffmpeg -loglevel quiet -ss {part_to_include_initial_time}.00 -i {input_video_name} -to {part_to_include_end_time}.00 -c copy {TEMP_OUTPUT_FILE_NAME+str(index)}.mp4')
            # commands.append(f'ffmpeg -ss {part_to_include_initial_time}.00 -i {input_video_name} -to {part_to_include_end_time}.00 {TEMP_OUTPUT_FILE_NAME+str(index)}.mp4')

    return commands

def cut_video(commands):
    with open(TEMP_CUTS_VIDEOS_FILE_NAME, 'w') as f:
        for index, command in enumerate(commands):
            subprocess.call(command.split(' '))
            f.write(f"file '{TEMP_OUTPUT_FILE_NAME + str(index)}.mp4'\n")

def concatenate_videos(output_name):
    subprocess.call(['ffmpeg', '-loglevel', 'quiet', '-y', '-f', 'concat', '-i', TEMP_CUTS_VIDEOS_FILE_NAME, '-c', 'copy', output_name])
    

def clear_temp_data(video_cuts_length):
        os.remove(TEMP_CUTS_VIDEOS_FILE_NAME)
        os.remove(TEMP_CUTS_TIMESTAMPS_FILE_NAME)
        for index in range(video_cuts_length):
            os.remove(f'{TEMP_OUTPUT_FILE_NAME+str(index)}.mp4')


def run(cuts, input_video_name):
    generate_cuts_file(cuts)
    commands = parse_cuts_file_to_commands('media/'+input_video_name)
    cut_video(commands)
    concatenate_videos('media/'+'out_'+input_video_name)

    print(commands)
    clear_temp_data(len(commands))
    print('FIM')

# cuts = [
#     "00:00:30,00:00:50", 
#     # "00:00:00,00:00:30", 
#     "00:04:34,00:05:59", 
#     "00:21:36,00:23:50", 
# ]

# run(cuts, "NarutoEP1.mp4")