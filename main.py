import time
import yaml
from serial_processor import SerialManager
from utils import track_time, calc_rolling_avg, get_current_timestamp
from database_processor import DatabaseManager
from audio_processor import AudioProcessor

def read_config(filename):
    with open(filename, 'r') as file:
        return yaml.safe_load(file)

def main():
    # Read the configuration and initialize classes and variables
    config = read_config('config.yml')
    serial_manager = SerialManager(config)
    
    db_manager = DatabaseManager("audio_data.db")
    audio_processor = AudioProcessor(config)
    
    serial_manager.init_serial()
    db_manager.create_audio_db_and_table()
    
    # Variables
    start_time = last_reset_time = time.time()
    minute_counter = counter = file_counter = 0
    adc_samples = []
    db_samples = []
    file_counter = 1
    print("Data recording has started...")

    while True:
        try:
            line = serial_manager.read_from_serial()
            if line is not None:
                # Update samples and counter
                adc_samples, db_samples, counter = audio_processor.accumulate_samples(line, adc_samples, db_samples, counter, config['DOWNSAMPLE_FACTOR'])
                
                # Check timing
                minute_counter, time_to_save = track_time(start_time, last_reset_time, minute_counter, config['SAMPLING_INTERVAL'])
    
                if time_to_save:
                    timestamp = get_current_timestamp()
                    
                    # Calculate rolling averages
                    adc_rolling_avg = calc_rolling_avg(adc_samples)
                    db_rolling_avg = calc_rolling_avg(db_samples)
                                        
                    # Preparing batch data
                    data_batch = [(timestamp, i+1, adc_avg, db_avg) for i, (adc_avg, db_avg) in enumerate(zip(adc_rolling_avg, db_rolling_avg))]

                    # Batch insert into database
                    db_manager.insert_audio_data_batch(data_batch)

                    print(f"5-minute mark reached. Rolling averages calculated and saved. Resets initiated. {file_counter} intervals completed.")
                    
                    # Reset counters and time
                    start_time = time.time()
                    last_reset_time = time.time()
                    minute_counter = 0
                    counter = 0
                    adc_samples.clear()
                    db_samples.clear()
                    file_counter += 1
    
        except KeyboardInterrupt:
            print("Stopped by user.")
            break

if __name__ == '__main__':
    main()
