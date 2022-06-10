def check_time_format(time):
    if (len(time)<8):
        return False
    
    splited_time = time.split(':')
    if (len(splited_time)!=3):
        return False

    hours, minutes, seconds = splited_time
    for time in splited_time:
        if (not time.isnumeric()):
            return False

    if (len(hours)!=2 or len(minutes)!=2 or len(seconds)!=2):
        return False
    
    return True