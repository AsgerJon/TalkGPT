"""DidUHearSomething is a class whose instances wait for a sound and the
triggers a callback function"""
#  Copyright (c) 2023 Asger Jon Vistisen
#  All Rights Reserved
#  This software is licensed under the MIT License.
#  SPDX-License-Identifier: MIT
from __future__ import annotations

import struct
import math
import time

import pyaudio
from worktoy import searchKeys, maybeType, maybe


class DidUHearSomething:
  """Records sound one second at a time and triggers a callback function
  if any voice is heard."""

  def __init__(self, callback):
    """Initializes a new DidUHearSomething instance.

    Args:
        callback: A function that will be called when voice is detected.
    """
    self.chunk_size = 1024
    self.sample_rate = 44100
    self.stream = None
    self.callback = callback
    audio = pyaudio.PyAudio()
    mic_index = None
    for i in range(audio.get_device_count()):
      info = audio.get_device_info_by_index(i)
      if 'jlab' in info['name'].lower() and info['maxInputChannels'] > 0:
        mic_index = info['index']
        break
    if mic_index is None:
      raise ValueError(
        'No microphone containing "jlab" in its name was found')

    self.device = mic_index

    audio.terminate()

  def start(self, *args, **kwargs):
    """Starts recording audio and detecting voice."""
    timeLimitKwarg = searchKeys('timeLimit', 'time') @ (int, float) >> kwargs
    timeLimitFloatArg = maybeType(float, *args)
    timeLimitIntArg = maybeType(int, *args)
    timeLimitArg = maybe(timeLimitFloatArg, timeLimitIntArg)
    timeLimitDefault = 2
    timeLimit = maybe(timeLimitKwarg, timeLimitArg, timeLimitDefault)
    print('sets time limit to: %s' % (timeLimit))
    audio = pyaudio.PyAudio()
    print(audio.get_default_input_device_info())
    self.stream = audio.open(
      format=pyaudio.paInt16,
      channels=1,
      rate=self.sample_rate,
      input=True,
      frames_per_buffer=self.chunk_size
    )
    tic = time.time()
    seconds = 0
    while True:
      data = self.stream.read(self.chunk_size, exception_on_overflow=False)
      rms = self.get_rms(data)
      if rms > 0.05:  # adjust threshold as necessary
        self.callback()
      if timeLimit is not None:
        elapsed = time.time() - tic
        if elapsed > timeLimit:
          break
        if elapsed > seconds:
          print('Time left: %d' % (timeLimit - seconds))
          print(rms)
          seconds += 1

  def get_rms(self, data):
    """Calculates the root-mean-square (RMS) amplitude of the given audio
    data.

    Args:
        data: Audio data in bytes.

    Returns:
        The RMS amplitude as a float.
    """
    count = len(data) / 2
    format = "%dh" % count
    shorts = struct.unpack(format, data)
    sum_squares = 0.0
    for sample in shorts:
      n = sample * (1.0 / 32768)
      sum_squares += n * n
    rms = math.sqrt(sum_squares / count)
    return rms
