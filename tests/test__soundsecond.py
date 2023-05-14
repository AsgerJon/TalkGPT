"""Testing SoundSecond"""
#  Copyright (c) 2023 Asger Jon Vistisen
#  All Rights Reserved
#  This software is licensed under the MIT License.
#  SPDX-License-Identifier: MIT
from __future__ import annotations

import unittest
from typing import Any

from talk2me import SoundSecond


class TestSoundSecond(unittest.TestCase):
  """Test suite for the SoundSecond class"""

  def test_get_device_named(self) -> None:
    """Test the getDeviceNamed staticmethod"""
    device_name = "JLab"  # name of device to search for
    device = SoundSecond.getDeviceNamed(device_name)
    self.assertIsInstance(device, dict)
    self.assertIn(device_name.lower(), device["name"].lower())
    self.assertGreater(device["max_input_channels"], 0)

  def test_call_back(self) -> None:
    """Test the callBack method"""
    test_value = "this is a test"
    sound_second = SoundSecond()
    sound_second._setCallBack(lambda x: x)
    result = sound_second.callBack(test_value)
    self.assertEqual(result, test_value)

  def test_record(self) -> None:
    """Test the _record method"""
    sound_second = SoundSecond()
    result = sound_second._record()
    self.assertIsInstance(result, Any)

  def test_transmit(self) -> None:
    """Test the _transmit method"""
    test_value = "this is a test"
    sound_second = SoundSecond(callBack=lambda x: test_value)
    result = sound_second._transmit(lambda x: x)
    self.assertEqual(result, test_value)


if __name__ == '__main__':
  unittest.main()
