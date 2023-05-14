"""Testing DidUHearSomething"""
#  Copyright (c) 2023 Asger Jon Vistisen
#  All Rights Reserved
#  This software is licensed under the MIT License.
#  SPDX-License-Identifier: MIT
from __future__ import annotations

from unittest import skip, TestCase
from unittest.mock import MagicMock

from talk2me import DidUHearSomething


class TestDidUHearSomething(TestCase):

  @skip
  def test_callback_is_called_when_voice_is_detected(self):
    # Create a mock callback function that we can use to verify it's called
    callback = MagicMock()

    # Create a new instance of DidUHearSomething with the mock callback
    dhs = DidUHearSomething(callback)

    # Call start() on the instance to start recording audio
    frames = dhs.start(5)

    # Verify that the callback was called at least once
    self.assertGreater(callback.call_count, 0)
