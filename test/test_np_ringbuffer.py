from unittest import TestCase
from unittest.mock import MagicMock, patch
import numpy as np

from np_ringbuffer.ringbuffer import NumpyRingBuffer, TimedNumpyRingBuffer



class TestNumpyRingBuffer(TestCase):

    def test_create_from_array(self):
        array = np.array([1,2,3,4])
        ring_buff = NumpyRingBuffer.create_from_array(array)
        self.assertEqual(ring_buff.capacity, 4)
        self.assertEqual(ring_buff.size, 4)

    def test_empty_add_latest(self):
        ring_buff = NumpyRingBuffer(4)
        ring_buff.add_to_latest(1)
        self.assertEqual(ring_buff.size, 1)

    def test_append_while_full(self):
        array = np.array([1,2,3,4], dtype=float)
        ring_buff = NumpyRingBuffer.create_from_array(array)
        ring_buff.append(5)
        self.assertEqual(ring_buff._buffer[0], 5)

    def test_basic_append(self):
        ring_buff = NumpyRingBuffer(4)
        ring_buff.append(1)
        self.assertEqual(ring_buff._buffer[0], 1)
        ring_buff.append(2)
        self.assertEqual(ring_buff._buffer[1], 2)

    def test_overflow_append(self):
        ring_buff = NumpyRingBuffer(4)
        for i in range(1, 6):
            ring_buff.append(i)
        self.assertEqual(ring_buff._buffer[0], 5)
        self.assertEqual(ring_buff._buffer[3], 4)

    def test_values(self):
        array = np.array([1, 2, 3, 4])
        ring_buff = NumpyRingBuffer.create_from_array(array)
        self.assertTrue((ring_buff.values() == array).all())

    def test_values_not_full(self):
        ring_buff = NumpyRingBuffer(4)
        for i in range(1, 3):
            ring_buff.append(i)
        self.assertEqual(ring_buff.size, 2)
        self.assertEqual(len(ring_buff.values()), 2)

    def test_first_last(self):
        ring_buff = NumpyRingBuffer(4)
        for i in range(1, 3):
            ring_buff.append(i)
        self.assertEqual(ring_buff.first(), 1)
        self.assertEqual(ring_buff.last(), 2)
        array = np.array([1, 2, 3, 4])
        ring_buff = NumpyRingBuffer.create_from_array(array)
        self.assertEqual(ring_buff.first(), 1)
        self.assertEqual(ring_buff.last(), 4)
        ring_buff.append(5)
        self.assertEqual(ring_buff.first(), 2)
        self.assertEqual(ring_buff.last(), 5)

    def test_latest(self):
        array = np.array([1, 2, 3, 4])
        ring_buff = NumpyRingBuffer.create_from_array(array)
        ring_buff.add_to_latest(10)
        self.assertEqual(ring_buff._buffer[3], 14)

    def test_get_index_at_capacity(self):
        array = np.array([1, 2, 3, 4])
        ring_buff = NumpyRingBuffer.create_from_array(array)
        self.assertEqual(ring_buff[0], 1)
        ring_buff.append(5)
        self.assertEqual(ring_buff[0], 2)
        self.assertEqual(ring_buff[3], 5)
        self.assertEqual(ring_buff[-1], 5)
        self.assertEqual(ring_buff[-4], 2)
        with self.assertRaises(IndexError):
            ring_buff[-5]
        with self.assertRaises(IndexError):
            ring_buff[10]

    def test_get_index_size(self):
        ring_buff = NumpyRingBuffer(5)
        with self.assertRaises(IndexError):
            ring_buff[0]
        ring_buff.append(1)
        self.assertEqual(ring_buff[0], 1)
        self.assertEqual(ring_buff[-1], 1)
        ring_buff.append(2)
        self.assertEqual(ring_buff[0], 1)
        self.assertEqual(ring_buff[-1], 2)