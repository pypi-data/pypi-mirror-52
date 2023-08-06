import requests
from multiprocessing.pool import ThreadPool
from geoip2.database import Reader

geolite_default = '/app/GeoLite2-City_20190730/GeoLite2-City.mmdb'
default_test_url = 'https://www.example.com/'
default_threads = 100
default_timeout = 4

class IPLoc(object):
    """
    IPLoc object, an environment to try some (free) proxies and locate them
        - tries to efficiently run with a bunch of threads
        - no non-sense tests
    """
    def __init__(self,
                 geolite_file=geolite_default,
                 test_url=default_test_url,
                 timeout=default_timeout,
                 threads=default_threads,
                ):
        self.test_url = test_url
        self.reader = Reader(geolite_file)
        self.threads = threads
        self.timeout = timeout

    def threaded_localize(self, many_ip):
        """
        Triggers call to localize in a multithreaded fashion
        """
        with ThreadPool(processes=self.threads) as p:
            res = [ p.apply_async(self.localize, (ip,)) for ip in many_ip ]
            return [ r.get() for r in res ]

    def localize(self, ip):
        px = ':'.join(ip)
        proxies = {
            'http': "http://%s" % px,
            'https': "http://%s" % px
        }
        try:
            req = requests.get(self.test_url, proxies=proxies, timeout=self.timeout)
        except requests.exceptions.RequestException:
            return None 
        
        c = self.reader.city(ip_address=ip[0])
        if c is not None and c.country.iso_code is not None and req.status_code == 200:
            return {'ip': px, 'cc': c.country.iso_code, 'time': req.elapsed.total_seconds() }
        else: 
            return None

