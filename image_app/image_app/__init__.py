import tomllib

config_filepath = 'config.toml'
with open(config_filepath, 'rb') as f:
         config = tomllib.load(f)
         image_file_size = config['image_validation']['max_file_size']
         image_file_types = config['image_validation']['image_file_types']   
         image_size_error_message = config['image_error_message']['image_size'] 
         image_empty_msg = config['image_error_message']['image_empty']
         image_extension_msg = config['image_error_message']['image_extension']

         video_file_size = config['video_validation']['video_max_size']
         video_file_types = config['video_validation']['video_file_types']   
         video_size_error_message = config['video_error_message']['video_size']
         video_empty_msg = config['video_error_message']['video_empty']
         video_extension_msg = config['video_error_message']['video_extension']

         openai_api_key = config['openai_whisper']['api_key']


# Make the config_value accessible outside __init__.py
__all__ = ["image_file_size", "image_file_types", "image_size_error_message", 
           "image_empty_msg", "image_extension_msg", "video_file_size", "video_file_types",
           "video_size_error_message", "video_empty_msg", "video_extension_msg", "openai_api_key"]



    