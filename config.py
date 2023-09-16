
# Serial port settings
COM_PORT = 'COM10'
BAUD_RATE = 9600

# Sampling settings
DOWNSAMPLE_FACTOR = 16 # 16 KHz to 1 KHz
SAMPLING_INTERVAL = 300  # 5 minutes in seconds

# Constants (Based on Arduino documentation)
ADC_MAX_VALUE = 65535    # 16-bit ADC
REFERENCE_VOLTAGE = 3.3  # 3.3V reference on the ADC
V_REF = 1.0              # Reference voltage for dB conversion
SPL_REF = 94             # Reference SPL level for the microphone
