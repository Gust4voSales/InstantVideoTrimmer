from datetime import timedelta

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

def subtract_times(start_time, end_time):
    start = timedelta(hours=int(start_time[0:2]), minutes=int(start_time[3:5]), seconds=int(start_time[6:8]))
    end = timedelta(hours=int(end_time[0:2]), minutes=int(end_time[3:5]), seconds=int(end_time[6:8]))
    
    return str(end-start)

def get_time_total_seconds(time):
    return timedelta(hours=int(time[0:2]), minutes=int(time[3:5]), seconds=int(time[6:8])).total_seconds()