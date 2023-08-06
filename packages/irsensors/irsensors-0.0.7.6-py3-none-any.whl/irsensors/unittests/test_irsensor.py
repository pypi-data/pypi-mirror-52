#!/usr/bin/env python3
# -*-coding:utf-8 -*


from unittest import TestCase, main
from random import randrange, random

from irsensors.irsensor import IRSensor, mean


class IRSensorTest(TestCase):
	"""This class test the IRSensor methods, plus the mean function defined in the same file."""
	def test_mean(self):
		"""Test the mean function."""
		# Check the function return None if the List is empty or None.
		self.assertIsNone(mean([]))
		self.assertIsNone(mean(None))

		# Check if the function return the correct random list's mean value.
		list_test = [randrange(0, 1000)/100 for i in range(20)]
		mean_value = sum(list_test)/len(list_test)
		self.assertEqual(mean_value, mean(list_test))


	def test_write(self):
		"""Test the write method in the IRSensor class."""
		# When the method write is launched, check that the first item of the history list is the latest value given as parameter.
		# Check also if the distance attribute stay the mean of the history list.
		# Check the history list size does not change.
		test_sensor = IRSensor(id=random())
		LEN = len(getattr(test_sensor, "_history"))
		values = [randrange(0, 1000)/100 for i in range(20)]
		for value in values:
			test_sensor.write(id=test_sensor["ID"], distance=value, error=0)
			self.assertEqual(getattr(test_sensor, "_history")[0], value)
			self.assertEqual(test_sensor["distance"], mean(getattr(test_sensor, "_history")))
			self.assertEqual(len(test_sensor), LEN)

		# Check that the distance does not change if the id is not the right one.
		distance_value = test_sensor["distance"]
		test_sensor.write(id=test_sensor["ID"] + 1, distance=distance_value + 5, error=0)
		self.assertEqual(distance_value, test_sensor["distance"])

		# Check if the method returns None when at least one of his parameter is None.
		self.assertIsNone(test_sensor.write(None, random(), 0))
		self.assertIsNone(test_sensor.write(test_sensor["ID"], None, 0))
		self.assertIsNone(test_sensor.write(test_sensor["ID"], random(), None))


if __name__ == "__main__":
	try:
		main()

	except KeyboardInterrupt:
		pass

	finally:
		pass
