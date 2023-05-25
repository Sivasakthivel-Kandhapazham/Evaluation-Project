from django.shortcuts import render
from django.urls import reverse
from django.http import HttpResponseRedirect, JsonResponse
from Transcript.transcript_service import Imprint
from config import AppCongiuration
from Logging.log_to_file import setup_logger

# Create your views here.
def video_text_view(request):
    if 'user_id' in request.session:
        return render(request,'video_speech/upload_video.html')
    else:
        redirect_path = reverse("logout")
        return HttpResponseRedirect(redirect_path)


def upload_video_process(request):
    if request.method == 'POST':
        try:
            video_aduio_file = request.FILES.get("video")  
            app_initiate = AppCongiuration()
            app_config = app_initiate.load_app_config_settings()
            logger = setup_logger()
            if video_aduio_file is None:
                logger.info(app_config.video_empty_msg)
                return JsonResponse({"message": app_config.video_empty_msg, "responseCode": 400}, status=200)
            file_extension = video_aduio_file.name.split('.')[-1]  
            file_size = video_aduio_file.size
            speech_text = Imprint(video_aduio_file, file_size, file_extension)
            result = speech_text.speech_to_text_openai()
            return result
        except Exception as ex:
            logger.error(f"Error occured while uploading video with name {video_aduio_file.name} exception : {ex}")
            return JsonResponse({"message": ex, "responseCode": 400}, status=200)
  