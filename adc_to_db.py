'''
import math
import numpy as np
from config import ADC_MAX_VALUE, REFERENCE_VOLTAGE, V_REF, SPL_REF

def adc_to_volts(adc_value, adc_max_value=ADC_MAX_VALUE, reference_voltage=REFERENCE_VOLTAGE):
    return np.abs((adc_value / adc_max_value) * reference_voltage)

def volts_to_dB(volts, v_ref=V_REF, spl_ref=SPL_REF):
    if volts <= 0:  # Avoid log(0) which is undefined
        return float(0)
    return 20 * math.log10(volts / v_ref) + spl_ref

def process_audio_data(adc_value):
    # print(f"ADC Value: {adc_value}")  # Debug print
    volts = adc_to_volts(adc_value)
    # print(f"Volts: {volts}")  # Debug print
    db = volts_to_dB(volts)
    # print(f"dB: {db}")  # Debug print
    return db
'''

import math
#import numpy as np
from config import ADC_MAX_VALUE, REFERENCE_VOLTAGE, V_REF, SPL_REF

def adc_to_volts(adc_value, adc_max_value=ADC_MAX_VALUE, reference_voltage=REFERENCE_VOLTAGE):
    return (adc_value / adc_max_value) * reference_voltage

def rms(values):
    return math.sqrt(sum(x ** 2 for x in values) / len(values))

def volts_to_dB(volts, v_ref=V_REF, spl_ref=SPL_REF):
    if volts <= 0:  # Avoid log(0) which is undefined
        return float(0)
    return 20 * math.log10(volts / v_ref) + spl_ref

def process_audio_data(adc_values):
    if isinstance(adc_values, int):
        adc_values = [adc_values]
        
    volts = [adc_to_volts(val) for val in adc_values]
    #print(f"Volts: {volts}")  # Debug print
    rms_volts = rms(volts)
    db = volts_to_dB(rms_volts)
    #print(f"dB: {db}")  # Debug print
    return db

