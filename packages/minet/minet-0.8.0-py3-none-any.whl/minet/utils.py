# =============================================================================
# Minet Utils
# =============================================================================
#
# Miscellaneous helper function used throughout the library.
#
import re
import chardet
import cgi
import certifi
import browser_cookie3
import urllib3
from urllib3.exceptions import ClosedPoolError, HTTPError
from urllib.request import Request

from minet.defaults import (
    DEFAULT_CONNECT_TIMEOUT,
    DEFAULT_READ_TIMEOUT,
    DEFAULT_SPOOFED_UA
)

# Handy regexes
CHARSET_RE = re.compile(rb'<meta.*?charset=["\']*(.+?)["\'>]', flags=re.I)
PRAGMA_RE = re.compile(rb'<meta.*?content=["\']*;?charset=(.+?)["\'>]', flags=re.I)
XML_RE = re.compile(rb'^<\?xml.*?encoding=["\']*(.+?)["\'>]')

# Constants
CHARDET_CONFIDENCE_THRESHOLD = 0.9


def guess_encoding(response, data, is_xml=False, use_chardet=False):
    """
    Function taking an urllib3 response object and attempting to guess its
    encoding.
    """
    content_type_header = response.getheader('content-type')

    if content_type_header is not None:
        parsed_header = cgi.parse_header(content_type_header)

        if len(parsed_header) > 1:
            charset = parsed_header[1].get('charset')

            if charset is not None:
                return charset.lower()

    # TODO: use re.search to go faster!
    if is_xml:
        matches = re.findall(CHARSET_RE, data)

        if len(matches) == 0:
            matches = re.findall(PRAGMA_RE, data)

        if len(matches) == 0:
            matches = re.findall(XML_RE, data)

        # NOTE: here we are returning the last one, but we could also use
        # frequency at the expense of performance
        if len(matches) != 0:
            return matches[-1].lower().decode()

    if use_chardet:
        chardet_result = chardet.detect(data)

        if chardet_result['confidence'] >= CHARDET_CONFIDENCE_THRESHOLD:
            return chardet_result['encoding'].lower()

    return None


class CookieResolver(object):
    def __init__(self, jar):
        self.jar = jar

    def __call__(self, url):
        req = Request(url)
        self.jar.add_cookie_header(req)

        return req.get_header('Cookie') or None


def grab_cookies(browser='firefox'):
    if browser == 'firefox':
        try:
            return CookieResolver(browser_cookie3.firefox())
        except:
            return None

    if browser == 'chrome':
        try:
            return CookieResolver(browser_cookie3.chrome())
        except:
            return None

    raise Exception('minet.utils.grab_cookies: unknown "%s" browser.' % browser)


def dict_to_cookie_string(d):
    return '; '.join('%s=%s' % r for r in d.items())


def create_safe_pool(**kwargs):
    """
    Helper function returning a urllib3 pool manager with sane defaults.
    """

    return urllib3.PoolManager(
        cert_reqs='CERT_REQUIRED',
        ca_certs=certifi.where(),
        timeout=urllib3.Timeout(connect=DEFAULT_CONNECT_TIMEOUT, read=DEFAULT_READ_TIMEOUT),
        **kwargs
    )


def fetch(http, url, method='GET', headers=None, cookie=None, spoof_ua=True):
    """
    Generic fetch helpers using a urllib3 pool to access some resource.
    """

    # Formatting headers
    final_headers = {}

    if spoof_ua:
        final_headers['User-Agent'] = DEFAULT_SPOOFED_UA

    if cookie:
        if not isinstance(cookie, str):
            cookie = dict_to_cookie_string(cookie)

        final_headers['Cookie'] = cookie

    # Note: headers passed explicitly by users always win
    if headers is not None:
        final_headers.update(headers)

    # Performing request
    try:
        result = http.request(method, url, headers=final_headers)
    except (ClosedPoolError, HTTPError) as e:
        return e, None

    return None, result
