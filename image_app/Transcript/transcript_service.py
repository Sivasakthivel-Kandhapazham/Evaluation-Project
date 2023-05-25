import openai
import numpy as np
from django.http import JsonResponse
from config import AppCongiuration
from Transcript.transcript_abc import TranscriptGeneral


class Imprint(TranscriptGeneral):
    def __init__(self, video_aduio_file, file_size, file_extension):
        self.video_aduio_file = video_aduio_file
        self.file_size = file_size
        self.file_extension = file_extension


    def speech_to_text_openai(self):
        try:      
            app_initiate = AppCongiuration()
            app_config = app_initiate.load_app_config_settings() 
            if self.video_aduio_file is None:
                return JsonResponse({"message": app_config.video_empty_msg , "responseCode": 220}, status=200)
               
            if not self.file_extension or self.file_extension.lower() not in app_config.video_file_types:
                    return JsonResponse({"message": app_config.video_extension_msg , "responseCode": 220}, status=200)
            
            if self.file_size > app_config.video_file_size:
                    return JsonResponse({"message": f'{app_config.video_size_error_message} {np.round(self.file_size/1048576,0)} MB', "responseCode": 220}, status=200)

            openai.api_key = app_config.openai_api_key  
            transcript = openai.Audio.transcribe("whisper-1", self.video_aduio_file)
            return JsonResponse({"message": transcript, "responseCode": 200}, status=200)
        except Exception as ex:
            return JsonResponse({"message": ex, "responseCode": 400}, status=200)


