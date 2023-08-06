python-ew
=========

This is a 2019 updating of the [PythonEw](https://github.com/osop/osop-python-ew) Python 2.x compatible modules by
[OSOP](http://www.osop.com.pa) to work with Python 3.x

`python-ew` is a Python wrapper for accessing a Earthworm shared memory rings, allowing you to extend the Earthworm
system with Python code.

[Earthworm](http://earthwormcentral.org) itself is a set of open source programs, tools and libraries that are used in
the development of software for maintaining seismic networks, research and other seismological and geophysical
applications.

**Supported message types**:

* `TYPE_HEARTBEAT`: `python_ew.HeartBeatRing`
* `TYPE_STATUS`: `python_ew.StatusRing`, `python_ew.StatusMessage`
* `TYPE_TRACEBUF2`: `python_ew.Tracebuf2Ring`, `python_ew.Tracebuf2Message`


## Installation

In order to install `python-ew`, you need to have first installed Earthworm itself.  This module builds successfully on
Linux against `earthworm-7.9` compiled with `EWBITS=64` and with "`-m64 -fPIC`" added to `GLOBALFLAGS` in
`${EW_HOME}/environment/ew_linux.bash`.  Your milage may vary for other versions of Earthworm, or on other platforms.

To compile the `python-ew` C extensions, we need to find the Earthworm `.o` and `.h` files.  We'll look in the following
places:

Libraries:

* `${EW_HOME}/lib`
* `${EW_HOME}/earthworm_7.9/lib`

Include files:

* `${EW_HOME}/include`
* `${EW_HOME}/earthworm_7.9/include`

Thus, ensure that the `EW_HOME` environment variable is set apporpriately.

Then:

```
pip install python-ew
```

## Example usage

### Reading TRACEBUF2 messages

Let's say your ring with `TYPE_TRACEBUF2` messages is named `WAVE_RING`, and you want to get all messages regardless of
what module created them:

```
> python3
>>> from python_ew import Tracebuf2Ring
>>> ring = Tracebuf2Ring('WAVE_RING', 'MOD_WILDCARD')
>>> messages = ring.read()
>>> messages[0]
{'pinno': 0, 'nsamp': 100, 'starttime': 1564770703.968393, 'endtime': 1564770704.958393, 'samprate': 100.0, 'sta': 'FOO', 'net': 'XX', 'chan': 'HNN', 'loc': '--', 'version': '20', 'datatype': 'i4', 'quality': '', 'pad': '', 'samples': [-22129, -22130, -22131, -22132, -22129, -22130, -22128, -22128, -22130, -22128, -22130, -22128, -22128, -22129, -22129, -22129, -22129, -22130, -22127, -22128, -22129, -22128, -22128, -22130, -22131, -22128, -22131, -22131, -22128, -22128, -22132, -22130, -22125, -22128, -22129, -22126, -22128, -22130, -22133, -22132, -22131, -22132, -22130, -22131, -22128, -22129, -22132, -22127, -22129, -22129, -22129, -22132, -22130, -22127, -22129, -22131, -22127, -22128, -22131, -22128, -22128, -22130, -22129, -22130, -22129, -22128, -22133, -22128, -22129, -22133, -22131, -22130, -22128, -22131, -22130, -22128, -22132, -22132, -22129, -22127, -22129, -22132, -22130, -22132, -22133, -22128, -22129, -22130, -22129, -22130, -22128, -22129, -22130, -22131, -22130, -22128, -22129, -22130, -22129, -22129]}
````
