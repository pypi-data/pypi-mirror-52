import argparse
import iplocalize.localize as ip
from pygments import highlight
from pygments.lexers import PythonLexer
from pygments.formatters import Terminal256Formatter
from pprint import pformat

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--url", default=ip.default_test_url, type=str,
                        help="URL to test the proxy against (success: http200, within timeout)")
    parser.add_argument("--timeout", default=ip.default_timeout, type=int,
                        help="Timeout")
    parser.add_argument("--threads", default=ip.default_threads, type=int,
                        help="Number of parallel tests we can run")
    parser.add_argument("--geofile", default=ip.geolite_default,
                        help="Path to the Geolite database")
    parser.add_argument("addresses", nargs='+', type=str,
                        help="One or more addresses to tests as free unauthenticated proxies")
    args = parser.parse_args()

    locator = ip.IPLoc(geolite_file=args.geofile,
                       test_url=args.url,
                       timeout=args.timeout,
                       threads=args.threads)
    px_to_check = [ ip_port.split(':') for ip_port in args.addresses ]
    located_px = locator.threaded_localize(px_to_check)
    print(highlight(pformat(located_px), PythonLexer(), Terminal256Formatter()))

if __name__ == '__main__':
    main()
