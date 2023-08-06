try:
    import numpy.random as random
except ImportError:
    import random

    numpy_enabled = False


    class Roller:
        def __init__(self, seed=None):
            self._generator = random.Random(seed) if (seed is not None) and (seed is not False) else random

        def get(self, next_buffer_size):
            return self._generator.uniform(0, 1)

        def shuffle(self, seq):
            return self._generator.shuffle(seq)

        def can_copy_state(self):
            return self._generator is not random

        def __copy__(self):
            ret = type(self)()
            if self.can_copy_state():
                ret._generator.setstate(self._generator.getstate())
            return ret
else:
    numpy_enabled = True


    class Roller:
        def __init__(self, seed=None):
            self._buffer = ()
            self._next_ind = 0
            self._generator = random.RandomState(seed) if (seed is not None) and (seed is not False) else random

        def get(self, next_buffer_size):
            if self._next_ind == len(self._buffer):
                self._buffer = self._generator.uniform(size=next_buffer_size)
                self._next_ind = 0
            ret = self._buffer[self._next_ind]
            self._next_ind += 1
            return ret

        def shuffle(self, seq):
            return self._generator.shuffle(seq)

        def can_copy_state(self):
            return self._generator is not random

        def __copy__(self):
            ret = type(self)()
            if self.can_copy_state():
                ret._buffer = self._buffer
                ret._next_ind = self._next_ind
                ret._generator.set_state(self._generator.get_state())
            return ret
