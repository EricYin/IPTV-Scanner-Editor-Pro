import threading

try:
    import requests
    from requests.adapters import HTTPAdapter
    _HAS_REQUESTS = True
except ImportError:
    _HAS_REQUESTS = False
    requests = None
    HTTPAdapter = None

_session = None
_lock = threading.Lock()


def get_session():
    global _session
    if not _HAS_REQUESTS:
        return None
    if _session is None:
        with _lock:
            if _session is None:
                _session = requests.Session()
                adapter = HTTPAdapter(pool_connections=10, pool_maxsize=20, max_retries=0)
                _session.mount('http://', adapter)
                _session.mount('https://', adapter)
    return _session


def get(url, **kwargs):
    session = get_session()
    if session is None:
        raise ImportError('requests is not available')
    if 'timeout' not in kwargs:
        kwargs['timeout'] = (10, 30)
    elif isinstance(kwargs['timeout'], (int, float)):
        t = kwargs['timeout']
        kwargs['timeout'] = (min(t, 10), t)
    return session.get(url, **kwargs)


def head(url, **kwargs):
    session = get_session()
    if session is None:
        raise ImportError('requests is not available')
    if 'timeout' not in kwargs:
        kwargs['timeout'] = (10, 30)
    elif isinstance(kwargs['timeout'], (int, float)):
        t = kwargs['timeout']
        kwargs['timeout'] = (min(t, 10), t)
    return session.head(url, **kwargs)


def post(url, **kwargs):
    session = get_session()
    if session is None:
        raise ImportError('requests is not available')
    if 'timeout' not in kwargs:
        kwargs['timeout'] = (10, 30)
    elif isinstance(kwargs['timeout'], (int, float)):
        t = kwargs['timeout']
        kwargs['timeout'] = (min(t, 10), t)
    return session.post(url, **kwargs)


def close():
    global _session
    if _session is not None:
        with _lock:
            if _session is not None:
                _session.close()
                _session = None