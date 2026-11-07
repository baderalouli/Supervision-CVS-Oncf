from collections import deque


class MovingAverageFilter:

    def __init__(self, window_size=5):

        self.window_size = window_size

        self.buffers = {
            "voltage": deque(maxlen=window_size),
            "output_voltage": deque(maxlen=window_size),
            "current": deque(maxlen=window_size),
            "power": deque(maxlen=window_size),
            "temperature": deque(maxlen=window_size),
            "internal_temperature": deque(maxlen=window_size),
            "vibration": deque(maxlen=window_size),
            "battery": deque(maxlen=window_size),
            "efficiency": deque(maxlen=window_size)
        }

    def update(self, data):

        filtered_data = data.copy()

        for parameter in self.buffers:

            value = data[parameter]

            self.buffers[parameter].append(value)

            average = sum(
                self.buffers[parameter]
            ) / len(
                self.buffers[parameter]
            )

            filtered_data[parameter] = round(
                average,
                2
            )

        return filtered_data

    def reset(self):

        for buffer in self.buffers.values():
            buffer.clear()