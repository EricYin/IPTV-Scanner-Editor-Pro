import importlib as _importlib
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from .bookmark_controller import BookmarkController
    from .catchup_controller import CatchupController
    from .channel_controller import ChannelController
    from .epg_controller import EPGController
    from .epg_reminder_controller import EpgReminderController
    from .event_handler import EventHandler
    from .favorites_controller import FavoritesController
    from .file_queue_controller import FileQueueController
    from .media_controller import MediaController
    from .multi_screen_controller import MultiScreenController
    from .pip_controller import PipController
    from .playback_controller import PlaybackController
    from .playback_settings_controller import PlaybackSettingsController
    from .progress_controller import ProgressController
    from .resume_playback_controller import ResumePlaybackController
    from .settings_file_ops import SettingsFileOperations
    from .skip_intro_outro_controller import SkipIntroOutroController
    from .subscription_controller import SubscriptionController
    from .subscription_ui_controller import SubscriptionUIController
    from .ui_controller import UIController
    from .update_controller import UpdateController
    from .window_controller import WindowController

_CONTROLLER_MODULES = {
    'BookmarkController': '.bookmark_controller',
    'CatchupController': '.catchup_controller',
    'ChannelController': '.channel_controller',
    'EPGController': '.epg_controller',
    'EpgReminderController': '.epg_reminder_controller',
    'EventHandler': '.event_handler',
    'FavoritesController': '.favorites_controller',
    'FileQueueController': '.file_queue_controller',
    'MediaController': '.media_controller',
    'MultiScreenController': '.multi_screen_controller',
    'PipController': '.pip_controller',
    'PlaybackController': '.playback_controller',
    'PlaybackSettingsController': '.playback_settings_controller',
    'ProgressController': '.progress_controller',
    'ResumePlaybackController': '.resume_playback_controller',
    'SettingsFileOperations': '.settings_file_ops',
    'SkipIntroOutroController': '.skip_intro_outro_controller',
    'SubscriptionController': '.subscription_controller',
    'SubscriptionUIController': '.subscription_ui_controller',
    'UIController': '.ui_controller',
    'UpdateController': '.update_controller',
    'WindowController': '.window_controller',
}


def __getattr__(name):
    if name in _CONTROLLER_MODULES:
        module = _importlib.import_module(_CONTROLLER_MODULES[name], __name__)
        cls = getattr(module, name)
        globals()[name] = cls
        return cls
    raise AttributeError(f"module {__name__!r} has no attribute {name!r}")


__all__ = [
    'BookmarkController',
    'CatchupController',
    'ChannelController',
    'EPGController',
    'EpgReminderController',
    'EventHandler',
    'FavoritesController',
    'FileQueueController',
    'MediaController',
    'MultiScreenController',
    'PipController',
    'PlaybackController',
    'PlaybackSettingsController',
    'ProgressController',
    'ResumePlaybackController',
    'SettingsFileOperations',
    'SkipIntroOutroController',
    'SubscriptionController',
    'SubscriptionUIController',
    'UIController',
    'UpdateController',
    'WindowController',
]

assert set(__all__) == set(_CONTROLLER_MODULES), "__all__ 与 _CONTROLLER_MODULES 不同步"
