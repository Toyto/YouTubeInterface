from django.shortcuts import render, redirect
from .forms import UrlForm
from django.http import JsonResponse, HttpResponse, HttpResponseRedirect, HttpResponseBadRequest
from .service import get_video_info, VideoInfo
from django.views.generic import RedirectView, TemplateView, FormView, View
from .models import Video


class PublishView(FormView):
    template_name = 'core/publish.html'
    form_class = UrlForm

    def form_valid(self, form):
        url = form.cleaned_data.get('video_url')
        video = get_video_info(url)
        Video.objects.create(
            author=video.author, youtube_id=video.video_id
        )
        return redirect('index')



class VideoInfoView(View):

    def post(self, request, *args, **kwargs):
        form = UrlForm(data=request.POST)
        if form.is_valid():
            url = form.cleaned_data.get('video_url')
            video = get_video_info(url)
            return JsonResponse({
                'video_info': {
                    'title': video.title,
                    'description': video.description,
                    'video_id': video.video_id,
                    'author': video.author.name
                }
            })
        else:
            return HttpResponseBadRequest()

class IndexView(TemplateView):
    template_name = 'core/index.html'
