from np_ringbuffer import NumpyRingBuffer, TimedNumpyRingBuffer
import random
import time
import numpy as np

# construct from an existing numpy array
ringbuffer = NumpyRingBuffer.create_from_array(np.array([1,2,3]))
ringbuffer.append(3)
print(ringbuffer.values())  # [2,3,3]
ringbuffer.add_to_latest(10)
print(ringbuffer.values()) # [2,3,13]

# construct an empty buffer with 5 capacity
ringbuffer = NumpyRingBuffer(capacity=10)
ringbuffer.append(3)
print(ringbuffer.values())  # [3]
ringbuffer.add_to_latest(10)
print(ringbuffer.values()) # [13]

# automate the append and add_to_latest with interval_ms
timed_ringbuffer = TimedNumpyRingBuffer(interval_ms=60_000, capacity=10)
timed_ringbuffer.add(1)

# volume 1-second bar example
def generate_volume() -> float:
    return random.random() * 100

def get_volume(iterations: int = 1_000_000, pause_ms: float = 1e-5):
    for _ in range(iterations):
        time.sleep(pause_ms)
        yield generate_volume()

timed_ringbuffer = TimedNumpyRingBuffer(interval_ms=1000, capacity=10)
for volume in get_volume():
    timed_ringbuffer.add(volume)
print(timed_ringbuffer.values())