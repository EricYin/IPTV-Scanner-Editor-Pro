import socket
import threading
from concurrent.futures import ThreadPoolExecutor
from urllib.parse import urlparse
from PySide6.QtCore import QObject, Signal
from core.log_manager import global_logger as logger


class DnsPrefetcher(QObject):
    dns_resolved = Signal(str, str)

    MAX_WORKERS = 8

    def __init__(self, parent=None):
        super().__init__(parent)
        self._cache = {}
        self._lock = threading.Lock()
        self._executor = ThreadPoolExecutor(max_workers=self.MAX_WORKERS)

    def prefetch(self, url):
        if not url:
            return
        if self._executor is None:
            return
        try:
            parsed = urlparse(url)
            host = parsed.hostname
            if not host:
                return
            with self._lock:
                if host in self._cache:
                    return
            try:
                self._executor.submit(self._resolve, host)
            except RuntimeError:
                pass
        except Exception as e:
            logger.debug(f"DNS 预解析提交失败: {e}")

    def prefetch_many(self, urls):
        for url in urls:
            self.prefetch(url)

    def _resolve(self, host):
        try:
            infos = socket.getaddrinfo(host, None, socket.AF_UNSPEC, socket.SOCK_STREAM)
            if infos:
                ip = infos[0][4][0]
                with self._lock:
                    self._cache[host] = ip
                try:
                    self.dns_resolved.emit(host, ip)
                except RuntimeError:
                    pass
        except Exception as e:
            logger.debug(f"DNS 预解析失败 {host}: {e}")

    def get_cached_ip(self, host):
        with self._lock:
            return self._cache.get(host)

    def clear(self):
        with self._lock:
            self._cache.clear()

    def shutdown(self):
        if self._executor:
            self._executor.shutdown(wait=False)
            self._executor = None


class ConnectionPreheater(QObject):
    connection_ready = Signal(str)

    MAX_WORKERS = 8

    def __init__(self, parent=None):
        super().__init__(parent)
        self._cache = set()
        self._lock = threading.Lock()
        self._executor = ThreadPoolExecutor(max_workers=self.MAX_WORKERS)

    def preheat(self, url):
        if not url:
            return
        if self._executor is None:
            return
        try:
            parsed = urlparse(url)
            host = parsed.hostname
            port = parsed.port
            if not host:
                return
            scheme = parsed.scheme.lower()
            if not port:
                if scheme == 'https':
                    port = 443
                elif scheme == 'http':
                    port = 80
                elif scheme == 'rtsp':
                    port = 554
                else:
                    return
            cache_key = f"{host}:{port}"
            with self._lock:
                if cache_key in self._cache:
                    return
            try:
                self._executor.submit(self._connect, host, port, cache_key)
            except RuntimeError:
                pass
        except Exception as e:
            logger.debug(f"连接预热提交失败: {e}")

    def preheat_many(self, urls):
        for url in urls:
            self.preheat(url)

    def _connect(self, host, port, cache_key):
        try:
            sock = socket.create_connection((host, port), timeout=3)
            sock.close()
            with self._lock:
                self._cache.add(cache_key)
            try:
                self.connection_ready.emit(cache_key)
            except RuntimeError:
                pass
        except Exception as e:
            logger.debug(f"连接预热失败 {cache_key}: {e}")

    def clear(self):
        with self._lock:
            self._cache.clear()

    def shutdown(self):
        if self._executor:
            self._executor.shutdown(wait=False)
            self._executor = None
