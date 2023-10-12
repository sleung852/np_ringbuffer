from unittest import TestCase
from unittest.mock import MagicMock, patch
import numpy as np

from np_ringbuffer.ringbuffer import NumpyRingBuffer, TimedNumpyRingBuffer


class TestTimedNumpyRingBuffer(TestCase):

    @patch("time.time_ns")
    def test_add_simple(self, mock_time_ns):
        mock_time_ns.side_effect = [5_000_000, 5_000_000]
        timed_ring_buffer = TimedNumpyRingBuffer(interval_ms=5, capacity=5)
        timed_ring_buffer.add(1)
        self.assertEqual(timed_ring_buffer[0], 1)

    @patch("time.time_ns")
    def test_add_latest(self, mock_time_ns):
        mock_time_ns.side_effect = [5_000_000, 5_000_000, 10_000_001, 10_000_001]
        timed_ring_buffer = TimedNumpyRingBuffer(interval_ms=5, capacity=5)
        timed_ring_buffer.add(1)
        self.assertEqual(timed_ring_buffer[0], 1)
        timed_ring_buffer.add(2)
        self.assertEqual(timed_ring_buffer[0], 1)
        self.assertEqual(timed_ring_buffer[1], 2)

    @patch("time.time_ns")
    def test_add_with_gaps(self, mock_time_ns):
        mock_time_ns.side_effect = [5_000_000, 5_000_000, 20_000_001, 20_000_001]
        timed_ring_buffer = TimedNumpyRingBuffer(interval_ms=5, capacity=5)
        timed_ring_buffer.add(1)
        self.assertEqual(timed_ring_buffer[0], 1)
        timed_ring_buffer.add(2)
        self.assertEqual(timed_ring_buffer[0], 1)
        self.assertEqual(timed_ring_buffer[1], 0)
        self.assertEqual(timed_ring_buffer[2], 2)

    def test_blocked_fns(self):
        timed_ring_buffer = TimedNumpyRingBuffer(interval_ms=5, capacity=5)
        with self.assertRaises(AttributeError):
            timed_ring_buffer.append(1)
        with self.assertRaises(AttributeError):
            timed_ring_buffer.add_to_latest(1)