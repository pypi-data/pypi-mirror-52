import os
from .helpers import folder_files, load_json_file, merge_dicts
from flask.helpers import get_root_path, get_env

# basedir = os.path.abspath(os.path.dirname(__file__))
basedir = get_root_path()


class FrameConfig():
    frame_config = {'app': {}}

    # 组装全部配置
    def __init__(self):
        app_config = {}
        vendor_config = {}
        env = get_env() or 'product'
        FrameConfig.from_folder()

        @staticmethod
        def from_folder(config_path=None, rule='*.json'):
            if config_path == None:
                config_path = get_root_path('config')
            config_files = folder_files(config_path, rule)
            # print('24', config_files)
            for config_file in config_files:
                file_name = config_file.split('.')[0]
                config_file_path = os.path.join(config_path, config_file)
                config_content = load_json_file(config_file_path)
                env_config = config_content.get(env, {})
                product_config = config_content.get('product')
                app_config[file_name] = merge_dicts(product_config, env_config)

            FrameConfig.frame_config = app_config