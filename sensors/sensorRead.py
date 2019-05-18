import serial
import time

ser = serial.Serial()
# !!!!!!!!!!!!!!!!!
# Different for different computers
ser.port = '/dev/cu.usbmodem1421'
# !!!!!!!!!!!!!!!!!
ser.baudrate = 9600

# Returns:
# tuple(string, string, string), (ir, humidity, temperature)
def get_ir_hum_temp():
  ser.open()

  # Throw away the first line
  ser.readline()

  data_split = str(ser.readline()).split('|')
  ser.close()
  return (data_split[1], data_split[2], data_split[3])
