"""WhatsThatPunk triggers a callback function when a voice is heard"""
#  Copyright (c) 2023 Asger Jon Vistisen
#  All Rights Reserved
#  This software is licensed under the MIT License.
#  SPDX-License-Identifier: MIT
from __future__ import annotations

import asyncio
import os
from typing import Optional

import speech_recognition as sr
from worktoy import CallMeMaybe, maybe


class WhatsThatPunk:
  def __init__(self,
               callback: CallMeMaybe,
               energy_threshold: Optional[int] = None,
               dynamic_energy_threshold: Optional[bool] = None):
    """
    Initializes the WhatsThatPunk instance.

    Args:
        callback (CallMeMaybe): The function to be called when voice is
        detected.
        energy_threshold (Optional[int], optional): Sets the energy
        threshold for voice detection. Defaults to None.
        dynamic_energy_threshold (Optional[bool], optional): Enables or
        disables dynamic energy threshold. Defaults to None.
    """
    self.callback = callback
    self.recognizer = sr.Recognizer()
    self._apikey: Optional[str] = None
    self.recognizer.energy_threshold = maybe(energy_threshold, 300)
    self.recognizer.dynamic_energy_threshold = maybe(
      dynamic_energy_threshold,
      False)

  async def record(self):
    loop = asyncio.get_running_loop()
    with sr.Microphone() as source:
      print(f"Using microphone: {source}")
      while True:
        print('lol')
        audio_data = self.recognizer.listen(source, phrase_time_limit=1.0)
        is_voice_task = loop.run_in_executor(
          None, self.recognizer.recognize_google_cloud,
          audio_data, credentials_json=self.apikey)
        is_voice: str = await asyncio.wrap_future(is_voice_task)
        if is_voice != "":
          loop.run_in_executor(None, self.callback)

  @property
  def apikey(self) -> str:
    if self._apikey is None:
      self.create_apikey()
    return self._apikey

  def create_apikey(self) -> None:
    self._apikey = os.environ.get('SPEECH_TO_TEXT_API')
    if self._apikey is None:
      raise Exception(
        "Please set the SPEECH_TO_TEXT_API environment variable.")
