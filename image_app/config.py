import tomllib

class AppCongiuration:
    def __init__(self):
        pass

    def load_app_config_settings(self):
        config_filepath = 'config.toml'
        with open(config_filepath, 'rb') as f:
            config = tomllib.load(f)
            self.image_file_size = config['image_validation']['max_file_size']
            self.image_file_types = config['image_validation']['image_file_types']   
            self.image_size_error_message = config['image_error_message']['image_size'] 
            self.image_empty_msg = config['image_error_message']['image_empty']
            self.image_extension_msg = config['image_error_message']['image_extension']

            self.video_file_size = config['video_validation']['video_max_size']
            self.video_file_types = config['video_validation']['video_file_types']   
            self.video_size_error_message = config['video_error_message']['video_size']
            self.video_empty_msg = config['video_error_message']['video_empty']
            self.video_extension_msg = config['video_error_message']['video_extension']

            self.openai_api_key = config['openai_whisper']['api_key']

            self.sender_email_id = config['email_service']['sender_email_id']
            self.receiver_email_id = config['email_service']['receiver_email_id']
            self.email_auth = config['email_service']['email_auth']
            self.sender_email_msg = config['email_service']['sender_email_msg']

            self.web_scraping_imdb = config['web_scraping']['web_scraping_imdb']
            self.web_scraping_metacritic = config['web_scraping']['web_scraping_metacritic']
            self.imdb_movie_site = config['web_scraping']['imdb_movie_site']
            self.meta_critic_netflix = config['web_scraping']['meta_critic_netflix']
            self.meta_critic_piv = config['web_scraping']['meta_critic_piv']
            self.meta_critic_hulu = config['web_scraping']['meta_critic_hulu']
            return self
    