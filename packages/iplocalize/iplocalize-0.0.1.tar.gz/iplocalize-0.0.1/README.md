# iplocalize

Straight forward python3 library to test (quickly) and locate a bunch of free-proxy IP.

## Python module

```python
import iplocalize as ip

locator = ip.IPLoc()
locator.threaded_localize([['1.2.3.4', '1111'], ['5.6.7.8', '2222'], ...])
> > > { ip: '1.2.3.4:1111', cc: 'RU', time: 1.492218 }
```

IPLoc class will accept several parameters :

- `geolite_file`: path to your copy of Geolite2-city.mmdb (https://www.maxmind.com)
- `test_url`: the URL the proxy will be tested upon (http200, and faster than timeout)
- `timeout`: timeout (directly passed to requests, the actual request might be longer than timeout)
- `threads`: number of concurrent jobs

The default value for threads is 100, it might sound huge, but it gave me *me* pretty good results, feel free to tweak it to your needs.

## Command line

Just run : `iplocalize --help`

Nothing fun or complicated.

## Disclaimer

Geolocation is provided through Geolite mmdb files, they have a free version available through their website.
