from datetime import datetime
def get_diff_milliseconds(time1, time2):
    return (time2 - time1).total_seconds() * 1000