import time
import numpy as np
from unittest import TestCase
from unittest.mock import MagicMock, patch


class NumpyRingBuffer:
    def __init__(self, capacity: int, dtype: np.dtype = float):
        assert isinstance(capacity, int), "capacity must be of type int"
        self.capacity = capacity
        self.size = 0
        self._buffer = np.zeros(capacity, dtype=dtype)
        self._idx = -1

    def append(self, value):
        self._idx = (self._idx + 1) % self.capacity
        self._buffer[self._idx] = value
        if self.size < self.capacity:
            self.size += 1

    def add_to_latest(self, value):
        if self._idx == -1:
            self.size = 1
            self._idx = 0
        self._buffer[self._idx] += value

    def last(self):
        return self._buffer[self._idx]

    def first(self):
        if self.size < self.capacity:
            return self._buffer[0]
        start_idx = (self._idx + 1) % self.capacity
        return self._buffer[start_idx]

    def mean(self):
        if self.size == self.capacity:
            return self._buffer.mean()
        return self._buffer[:self.size].mean()

    def values(self):
        if self.size == self.capacity:
            start_idx = (self._idx + 1) % self.capacity
            return np.concatenate([self._buffer[start_idx:], self._buffer[:self._idx + 1]])
        return self._buffer[:self._idx+1]

    def __getitem__(self, idx: int):
        if idx >= self.size or idx < self.size * -1:
            raise IndexError(f"Array only contain {self.size} elements, cannot access {idx}th element")
        real_idx = (self._idx + 1 + idx) % self.size
        return self._buffer[real_idx]

    @classmethod
    def create_from_array(cls, array: np.array):
        instance = cls(len(array), array.dtype)
        instance._buffer = array
        instance.size = len(array)
        return instance


class TimedNumpyRingBuffer(NumpyRingBuffer):
    def __init__(self, interval_ms: int, capacity: int, dtype: np.dtype = float):
        super().__init__(capacity, dtype)
        self.interval_ns = interval_ms * 1_000_000
        self._set_next_time()

    def _set_next_time(self):
        current_time = time.time_ns()
        self.next_time = current_time - current_time % self.interval_ns + self.interval_ns

    def add(self, value):
        current_time = time.time_ns()
        if current_time < self.next_time:
            super().add_to_latest(value)
        else:
            overflow = (current_time - self.next_time) // self.interval_ns - 1
            for _ in range(overflow):
                super().append(0.0)
            super().append(value)
            self._set_next_time()

    def append(self, value):
        raise AttributeError("TimedNumpyRingBuffer forbids access to NumpyRingBuffer.append")

    def add_to_latest(self, value):
        raise AttributeError("TimedNumpyRingBuffer forbids access to NumpyRingBuffer.add_to_latest")

    @classmethod
    def create_from_array(cls, array: np.array, interval_ms: int):
        instance = cls(interval_ms, len(array), array.dtype)
        instance._buffer = array
        instance.size = len(array)
        return instance

