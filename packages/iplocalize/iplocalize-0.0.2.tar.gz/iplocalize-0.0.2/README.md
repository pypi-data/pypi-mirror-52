# iplocalize

Straight forward python3 library to test (quickly) and locate a bunch of free-proxy IP.

[![Build Status](https://travis-ci.org/ylmrx/iplocalize.svg?branch=master)](https://travis-ci.org/ylmrx/iplocalize)

## Installation

```bash
pip install iplocalize
```

## Python module

```python
import iplocalize as ip

locator = ip.IPLoc()
locator.threaded_localize([['1.2.3.4', '1111'], ['5.6.7.8', '2222'], ...],
                            'path/to/geolite2-city.mmdb')
> > > { ip: '1.2.3.4:1111', cc: 'RU', time: 1.492218 }
```

IPLoc class will accept several parameters :

- `test_url`: the URL the proxy will be tested upon (http200, and faster than timeout)
- `timeout`: timeout (directly passed to requests, the actual request might be longer than timeout)
- `threads`: number of concurrent jobs

threaded_localize needs 2 parameters:
- a list of `['ip', 'port']` lists
- `geolite_file`: path to your copy of Geolite2-city.mmdb (https://www.maxmind.com)

The default value for threads is 100, it might sound huge, but it gave *me* pretty good results, feel free to tweak it to your needs.

You can call localize directly with:
- a single `['ip', 'port']` structure
- a `Reader()` object (cf. GeoIP2 module documentation)

## Command line

Just run : `iplocalize --help`

Nothing fun or complicated.

## Disclaimer

Geolocation is provided through Geolite mmdb files, they have a free version available through their website.
