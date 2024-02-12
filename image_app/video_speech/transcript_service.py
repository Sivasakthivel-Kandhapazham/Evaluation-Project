import openai
import numpy as np
from django.http import JsonResponse
from image_app.__init__ import openai_api_key, video_file_size, video_file_types, video_size_error_message, video_empty_msg, video_extension_msg


class Transcript:
    def __init__(self, video_aduio_file, file_size, file_extension):
        self.video_aduio_file = video_aduio_file
        self.file_size = file_size
        self.file_extension = file_extension


    def speech_to_text_transcript(self):
        try:              
            if self.video_aduio_file is None:
                return JsonResponse({"message": video_empty_msg , "responseCode": 220}, status=200)
               
            if not self.file_extension or self.file_extension.lower() not in video_file_types:
                    return JsonResponse({"message": video_extension_msg , "responseCode": 220}, status=200)
            
            if self.file_size > video_file_size:
                    return JsonResponse({"message": f'{video_size_error_message} {np.round(self.file_size/1048576,0)} MB', "responseCode": 220}, status=200)
            
            openai.api_key = openai_api_key  
            transcript = openai.Audio.transcribe("whisper-1", self.video_aduio_file)
            return JsonResponse({"message": transcript, "responseCode": 200}, status=200)
        except Exception as ex:
            return JsonResponse({"message": ex, "responseCode": 400}, status=200)


