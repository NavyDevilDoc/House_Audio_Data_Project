import csv
import numpy as np
import time

def write_to_csv(filename, data):
    with open(filename, "a", newline="") as avgfile:
        avg_writer = csv.writer(avgfile)
        avg_writer.writerow(["Timestamp", "Counter", "Rolling_Avg (ADC)", "Rolling_Avg (dB)"])
        avg_writer.writerows(data)


def calc_rolling_avg(samples):
    return np.convolve(samples, np.ones(10)/10, mode='valid')

def get_current_timestamp():
    return time.strftime("%Y-%m-%d %H:%M:%S")
