from copy import copy
from typing import MutableSet
from warnings import warn

from randombag.roller import Roller, numpy_enabled


class RandomBag(MutableSet):
    """
    A pseudo-random multiset
    """

    def __init__(self, iterable=(), random_buffer_max_size=None, seed=None):
        """
        :param iterable: an initial iterable to be inserted into the bag
        :param random_buffer_max_size: the maximum size of the random buffer
        :param seed: A random seed to use. By default, uses the random generator.
        """
        self._list = list(iterable)

        if isinstance(iterable, RandomBag) and seed is None:
            self._roller = copy(iterable._roller)
        else:
            self._roller = Roller(seed)
            self._roller.shuffle(self._list)

        self._dict = {k: i for (i, k) in enumerate(self._list)}

        if random_buffer_max_size is None:
            random_buffer_max_size = 1024
        elif not numpy_enabled:
            warn('numpy could not be imported, random_buffer_max_size is ignored')
        self._buffer_max_size = random_buffer_max_size

    def add(self, x) -> None:
        if x in self._dict:
            return

        if not self._list:
            self._list.append(x)
            self._dict[x] = 0
        else:
            ind = int(
                self._roller.get(min(
                    self._buffer_max_size,
                    len(self) + 1
                )) * len(self)
            )
            self._list.append(self._list[ind])
            self._list[ind] = x

            self._dict[self._list[-1]] = len(self._list) - 1
            self._dict[x] = ind

    def __len__(self):
        return len(self._list)

    def popn(self, n):
        """
        remove multiple elements from the bag
        :param n: number of elements to remove
        :return: a list of the removed elements
        """
        s = slice(len(self._list) - 1, len(self._list) - n - 1, -1)
        ret = self._list[s]
        del self._list[s]
        for k in ret:
            del self._dict[k]
        return ret

    def pop(self):
        return self.popn(1)[0]

    def _remove_ind(self, ind):
        if ind != len(self._list) - 1:
            new_elem = self._list[ind] = self._list[-1]
            self._dict[new_elem] = ind

        self._list.pop()

    def discard(self, x):
        ind = self._dict.pop(x, None)
        if ind is not None:
            self._remove_ind(ind)

    def remove(self, x):
        ind = self._dict.pop(x, None)
        if ind is None:
            raise KeyError(x)
        else:
            self._remove_ind(ind)

    def __contains__(self, item):
        return item in self._dict

    def __iter__(self):
        return (yield from self._list)

    def clear(self) -> None:
        self._list.clear()
        self._dict.clear()

    def __repr__(self):
        return type(self).__name__ + '(' + repr(self._list) + ')'
