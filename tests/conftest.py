import sys
import os
import pytest
from unittest.mock import MagicMock

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

# PySide6 未安装时注入 mock，使测试可收集和运行
if 'PySide6' not in sys.modules:
    try:
        import PySide6  # noqa: F401
    except ImportError:
        _mock_qt = MagicMock()
        _mock_qt.QtCore = MagicMock()
        _mock_qt.QtCore.Qt = MagicMock()
        _mock_qt.QtCore.QThread = MagicMock()
        _mock_qt.QtCore.QTimer = MagicMock()
        _mock_qt.QtCore.Signal = lambda *a, **k: MagicMock()
        _mock_qt.QtCore.Slot = lambda *a, **k: (lambda f: f)
        _mock_qt.QtCore.QObject = MagicMock()
        _mock_qt.QtWidgets = MagicMock()
        _mock_qt.QtGui = MagicMock()
        sys.modules['PySide6'] = _mock_qt
        sys.modules['PySide6.QtCore'] = _mock_qt.QtCore
        sys.modules['PySide6.QtWidgets'] = _mock_qt.QtWidgets
        sys.modules['PySide6.QtGui'] = _mock_qt.QtGui


class MockMainWindow:
    """模拟 MainWindowProtocol 的最小实现，用于 Mixin 单元测试"""

    def __init__(self):
        self.config = MagicMock()
        self.language_manager = MagicMock()
        self.language_manager.tr = lambda key, default='': default
        self.status_bar = MagicMock()
        self._server_action = MagicMock()
        self._system_tray = MagicMock()
        self._is_hidden_to_tray = False
        self._was_playing_before_tray = False
        self._tray_hidden_docks = []
        self._force_quit = False
        self.player_controller = MagicMock()
        self.player_controller.is_playing = False
        self.player_controller.is_paused = False
        self.update_ctrl = MagicMock()
        self.ui_ctrl = MagicMock()
        self.sub_channel_list = MagicMock()
        self.local_channel_list = MagicMock()
        self._sub_channels = []
        self._local_channels = []
        self.play_state = MagicMock()
        self.play_state.is_catchup_or_timeshift = False
        self.event_handler = MagicMock()
        self.config_manager = MagicMock()
        self.epg_visible = False
        self.playlist_visible = False
        self.floating_panel_visible = False

        self.PLAYLIST_EXTENSIONS = ('.m3u', '.m3u8', '.txt')
        self.VIDEO_EXTENSIONS = ('.mp4', '.mkv', '.avi', '.mov', '.flv', '.wmv', '.ts', '.webm')
        self.AUDIO_EXTENSIONS = ('.mp3', '.flac', '.wav', '.aac', '.ogg', '.opus', '.wma', '.m4a', '.ape', '.alac', '.wv', '.tta', '.dts', '.ac3', '.mid', '.midi')
        self.ALL_DROP_EXTENSIONS = self.PLAYLIST_EXTENSIONS + self.VIDEO_EXTENSIONS + self.AUDIO_EXTENSIONS

    def status_bar_show_message(self, message, timeout=0):
        if self.status_bar:
            self.status_bar.showMessage(message, timeout)

    def show(self):
        pass

    def hide(self):
        pass

    def activateWindow(self):
        pass

    def raise_(self):
        pass

    def close(self):
        pass

    def setAttribute(self, *args, **kwargs):
        pass

    def setCursor(self, *args, **kwargs):
        pass

    def unsetCursor(self, *args, **kwargs):
        pass

    def cursor(self):
        m = MagicMock()
        m.pos.return_value = MagicMock()
        return m

    def rect(self):
        m = MagicMock()
        m.contains.return_value = True
        return m

    def mapFromGlobal(self, pos):
        return pos

    def mousePressEvent(self, event):
        pass

    def mouseMoveEvent(self, event):
        pass

    def mouseReleaseEvent(self, event):
        pass

    def mouseDoubleClickEvent(self, event):
        pass

    def enterEvent(self, event):
        pass

    def leaveEvent(self, event):
        pass


@pytest.fixture
def mock_main_window():
    return MockMainWindow()