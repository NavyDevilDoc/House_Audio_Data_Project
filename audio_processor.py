import math
import yaml

class AudioProcessor:

    def __init__(self, config):
        self.adc_max_value = config['ADC_MAX_VALUE']
        self.reference_voltage = config['REFERENCE_VOLTAGE']
        self.v_ref = config['V_REF']
        self.spl_ref = config['SPL_REF']

    def read_config(self, filename):
        with open(filename, 'r') as file:
            return yaml.safe_load(file)

    def adc_to_volts(self, adc_value):
        return (adc_value / self.adc_max_value) * self.reference_voltage

    def rms(self, values):
        return math.sqrt(sum(x ** 2 for x in values) / len(values))

    def volts_to_dB(self, volts):
        if volts <= 0:
            return float(0)
        return 20 * math.log10(volts / self.v_ref) + self.spl_ref

    def process_audio_data(self, adc_values):
        if isinstance(adc_values, int):
            adc_values = [adc_values]
        volts = [self.adc_to_volts(val) for val in adc_values]
        rms_volts = self.rms(volts)
        db = self.volts_to_dB(rms_volts)
        return db

    def accumulate_samples(self, line, adc_samples, db_samples, counter, DOWNSAMPLE_FACTOR):
        adc_value = int(line)
        db_value = self.process_audio_data(adc_value)
        counter += 1
        if counter % DOWNSAMPLE_FACTOR == 0:
            adc_samples.append(adc_value)
            db_samples.append(db_value)
        return adc_samples, db_samples, counter
