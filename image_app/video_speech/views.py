from django.shortcuts import render
from django.urls import reverse
from django.http import HttpResponseRedirect, JsonResponse
from .transcript_service import Transcript
from image_app.__init__ import video_empty_msg

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
            if video_aduio_file is None:
                return JsonResponse({"message": video_empty_msg, "responseCode": 400}, status=200)
            file_extension = video_aduio_file.name.split('.')[-1]  
            file_size = video_aduio_file.size
            tanscript = Transcript(video_aduio_file, file_size, file_extension)
            result = tanscript.speech_to_text_transcript()
            return result
        except Exception as ex:
            return JsonResponse({"message": ex, "responseCode": 400}, status=200)
  