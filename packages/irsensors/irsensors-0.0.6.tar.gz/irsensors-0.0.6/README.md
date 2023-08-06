irsensors - This package allows to read datas from an IR sensor set connected by USB.
========================================================

This package allows to read datas from an IR sensor set connected by USB.

This package expect the IR sensor set to send string encode line datas as follow:
"sensorID,errorCode,distance,"

This package uses the serial package. You can install it with "pip install serial" command.

In this version, the sensor ID can not be more than 9 (if it is more than 9, it will cause a bug).


You can install it with pip:

	pip install irsensors


Application example:

	import time

	import irsensors

	sensor = irsensors.IRSensorSet()
    try:
        sensor.start()

        while True:
            print(sensor)
            time.sleep(0.1)

    except KeyboardInterrupt:
        pass

    finally:
        sensor.stop()