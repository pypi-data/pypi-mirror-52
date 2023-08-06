dictondisk
==========

It's a thing that implements a dictionary, but in a temporary directory.

Why?
---

I had a machine with not a lot of RAM and a script that was RAM-hungry.
Instead of optimizing the script i did _this_ montrostity.

Should you use it?
------------------

Probably not. It's slow. I'm almost certain there are many security flaws in this approach.  

How to use dictondisk?
----------------------

```python
from dictondisk import DictOnDisk

some_dict = DictOnDisk()

some_dict[1] = "One"
some_dict[2] = "Two"
some_dict[3] = "Three"

del some_dict[1]

for key, value in some_dict.items():
    print(key, value)

```

Comparison to the vanilla dict
------------------------------

|            Action            | dict() | DictOnDisk() |
|------------------------------|--------|--------------|
| len(d)                       |   ✔️    |      ✔️       |
| d[key]                       |   ✔️    |      ✔️       |
| d[key] = value               |   ✔️    |      ✔️       |
| del d[key]                   |   ✔️    |      ✔️       |
| key in d                     |   ✔️    |      ✔️       |
| key not in d                 |   ✔️    |      ✔️       |
| iter(d)                      |   ✔️    |      ✔️       |
| d.clear()                    |   ✔️    |      ✔️       |
| d.copy()                     |   ✔️    |      ✔️       |
| d.fromkeys()                 |   ✔️    |      ✔️       |
| d.get(key[, default])        |   ✔️    |      ✔️       |
| d.items()                    |   ✔️    |      ✔️       |
| d.keys()                     |   ✔️    |      ✔️       |
| d.pop(key[, default])        |   ✔️    |      ✔️       |
| d.popitem()                  |   ✔️    |      ✔️       |
| d.setdefault(key[, default]) |   ✔️    |      ❌      |
| d.update([other])            |   ✔️    |      ✔️       |
| d.values()                   |   ✔️    |      ✔️       |
| Preserve insertion order     |   ✔️    |      ❌      |
| bool(d)                      |   ✔️    |      ✔️       |
| d1 == d2                     |   ✔️    |      ✔️       |
| d1 != d2                     |   ✔️    |      ✔️       |
