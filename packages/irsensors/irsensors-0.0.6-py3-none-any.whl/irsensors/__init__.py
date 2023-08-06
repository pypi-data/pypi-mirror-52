#!/usr/bin/env python3
# -*-coding:utf-8 -*


"""This package allows to read data from an IR sensor set connected by USB.

This package expect the IR sensor set to send string encode line data as follow:
"ID,Error_Code,Distance,.........,\r\n". What is between the third and the fourth comma does not matter.

This package uses the serial package. You can install it with "pip install serial" command.

In this version, the sensor ID can not be more than 9 (if it is more than 9, it will cause a bug).

"""


__version__ = "0.0.6"


from irsensors.irsensorset import IRSensorSet


if __name__ == "__main__":
	try:
		pass

	except KeyboardInterrupt:
		pass

	finally:
		pass
