import json
import logging
import os

_setting_path = os.path.join(os.path.expanduser('~'), 'fh-asset')
_default_settings = {
    'root_path': os.path.join(_setting_path, 'Assets'),
    'asset_label_color': (160, 160, 160, 255),
    'init_panel_size': [240, 400, 200]
}


def _loadSettings(setting_dir):
    settings_file = os.path.join(setting_dir, 'settings.json')
    settings = {}

    if os.path.isfile(settings_file):
        with open(settings_file, 'r') as f:
            try:
                settings = json.load(f)
            except Exception as e:
                logging.warning('Cannot read setting file', e)
    else:
        # write default setting
        if not os.path.isdir(setting_dir):
            os.makedirs(setting_dir)
        with open(settings_file, 'w+') as f:
            json.dump(_default_settings, f, indent=2)

    settings = {k: v for (k, v) in settings.items() if v is not None}
    s = _default_settings.copy()
    s.update(settings)
    return s


asset_file = 'asset.json'
asset_def_file = 'assetDef.json'
thumbnail_filename = 'thumbnail'

_settings = _loadSettings(_setting_path)

root_path = _settings['root_path']
asset_label_color = tuple(_settings['asset_label_color'])
init_panel_sizes = _settings['init_panel_size']

# ensure root path exist
if not os.path.isdir(root_path):
    os.makedirs(root_path)
