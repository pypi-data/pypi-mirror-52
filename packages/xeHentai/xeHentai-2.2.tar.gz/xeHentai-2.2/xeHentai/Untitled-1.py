import requests
import random
try:
    from urlparse import urlparse, urlunparse
except:
    from urllib.parse import urlparse, urlunparse

class FallbackIpAdapter(requests.adapters.HTTPAdapter):
    def __init__(self, ip_map, **kwargs):
        self.ip_map = ip_map
        requests.adapters.HTTPAdapter.__init__(self, **kwargs)

    # override
    def get_connection(self, url, proxies=None):
        if not proxies:
            parsed = urlparse(url)
            _hostname = parsed.hostname
            _scheme = parsed.scheme
            if _hostname in self.ip_map:
                _parsed = list(parsed)
                # alter the hostname
                _hostname = '%s%s' % (random.choice(self.ip_map[_hostname]),
                                        (":%d" % parsed.port) if parsed.port else "")
                _scheme = 'https'
                print(parsed.scheme, _scheme)
            return self.poolmanager.connection_from_host(_hostname, parsed.port, scheme=_scheme,
                                                            pool_kwargs={'assert_hostname': parsed.hostname})
        else:
            # fallback
            return requests.adapters.HTTPAdapter.get_connection(self, url, proxies)
    
    def add_headers(self, request, **kwargs):
        if not request.headers.get('Host'):
            parsed = urlparse(request.url)
            request.headers['Host'] = parsed.hostname

    def cert_verify(self, conn, url, verify, cert):
        if url.startswith('http://'):
            url = "https://%s" % url[7:]
        return requests.adapters.HTTPAdapter.cert_verify(self, conn, url, verify, cert)
    
    # def __getattr__(self, k):
        # fallback attribute handler
    #    return getattr(self.super, k)
_FALLBACK_CF_IP = ("104.24.255.11", "104.24.254.11")

s = requests.Session()
s.mount('https://', FallbackIpAdapter({
    'e-hentai.org': _FALLBACK_CF_IP,
    'forums.e-hentai.org': ("94.100.18.243", ) + _FALLBACK_CF_IP,
    'exhentai.org': ("217.23.13.91","217.23.13.45","109.236.84.136","109.236.92.143","109.236.84.145","109.236.92.166")
} ))
s.mount('http://', FallbackIpAdapter({
    'e-hentai.org': _FALLBACK_CF_IP,
    'forums.e-hentai.org': ("94.100.18.243", ) + _FALLBACK_CF_IP,
    'exhentai.org': ("217.23.13.91","217.23.13.45","109.236.84.136","109.236.92.143","109.236.84.145","109.236.92.166")
} ))
# print(s.get('http://httpbin.tk/headers', proxies = {'http':'socks5://127.0.0.1:16961'}).content)
print(s.get('https://exhentai.org', allow_redirects=False).headers)