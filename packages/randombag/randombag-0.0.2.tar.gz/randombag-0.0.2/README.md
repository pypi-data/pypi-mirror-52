# randombag
randombag is a python package to handle a multi-set (bag) with a pseudo-random pop. The bag supports all set operations in constant time.

## How does it Work?
Internally, the bag is represented by a list.

Whenever a new element is added into the bag, it is shuffled in place of a random element, which is then inserted to the front of the list. This is the only time in which randomness is invoked.

The bag also contains a dict mapping elements to their indices, to support constant-time removal.

## The Random Buffer
To support fast random insertion, randombag will use numpy if it can be found. If randombag finds numpy, it will use a pre-calculated buffer or random numbers from numpy. The buffer's size will be equal to the bag's current size, up to a maximum that can be set in the bag's constructor (`random_buffer_max_size`, 1024 by default). Buffer behaviour is ignored if numpy cannot be imported.

## Reproducibility
A useful feature of random bags is that each bag can contain its own random generator. This feature can be used by setting the `seed` parameter in `RandomBag` constructor.

A RandomBag with a seed can also be cloned to reproduction. If a new `RandomBag` is made from a seeded `RandomBag`, then the internal random generator is cloned, such that the random behavior will be identical between the two. This behaviour can be disabled by setting the random seed of the new bag, or by setting it to `False`.