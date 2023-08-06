# decrunch_unity
A clone of [decrunch](https://github.com/HearthSim/decrunch) which uses [Unity's crunch version](https://github.com/Unity-Technologies/crunch).


## Setup

- To install directly from PyPI: `pip install decrunch_unity`
- To install from source: `pip install Cython`, then `./setup.py install`


## Usage

```py
import decrunch_unity

with open("example.crn", "rb") as f:
	buf = f.read()

fi = decrunch_unity.File(buf)
tex_info = fi.info()

for level in range(tex_info["levels"]):
	print("Level info %i: %r" % (level, fi.info(level)))

with open("out.bc1", "wb") as f:
	f.write(fi.decode_level(0))
```

Further image decoding requires a DXTn decompressor, such as the one that
can be found in [Pillow](https://github.com/python-pillow/Pillow) as `bcn`.

## License

The full license text is available in the `LICENSE` file.
See crunch/license.txt for the license of files in the `crunch/` subdirectory.

The files in `crunch/` are an unaltered subset of the original code; the
entirety of crunch may be obtained at <https://github.com/BinomialLLC/crunch>.
