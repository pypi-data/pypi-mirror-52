# `time_converter` [![build status](https://gitlab.physik.uni-kiel.de/ET/time_converter/badges/master/build.svg)](https://gitlab.physik.uni-kiel.de/ET/time_converter/commits/master) [![coverage report](https://gitlab.physik.uni-kiel.de/ET/time_converter/badges/master/coverage.svg)](http://et.page.physik.uni-kiel.de/time_converter/coverage/)

A Python class that allows for convenient conversion between different date and time formats and units.
The library supports both general-purpose Earth-based time units (such as Python's `datetime` type, Day-of-year or
POSIX time) as well as time units useful for working with data from the Mars Science Laboratory and Chang'e 4 space
missions. It can be easily extended to support additional units.

## Installation
```python
pip3 install time_converter
```

Yes, it's that simple.

## Usage
```python
from time_converter import Time

Time(2019.5, 'decimalyear').to('dt')
# > datetime.datetime(2019, 7, 2, 12, 0)
```

you can also supply list-like objects as input, the output will be a `numpy` array.
```python
Time([2018.0, 2018.1], 'decimalyear').to('dt')
# > array([datetime.datetime(2019, 1, 1, 0, 0),
#          datetime.datetime(2019, 2, 6, 11, 59, 59, 999997)], dtype=object)
```

## Supported units

### Earth-based time units

| Unit                          | Example                               | Name          | Abbreviated Name |
|-------------------------------|---------------------------------------|---------------|------------------|
| Python datetime (UTC)         | `datetime.datetime(2019, 1, 1, 0, 0)` | `datetime`    | `dt`             |
| DoY Tuple (year, day of year) | `(2019, 1.0)`                         | `doy`         |                  |
| Decimal year                  | `2019.0`                              | `decimalyear` | `dy`             |
| POSIX time                    | `1546300800`                          | `posix`       |                  |

### Mars Science Laboratory

The MSL spacecraft clock (`sclk`) measures the number of seconds since January 1 2000, 11:58:55.816 UTC. However, due to
drifting of the clock, some corrections need to be applied based on
[files supplied by NASA](https://naif.jpl.nasa.gov/pub/naif/pds/data/msl-m-spice-6-v1.0/mslsp_1000/data/sclk/sclkinfo.txt),
which this tool uses to do the conversion between `sclk` and other units.

| Unit                 | Example              | Name   |
|----------------------|----------------------|--------|
| MSL mission sol      | `2276.8306983767375` | `sol`  |
| MSL spacecraft clock | `599570768.5720837`  | `sclk` |

### Chang'E 4

For Chang'E 4, the conversion of spacecraft clock time to datetime has already implemented, so it does not need to be
included in time_converter. But we have implemented a converter for the lunar day number and local solar time at
Chang'E 4's landing site:

| Unit                           | Example                       | Name       |
|--------------------------------|-------------------------------|------------|
| Local solar time at Chang'E 4  | `1, datetime.time(7, 32, 30)` | `ce4lst`   |