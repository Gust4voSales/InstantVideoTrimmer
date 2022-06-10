import os
import subprocess

TEMP_OUTPUT_FILE_NAME = 'out'

def parse_cuts_file_to_commands(input_video_name):
    lines = ['00:00:00,00:00:00']
    # create array with each line
    with open('cuts.txt') as file:
        for line in file:
            lines.append(line.rstrip())

    # loop through the lines and create command that will include the desired part of the video (removing the cuts)
    commands = []
    for index, line in enumerate(lines):
        part_to_include_initial_time = line.split(',')[1]

        if (index==len(lines)-1):
            part_to_include_end_time = 'end'
        else:
            part_to_include_end_time = lines[index+1].split(',')[0]

        # commented parts increase accuracy
        if (part_to_include_end_time!='end'):
            commands.append(f'ffmpeg -ss {part_to_include_initial_time}.00 -i {input_video_name} -to {part_to_include_end_time}.00 -c copy {TEMP_OUTPUT_FILE_NAME+str(index)}.mp4')
            # commands.append(f'ffmpeg -ss {part_to_include_initial_time}.00 -i {input_video_name} -to {part_to_include_end_time}.00 {TEMP_OUTPUT_FILE_NAME+str(index)}.mp4')
        else:
            commands.append(f'ffmpeg -ss {part_to_include_initial_time}.00 -i {input_video_name} -c copy {TEMP_OUTPUT_FILE_NAME+str(index)}.mp4')
            # commands.append(f'ffmpeg -ss {part_to_include_initial_time}.00 -i {input_video_name} {TEMP_OUTPUT_FILE_NAME+str(index)}.mp4')
    
    return commands

def cut_video(commands):
    file_name = 'video_cuts.txt'
    with open(file_name, 'w') as f:
        for index, command in enumerate(commands):
            subprocess.call(command.split(' '))
            f.write(f"file '{TEMP_OUTPUT_FILE_NAME + str(index)}.mp4'\n")
    return file_name    

def concatenate_videos(file_name):
    subprocess.call(['ffmpeg', '-y', '-f', 'concat', '-i', file_name, '-c', 'copy', 'output.mp4'])
    

def clear_temp_data(cuts_file_name, video_cuts_length):
    os.remove(cuts_file_name)
    for index in range(video_cuts_length):
        os.remove(f'{TEMP_OUTPUT_FILE_NAME+str(index)}.mp4')


def run(input_video_name):
    commands = parse_cuts_file_to_commands(input_video_name)
    file_name = cut_video(commands)
    concatenate_videos(file_name)

    clear_temp_data(file_name, len(commands))
