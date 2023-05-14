"""SoundSecond records audio and returns it one second at a time."""
#  Copyright (c) 2023 Asger Jon Vistisen
#  All Rights Reserved
#  This software is licensed under the MIT License.
#  SPDX-License-Identifier: MIT
from __future__ import annotations

from typing import Any, NoReturn

import sounddevice as sd
from worktoy import maybeType, searchKeys, maybe, CallMeMaybe


class SoundSecond:
  """SoundSecond records audio and returns it one second at a time.
  #  Copyright (c) 2023 Asger Jon Vistisen
  #  All Rights Reserved
  #  This software is licensed under the MIT License.
  #  SPDX-License-Identifier: MIT"""

  @staticmethod
  def _blankCallBackFactory() -> CallMeMaybe:
    """Blank placeholder callback function"""

    @CallMeMaybe(True)
    def func(*__, **_) -> bool:
      """Blank function"""
      return False

    return func

  @staticmethod
  def getDeviceNamed(name: str) -> Any:
    """Getter-function for device by name"""
    devices = sd.query_devices()
    for idx, device in enumerate(devices):
      inChannels = device.get('max_input_channels', 0)
      deviceName = device.get('name', '').lower()
      if inChannels and deviceName:
        if name.lower() in deviceName:
          return device

  def __init__(self, *args, **kwargs) -> None:
    deviceKwarg = searchKeys('name', 'device') @ str >> kwargs
    deviceArg = maybeType(str, *args)
    deviceDefault = 'JLab'
    self._deviceName = maybe(deviceKwarg, deviceArg, deviceDefault)
    callBackKwarg = searchKeys('callBack', ) >> kwargs
    callBackArg = maybeType(str, *args)
    callBackDefault = None
    self._callBack = maybe(callBackKwarg, callBackArg, callBackDefault)

  def callBack(self, *args, **kwargs) -> Any:
    """Invokes the callback function"""
    if self._callBack is not None:
      return self._callBack(*args, **kwargs)

  def _setCallBack(self, callBack: CallMeMaybe) -> NoReturn:
    """Setter-function for callBack function"""
    self._callBack = callBack

  def _getDeviceName(self) -> str:
    """Getter-function for the name of the device to be used"""
    return maybe(self._deviceName, 'JLab')

  def _setDeviceName(self, name: str) -> NoReturn:
    """Setter-function for the name of the device to be used"""
    self._deviceName = name

  def _delDeviceName(self, ) -> NoReturn:
    """Illegal deleter function"""
    raise TypeError('Illegal deletion attempted!')

  def _getDevice(self) -> Any:
    """Getter-function for the device to be used"""
    return self.getDeviceNamed(self.deviceName)

  def _setDevice(self, *_) -> NoReturn:
    """Illegal setter-function"""
    raise TypeError('Read only variable!')

  def _delDevice(self, ) -> NoReturn:
    """Illegal setter-function"""
    raise TypeError('Read only variable!')

  def _record(self, ) -> Any:
    """Records and transmit sound at the given file name"""
    # set sampling frequency and duration for recording
    fs = 44100
    duration = 1.0

    # record audio for 1 second
    recording = sd.rec(int(fs * duration),
                       samplerate=fs,
                       channels=1,
                       blocking=True,
                       device=self.device)

    return self._callBack(recording)

  def _transmit(self, callBack: CallMeMaybe) -> Any:
    """Records some sound and transmits it to callback"""
    self._setCallBack(callBack)
    return callBack(self._record())

  deviceName = property(_getDeviceName, _setDeviceName, _delDeviceName)
  device = property(_getDevice, _setDevice, _delDevice)
