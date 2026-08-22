import sys
import os


def setup_environment():
    if sys.platform == 'darwin' and getattr(sys, 'frozen', False):
        try:
            import certifi
            os.environ['SSL_CERT_FILE'] = certifi.where()
            os.environ['REQUESTS_CA_BUNDLE'] = certifi.where()
        except ImportError:
            _cert_path = os.path.join(os.path.dirname(sys.executable), 'resources', 'cert.pem')
            if os.path.exists(_cert_path):
                os.environ['SSL_CERT_FILE'] = _cert_path
                os.environ['REQUESTS_CA_BUNDLE'] = _cert_path

    if sys.platform.startswith('linux') and 'ANDROID_ARGUMENT' not in os.environ:
        session_type = os.environ.get('XDG_SESSION_TYPE', '').lower()
        wayland_display = os.environ.get('WAYLAND_DISPLAY', '')
        is_wayland_env = (session_type == 'wayland') or (bool(wayland_display) and session_type != 'x11')
        if is_wayland_env and not os.environ.get('QT_QPA_PLATFORM'):
            os.environ['QT_QPA_PLATFORM'] = 'xcb'

    sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))