import serial
import os
import time
from config import COM_PORT, BAUD_RATE, DOWNSAMPLE_FACTOR, SAMPLING_INTERVAL
from utils import write_to_csv, calc_rolling_avg, get_current_timestamp
from adc_to_db import process_audio_data

def main():
    ser = serial.Serial(COM_PORT, BAUD_RATE)
    counter, entry_counter, avg_counter, file_counter = 0, 0, 0, 1
    start_time = last_reset_time = time.time()
    samples = []
    minute_counter = 0

    print("Data recording has started...")

    adc_samples = []
    db_samples = []

    while True:
        try:
            line = ser.readline().decode('utf-8').strip()
            adc_value = int(line)  # Convert the line to integer (assuming it's just the ADC value)
            db_value = process_audio_data(adc_value)
            
            counter += 1
    
            # Downsample
            if counter % DOWNSAMPLE_FACTOR == 0:
                adc_samples.append(int(line))
                db_samples.append(db_value)  # Append the dB value, not the raw ADC value
                entry_counter += 1
    
            elapsed_since_reset = time.time() - last_reset_time
            if elapsed_since_reset >= (minute_counter + 1) * 60:
                minute_counter += 1
                print(f"{minute_counter} minute(s) has elapsed for this CSV file.")
    
            elapsed_time = time.time() - start_time
            if elapsed_time >= SAMPLING_INTERVAL:
                adc_rolling_avg = calc_rolling_avg(adc_samples)
                db_rolling_avg = calc_rolling_avg(db_samples)
                
                timestamp = get_current_timestamp()
                data_to_write = [[timestamp, i+1, adc_avg, db_avg] for i, (adc_avg, db_avg) in enumerate(zip(adc_rolling_avg, db_rolling_avg))]
                file_path = os.path.join("data_file_storage", f"rolling_avg_{file_counter}.csv")
                write_to_csv(file_path, data_to_write)    
                
                print(f"5-minute mark reached. Rolling averages calculated and saved. Resets initiated. {file_counter} CSV files generated.")
                last_reset_time = time.time()
                minute_counter = 0
                counter = 0
                start_time = time.time()
                samples.clear()
                file_counter += 1
    
        except KeyboardInterrupt:
            print("Stopped by user.")
            break


if __name__ == '__main__':
    main()
