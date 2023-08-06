#!/usr/bin/env python3
# -*-coding:utf-8 -*


import serial


if __name__ == "__main__":
    sensor = serial.Serial("COM22", 9600, timeout=1)	# Open an USB communication
    try:
        sensor.write(b"1")	# Write "1" in the USB communication to ask the sensor to send data
        while True:	# infinite loop
            data = sensor.readline()	# Read one line of data
            data = data.decode().split(",")[:-1]	# Decompose the data and erase the new line caracters
            data[0] = data[0][-1]	# Rewrite the sensor's ID
            print(data)

    except KeyboardInterrupt:
        pass

    finally:
        sensor.write(b"0")	# Write "0" in the USB communication to ask the sensor to stop to send data
        sensor.close()	# Close the USB communication
