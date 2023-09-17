import csv
import numpy as np
import time

def write_to_csv(filename, data):
    with open(filename, "w", newline="") as avgfile:  # Note the "w" here
        avg_writer = csv.writer(avgfile)
        avg_writer.writerow(["Timestamp", "Counter", "Rolling_Avg (ADC)", "Rolling_Avg (dB)"])
        avg_writer.writerows(data)


def calc_rolling_avg(samples):
    return np.convolve(samples, np.ones(10)/10, mode='valid')


def get_current_timestamp():
    return time.strftime("%Y-%m-%d %H:%M:%S")


def track_time(start_time, last_reset_time, minute_counter, SAMPLING_INTERVAL):
    elapsed_since_reset = time.time() - last_reset_time
    elapsed_time = time.time() - start_time
    
    if elapsed_since_reset >= (minute_counter + 1) * 60:
        minute_counter += 1
        print(f"{minute_counter} minute(s) of data recording has elapsed.")
    
    time_to_save = elapsed_time >= SAMPLING_INTERVAL
    
    return minute_counter, time_to_save
