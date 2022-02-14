# pyrtcm

[Current Status](#currentstatus) |
[Installation](#installation) |
[Reading](#reading) |
[Parsing](#parsing) |
[Generating](#generating) |
[Serializing](#serializing) |
[Examples](#examples) |
[Extensibility](#extensibility) |
[Graphical Client](#gui) |
[Author & License](#author)

## !!! WORK IN PROGRESS - NOT YET FULLY FUNCTIONAL !!!

`pyrtcm` is an original Python 3 library for the RTCM 3 &copy; protocol.

The `pyrtcm` homepage is located at [https://github.com/semuconsulting/pyrtcm](https://github.com/semuconsulting/pyrtcm).

This is an independent project and we have no affiliation whatsoever with RTCM.

**FYI** There are companion libraries which handles standard NMEA 0183 &copy; and UBX &copy; (u-blox) GNSS/GPS messages.
- [pynmeagps](http://github.com/semuconsulting/pynmeagps)
- [pyubx2](http://github.com/semuconsulting/pyubx2)

## <a name="currentstatus">Current Status</a>

![Status](https://img.shields.io/pypi/status/pyrtcm)
![Release](https://img.shields.io/github/v/release/semuconsulting/pyrtcm)
![Build](https://img.shields.io/github/workflow/status/semuconsulting/pyrtcm/pyrtcm)
![Codecov](https://img.shields.io/codecov/c/github/semuconsulting/pyrtcm)
![Release Date](https://img.shields.io/github/release-date-pre/semuconsulting/pyrtcm)
![Last Commit](https://img.shields.io/github/last-commit/semuconsulting/pyrtcm)
![Contributors](https://img.shields.io/github/contributors/semuconsulting/pyrtcm.svg)
![Open Issues](https://img.shields.io/github/issues-raw/semuconsulting/pyrtcm)

Currently under development and not yet uploaded to PyPi Test or Prod. May or may not be taken forward depending on
time constraints and availability of payload documentation and test resources. As it stands, only a limited subset of RTCM message types are defined, though these can be extended by adding appropriate definitions to `rtcmtypes_*.py` - contributions welcome!

Sphinx API Documentation in HTML format is available at [https://www.semuconsulting.com/pyrtcm](https://www.semuconsulting.com/pyrtcm).

Contributions welcome - please refer to [CONTRIBUTING.MD](https://github.com/semuconsulting/pyrtcm/blob/master/CONTRIBUTING.md).

[Bug reports](https://github.com/semuconsulting/pyrtcm/blob/master/.github/ISSUE_TEMPLATE/bug_report.md) and [Feature requests](https://github.com/semuconsulting/pyrtcm/blob/master/.github/ISSUE_TEMPLATE/feature_request.md) - please use the templates provided.

---
## <a name="installation">Installation</a>

**NB** NOT YET AVAILABLE IN PYPI PROD - I may post an Alpha to PyPi TEST if there's sufficient interest.

`pyrtcm` is compatible with Python 3.6+ and has no third-party library dependencies.

In the following, `python` & `pip` refer to the Python 3 executables. You may need to type 
`python3` or `pip3`, depending on your particular environment.

![Python version](https://img.shields.io/pypi/pyversions/pyrtcm.svg?style=flat)
[![PyPI version](https://img.shields.io/pypi/v/pyrtcm.svg?style=flat)](https://pypi.org/project/pyrtcm/)
![PyPI downloads](https://img.shields.io/pypi/dm/pyrtcm.svg?style=flat)

The recommended way to install the latest version of `pyrtcm` is with
[pip](http://pypi.python.org/pypi/pip/):

```shell
python -m pip install --upgrade pyrtcm
```

If required, `pyrtcm` can also be installed into a virtual environment, e.g.:

```shell
python -m pip install --user --upgrade virtualenv
python -m virtualenv env
source env/bin/activate (or env\Scripts\activate on Windows)
(env) python -m pip install --upgrade pyrtcm
...
deactivate
```

---
## <a name="reading">Reading (Streaming)</a>

```
class pyrtcm.rtcmreader.RTCMReader(stream, *args, **kwargs)
```

You can create a `RTCMReader` object by calling the constructor with an active stream object. 
The stream object can be any data stream which supports a `read(n) -> bytes` method (e.g. File or Serial, with 
or without a buffer wrapper).

Individual input rtcm and/or NMEA messages can then be read using the `RTCMReader.read()` function, which returns both the raw binary data (as bytes) and the parsed data (as a `RTCMMessage`, via the `parse()` method). The function is thread-safe in so far as the incoming data stream object is thread-safe. `RTCMReader` also implements an iterator.

The constructor accepts the following optional keyword arguments:

* `quitonerror`: 0 = ignore errors, 1 = log errors and continue (default), 2 = (re)raise errors and terminate
* `validate`: VALCKSUM (0x01) = validate checksum (default), VALNONE (0x00) = ignore invalid checksum or length

Example -  Serial input. This example will output both rtcm and NMEA messages:
```python
>>> from serial import Serial
>>> from pyrtcm import RTCMReader
>>> stream = Serial('/dev/tty.usbmodem14101', 9600, timeout=3)
>>> rtr = RTCMReader(stream)
>>> (raw_data, parsed_data) = rtr.read()
>>> print(parsed_data)
```

Example - File input (using iterator).
```python
>>> from pyrtcm import RTCMReader
>>> stream = open('rtcmdata.bin', 'rb')
>>> rtr = rtcmReader(stream)
>>> for (raw_data, parsed_data) in rtr: print(parsed_data)
...
```

---
## <a name="parsing">Parsing</a>

You can parse individual rtcm messages using the static `RTCMReader.parse(data)` function, which takes a bytes array containing a binary rtcm message and returns a `RTCMMessage` object.

**NB:** Once instantiated, a `RTCMMessage` object is immutable.

The `parse()` method accepts the following optional keyword arguments:

* `validate`: VALCKSUM (0x01) = validate checksum (default), VALNONE (0x00) = ignore invalid checksum or length

Example:
```python
>>> from pyrtcm import RTCMReader
>>> msg = RTCMReader.parse(b">\xd0\x00\x03\x8aX\xd9I<\x87/4\x10\x9d\x07\xd6\xafH ")
>>> print(msg)
<rtcm(NAV-VELNED, iTOW=16:01:48, velN=-3, velE=-15, velD=-4, speed=16, gSpeed=15, heading=1.28387, sAcc=65, cAcc=80.5272)>
```

The `RTCMMessage` object exposes different public attributes depending on its message type or 'identity',
e.g. the `1005` message has the following attributes:

```python
>>> print(msg)
<RTCM(1005, iTOW=16:01:54, lon=-2.1601284, lat=52.6206345, height=86327, hMSL=37844, hAcc=38885, vAcc=16557)>
>>> msg.identity
'1005'
>>> msg.lat, msg.lon
(52.6206345, -2.1601284)
>>> msg.hMSL/10**3
37.844
```

Attributes within repeating groups are parsed with a two-digit suffix (svid_01, svid_02, etc.). The `payload` attribute always contains the raw payload as bytes.

---
## <a name="generating">Generating</a>

(see [below](#configinterface) for special methods relating to the rtcm configuration interface)

```
class pyrtcm.rtcmmessage.RTCMMessage(payload, **kwargs)
```

You can create a `rtcmMessage` object by calling the constructor with the following parameters:
1. payload as bytes
2. (optional) a series of keyword parameters representing the message payload

Example:

```python
>>> from pyrtcm import RTCMMessage
>>> msg = RTCMMessage(b">\xd0\x00\x03\x8aX\xd9I<\x87/4\x10\x9d\x07\xd6\xafH ")
>>> print(msg)
<RTCM(1005, DF002=1005, DF003=0, DF021=0, DF022=1, DF023=1, DF024=1, DF141=0, DF025=44440308028, DF142=1, DF001_1=0, DF026=30856712349, DF001_2=0, DF027=33666582560)>
```

---
## <a name="serializing">Serializing</a>

The `RTCMMessage` class implements a `serialize()` method to convert a `RTCMMessage` object to a bytes array suitable for writing to an output stream.

e.g. to create and send a `CFG-MSG` command which sets the NMEA GLL (*msgClass 0xf0, msgID 0x01*) message rate to 1 on the receiver's UART1 and USB ports:

```python
>>> from serial import Serial
>>> serialOut = Serial('COM7', 38400, timeout=5)
>>> from pyrtcm import RTCMMessage
>>> msg = RTCMMessage(b">\xd0\x00\x03\x8aX\xd9I<\x87/4\x10\x9d\x07\xd6\xafH ")
>>> print(msg)
<RTCM(1005, DF002=1005, DF003=0, DF021=0, DF022=1, DF023=1, DF024=1, DF141=0, DF025=44440308028, DF142=1, DF001_1=0, DF026=30856712349, DF001_2=0, DF027=33666582560)>
>>> output = msg.serialize()
>>> output
b'\xd3\x00\x13>\xd0\x00\x03\x8aX\xd9I<\x87/4\x10\x9d\x07\xd6\xafH Z\xd7\xf7'
>>> serialOut.write(output)
```

---
## <a name="examples">Examples</a>


---
## <a name="extensibility">Extensibility</a>

The rtcm protocol is principally defined in the module `rtcmtypes_get.py` as a series of dictionaries. Message payload definitions must conform to the following rules:

```
1. attribute names must be unique within each message class
2. attribute types must be one of the valid data field types (DF026, DF059, etc.)
3. repeating or bitfield groups must be defined as a tuple ('numr', {dict}), where:
   'numr' is either:
     a. an integer representing a fixed number of repeats e.g. 32
     b. a string representing the name of a preceding attribute containing the number of repeats e.g. 'DF029'
   {dict} is the nested dictionary of repeating items or bitfield group
```

Repeating attribute names are parsed with a two-digit suffix (svid_01, svid_02, etc.). Nested repeating groups are supported.

---
## <a name="cli">Command Line Utility</a>

TODO

---
## <a name="gui">Graphical Client</a>

A python/tkinter graphical GPS client which supports NMEA, UBX and RTCM protocols is available at: 

[https://github.com/semuconsulting/PyGPSClient](https://github.com/semuconsulting/PyGPSClient)

---
## <a name="author">Author & License Information</a>

semuadmin@semuconsulting.com

![License](https://img.shields.io/github/license/semuconsulting/pyrtcm.svg)

`pyrtcm` is maintained entirely by volunteers. If you find it useful, a small donation would be greatly appreciated!

[![Donations](https://www.paypalobjects.com/en_GB/i/btn/btn_donate_LG.gif)](https://www.paypal.com/donate/?hosted_button_id=4TG5HGBNAM7YJ)
