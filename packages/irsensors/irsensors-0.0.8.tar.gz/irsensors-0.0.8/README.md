irsensors - This package allows to read data from an IR sensor set connected by USB.
========================================================

This package allows to read data from an IR sensor set connected by USB.

This package expect the IR sensor set to send string encode line data as follow:
"sensorID,errorCode,distance,.........,\r\n". What is between the third and the fourth comma does not matter.

This package uses the pyserial package. You can install it with "pip install pyserial" command.

In this version, the sensor ID can not be more than 9 (if it is more than 9, it will cause a bug).


You can install it with pip:

	pip install irsensors


Application example:

	from time import sleep

	from irsensors import IRSensorSet


	sensor = IRSensorSet("COM22")
    try:
        sensor.start()

        while True:
            print(sensor)
            sleep(0.1)

    except KeyboardInterrupt:
        pass

    finally:
        sensor.stop()
        del sensor
